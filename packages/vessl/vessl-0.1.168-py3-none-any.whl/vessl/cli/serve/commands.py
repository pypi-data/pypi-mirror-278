"""
Serving command definition and delegation.
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, TextIO, Tuple

import click
import yaml

from openapi_client.models import (
    ClusterClusterListResponse,
    ModelServiceCreateAPIInput,
    ModelserviceModelServiceListResponse,
    ModelserviceModelServiceReadResponse,
    ResponseKernelClusterInfo,
    ResponseModelServiceInfo,
    secret_upsert_generic_secret_api_input,
)
from openapi_client.models.response_kernel_cluster import ResponseKernelCluster
from openapi_client.models.response_path_operation import ResponsePathOperation
from openapi_client.models.response_volume_source_entity import (
    ResponseVolumeSourceEntity,
)
from openapi_client.models.v1_autoscaling import V1Autoscaling
from openapi_client.models.v1_auxiliary_form import V1AuxiliaryForm
from openapi_client.models.v1_command import V1Command
from openapi_client.models.v1_env_form import V1EnvForm
from openapi_client.models.v1_env_var import V1EnvVar
from openapi_client.models.v1_import_form import V1ImportForm
from openapi_client.models.v1_model_ref_form import V1ModelRefForm
from openapi_client.models.v1_port_path import V1PortPath
from openapi_client.models.v1_resources_form import V1ResourcesForm
from openapi_client.models.v1_serve_revision_service_form import (
    V1ServeRevisionServiceForm,
)
from vessl import vessl_api
from vessl.cli import serve
from vessl.cli._base import VesslCommand, VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import (
    Endpoint,
    print_debug,
    print_error,
    print_error_result,
    print_info,
    print_success,
    print_table_tabulate,
    prompt_checkbox,
    prompt_choices,
    prompt_confirm,
    prompt_text,
)
from vessl.cli.serve.util import print_gateway, print_revision
from vessl.enums import ClusterProvider, ModelServiceType
from vessl.models.vessl_model import VesslModel
from vessl.kernel_cluster import list_cluster_presets, list_clusters
from vessl.organization import _get_organization_name
from vessl.secret import list_generic_secrets
from vessl.serving import (
    _wait_for_gateway_enabled,
    _wait_for_revision_to_launch,
    abort_in_progress_rollout,
    abort_in_progress_rollout_by_name,
    create_active_revision_replacement_rollout,
    create_revision_from_yaml,
    create_revision_from_yaml_v2,
    get_recent_rollout,
    launch_revision,
    list_revisions,
    list_services,
    read_gateway,
    read_revision,
    read_service,
    terminate_revision,
    update_model_service,
    update_revision_autoscaler_config,
)
from vessl.util.constant import (
    VESSL_SERVICE_TENSORFLOW_BASE_IMAGE_TEMPLATE,
    VESSL_SERVICE_TORCH_BASE_IMAGE_TEMPLATE,
)
from vessl.util.exception import VesslApiException

from .command_options import format_option, service_name_option

cli = VesslGroup("serve")


@cli.command("list", cls=VesslCommand)
def serving_list():
    """
    List servings in current organization.
    """
    servings: List[ResponseModelServiceInfo] = list_services(
        organization=vessl_api.organization.name
    ).results

    print(f"{len(servings)} serving(s) found.\n")
    for serving in servings:
        kernel_cluster: ResponseKernelCluster = serving.kernel_cluster
        status: str = serving.status  # "ready", "running", "error"

        print(f"{serving.name} (cluster {kernel_cluster.name}): status {status.capitalize()}")


@cli.group("revision")
def cli_revision():
    """
    Root command for revision-related commands.
    """
    pass


@cli.command("abort-update", cls=VesslCommand)
@service_name_option
def abort_update(service: ResponseModelServiceInfo):
    """
    Abort the current revision update.
    """
    try:
        abort_in_progress_rollout(service=service)
    except VesslApiException as e:
        print(f"Failed to abort the service update: {e.message}")
        sys.exit(1)


@cli.command("create", cls=VesslCommand)
@click.option(
    "-f",
    "--file",
    type=click.File("r"),
    required=True,
    help="Path to YAML file for service revision definition.",
)
@click.option(
    "-y",
    "--no-prompt",
    type=click.BOOL,
    is_flag=True,
    help="do not ask anything while creating revision"
)
@click.option(
    "-l",
    "--launch",
    type=click.BOOL,
    is_flag=True,
    help="Launch after creating revision.",
)
@click.option(
    "-a",
    "--set-current-active",
    type=click.BOOL,
    is_flag=True,
    help="Launch and send traffic to the created revision. If another live revision exists, replace the existing revision.",
)
@click.option(
    "--force",
    type=click.BOOL,
    is_flag=True,
    help="force to abort the existing rollout.",
)
@click.option(
    "-s",
    "--service-name",
    type=click.STRING,
    help="Name of service to create this revision inside. "
    "If such service does not exist, you will be be asked on whether to create one. "
    "If service name is not given, but YAML has a name field, "
    "then that name will be used.",
)
@click.option(
    "--serverless",
    type=click.BOOL,
    is_flag=True,
    help="If the service does not exist and should be created, this flag requires "
    "the service to be serverless. If not given, it defaults to provisioned. "
    "If this parameter is given, but the named service is not in serverless mode, "
    "an error is raised.",
)
def revision_create_with_yaml(
    file: TextIO,
    no_prompt: bool,
    launch: bool,
    set_current_active: bool,
    force: bool,
    service_name: str,
    serverless: bool,
):
    """
    Create a revision from a YAML file.

    The YAML file should contain the definition of the revision. See https://docs.vessl.ai/guides/serve/service-yaml

    Example:
    $ vessl serve revision create -f service.yaml --set-current-active
    """
    organization_name = vessl_api.set_organization()
    vessl_api.configure_default_organization(organization_name)

    yaml_body = file.read()
    try:
        yaml_loaded = yaml.safe_load(yaml_body)
    except yaml.YAMLError as e:
        print_error(f"Error: invalid YAML\n{e}")
        sys.exit(1)

    if not isinstance(yaml_loaded, dict):
        print_error(f"Error: invalid YAML: expected mapping (dict), got {type(yaml_loaded)}")
        sys.exit(1)

    try:
        cluster_name = yaml_loaded["resources"]["cluster"]
    except (KeyError, TypeError):
        print_error("Error: invalid YAML: no cluster name")
        sys.exit(1)

    service_name_from_legacy_yaml = yaml_loaded.get("name", None)

    service_name = service_name or service_name_from_legacy_yaml or None
    service_name, service_type = _check_service_name_or_prompt(
        service_name=service_name,
        cluster_name=cluster_name,
        serverless=serverless,
        no_prompt=no_prompt,
    )

    max_timeout = 8 * 60  # sec

    ## Check if the service is already rolling out
    ongoing_rollout_exists = False
    try:
        recent_rollout = get_recent_rollout(service_name)
        if recent_rollout and recent_rollout.status == "rolling_out":
            ongoing_rollout_exists = True
            print_error(f"Error: the service {service_name} is currently rolling out.")
            if not force:
                print_error("Use --force option to abort the existing rollout.")
                sys.exit(1)
    except VesslApiException as e:
        print_debug("No existing rollout found.")
        pass

    ## Abort the existing rollout if --force
    if ongoing_rollout_exists and force:
        if abort_in_progress_rollout_by_name(service_name):
            print_info("Waiting for the existing rollout to be aborted...")
            time.sleep(30)

    ## create revision
    try:
        revision = create_revision_from_yaml_v2(
            organization=vessl_api.organization.name,
            service_name=service_name,
            yaml_body=yaml_body,
            serverless=(service_type == ModelServiceType.SERVERLESS),
        )
    except VesslApiException as e:
        if e.status == 400:
            print_error("Error: failed to create revision (invalid parameters).")
            print_error_result(e.message)
        else:
            print_error("Error: failed to create revision. (internal error).")
        sys.exit(1)

    if service_type == ModelServiceType.SERVERLESS:
        service_url = Endpoint.service.format(vessl_api.organization.name, service_name)
        print_success(f"Successfully created revision #{revision.number}!")
        print()
        print_success(f"Check out the service at: {service_url}")
        print()
        return

    ## launch or set-active
    if set_current_active:
        launch = True
    if not launch and not no_prompt:
        launch = prompt_confirm("Do you want to launch this revision immediately?")
    if launch:
        if not set_current_active and not no_prompt:
            set_current_active = prompt_confirm("Do you want to replace the current open-to-public revision?")

    try:
        if set_current_active:
            create_active_revision_replacement_rollout(
                organization=vessl_api.organization.name,
                model_service_name=revision.model_service_name,
                desired_active_revisions_to_weight_map={revision.number: 100},
            )
        elif launch:
            launch_revision(
                organization=vessl_api.organization.name,
                service_name=revision.model_service_name,
                revision_number=revision.number,
            )
        print_info("Successfully triggered revision launch.")
        if not no_prompt:
            _wait_for_revision_to_launch(service_name=service_name, revision_number=revision.number, print_output=True)
        revision = read_revision(
            organization=vessl_api.organization.name,
            service_name=revision.model_service_name,
            revision_number=revision.number,
        )
        print_revision(revision)
        
    except VesslApiException as e:
        print_error("Error: failed to launch revision.")
        print_error_result(e.message)
        sys.exit(1)

    ## Wait for the gateway to be enabled
    if set_current_active:
        gateway = read_gateway(
            organization=vessl_api.organization.name,
            service_name=revision.model_service_name,
        )
        if not no_prompt:
            _wait_for_gateway_enabled(gateway=gateway, service_name=revision.model_service_name, print_output=True)

        print_info("Endpoint is enabled.")
        gateway = read_gateway(
                organization=vessl_api.organization.name,
                service_name=service_name,
            )
        print_gateway(gateway)
        print_info(f"You can test your service via {gateway.endpoint}")


@cli_revision.command("show", cls=VesslCommand)
@service_name_option
@click.option("--number", "-n", required=True, type=int, help="Number of revision.")
@format_option
@vessl_option("-o", "--output", "output", type=click.Path(), help="Output file path.")
def revision_show(service: ResponseModelServiceInfo, number: int, format: str, output: str):
    """
    Show current status and information about a service revision.
    """
    try:
        revision = read_revision(
            organization=vessl_api.organization.name,
            service_name=service.name,
            revision_number=number,
        )
    except VesslApiException as e:
        print(f"Failed to read revision #{number} of service {service.name}: {e.message}")
        sys.exit(1)

    result = ""
    if format == "text":
        print_revision(revision, verbose=True)
        return
    if format == "json":
        result = json.dumps(revision.to_dict(), default=str)
    if format == "yaml":
        result = revision.yaml_spec
    
    if output:  
        with open(output, "w") as f:
            f.write(result)
    else:
        print_info(result)


def _translate_vops(vops: List[ResponsePathOperation]) -> dict:
    def _parse_source_entity(e: ResponseVolumeSourceEntity, t: str) -> str:
        if t == "model":
            org = e.model.model_repository.organization.name
            model_repo_name = e.model.model_repository.name
            model_num = e.model.model.number
            return f"vessl-model://{org}/{model_repo_name}/{model_num}"
        if t == "dataset":
            org = e.dataset.organization.name
            dataset_name = e.dataset.name
            return f"vessl-dataset://{org}/{dataset_name}"
        if t == "artifact":
            name = e.artifact.persistent.name
            return f"vessl-artifact://{name}"
        if t == "git":
            provider = e.git.repository.provider
            owner = e.git.repository.owner
            repo = e.git.repository.repo
            if provider == "bitbucket":
                return f"git://bitbucket.org/{owner}/{repo}"
            if provider == "huggingface":
                return f"hf://huggingface.co/{owner}/{repo}"
            else:
                return f"git://{provider}.com/{owner}/{repo}"
        if t == "s3":
            bucket = e.s3.bucket
            prefix = e.s3.prefix
            return f"s3://{bucket}/{prefix}"
        if t == "gs":
            bucket = e.gs.bucket
            prefix = e.gs.prefix
            return f"gs://{bucket}/{prefix}"
        if t == "hostpath":
            path = e.hostpath.path
            return f"hostpath://{path}"
        if t == "nfs":
            server = e.nfs.server
            path = e.nfs.path
            return f"nfs://{server}/{path}"
        if t == "cifs":
            return None
        if t == "googledisk":
            return None
        else:
            return None

    res = {
        "import": {},
        "mount": {},
    }
    for item in vops:
        if item._import:
            source_entity = item._import.source_entity
            t = source_entity.source_entity_type
            signature = _parse_source_entity(source_entity, t)
            res["import"][item.path] = signature
        if item.mount:
            source_entity = item.mount.source_entity
            t = source_entity.source_entity_type
            signature = _parse_source_entity(source_entity, t)
            res["mount"][item.path] = signature
    if not res["import"]:
        del res["import"]
    if not res["mount"]:
        del res["mount"]
    return res

def _translate_envvars(envvars: Dict[str,V1EnvVar]) -> dict:
    res = {}
    for k, v in envvars.items():
        if v.default_value.source == "secret":
            res[k] = {
                "secret": v.default_value.secret,
                "source": v.default_value.source,
            }
        if v.default_value.source == "text":
            res[k] = {
                "text": v.default_value.text,
                "source": v.default_value.source,
            }
    return res



@cli_revision.command("list", cls=VesslCommand)
@service_name_option
@format_option
def revision_list(service: ResponseModelServiceInfo, format: str):
    """
    List all revisions.
    """
    try:
        revisions = list_revisions(
            organization=vessl_api.organization.name,
            service_name=service.name,
        )
    except VesslApiException as e:
        print(f"Failed to list revisions of serving {service.name}: {e.message}")
        sys.exit(1)

    if format == "json":
        print(json.dumps([r.to_dict() for r in revisions], default=str))
    if format == "yaml":
        print("\n\n".join([r.yaml_spec for r in revisions]))
    else:
        print(f"{len(revisions)} revision(s) found.\n")
        for i, revision in enumerate(revisions):
            if i > 0:
                print()
            print_revision(revision)


@cli_revision.command("terminate", cls=VesslCommand)
@service_name_option
@click.option("--number", "-n", required=True, type=int, help="Number of revision.")
def revision_terminate(service: ResponseModelServiceInfo, number: int):
    """
    Terminate specified revision.
    """
    try:
        terminate_revision(
            organization=vessl_api.organization.name,
            service_name=service.name,
            revision_number=number,
        )
        print("Successfully terminated revision.")
    except VesslApiException as e:
        print(f"Failed to terminate revision #{number} of serving {service.name}: {e.message}")
        sys.exit(1)


@cli_revision.command("scale", cls=VesslCommand)
@service_name_option
@click.option("--number", "-n", required=True, type=int, help="Number of revision.")
@click.option("--min", required=False, type=int, help="Number of min replicas.")
@click.option("--max", required=False, type=int, help="Number of max replicas.")
@click.option("--target", required=False, type=int, help="Target resource utilization.")
@click.option("--metric", required=False, type=str, help="Metric for autoscaling.")
def revision_update_autoscaler_config(
    service: ResponseModelServiceInfo,
    number: int,
    min: Optional[int],
    max: Optional[int],
    target: Optional[int],
    metric: Optional[str],
):
    """
    Update revision's autoscaler config
    """
    try:
        current_revision = read_revision(
            organization=vessl_api.organization.name,
            service_name=service.name,
            revision_number=number,
        )

        conf: V1Autoscaling = current_revision.revision_spec.autoscaling
        if conf is None:
            conf = V1Autoscaling(
                min=1,
                max=1,
                metric="cpu",
                target=60,
            )
        if min is not None:
            conf.min = min
        if max is not None:
            conf.max = max
        if target is not None:
            conf.target = target
        if metric is not None:
            conf.metric = metric

        update_revision_autoscaler_config(
            organization=vessl_api.organization.name,
            service_name=service.name,
            revision_number=number,
            autoscaling=conf,
        )
        print("Successfully updated autoscaler config.")
    except VesslApiException as e:
        print(
            f"Failed to update autoscaler config of revision #{number} of serving {service.name}: {e.message}"
        )
        sys.exit(1)


@cli.group("gateway")
def cli_gateway():
    """
    Root command for gateway-related commands.
    """
    pass


@cli_gateway.command("show", cls=VesslCommand)
@service_name_option
@format_option
def gateway_show(service: ResponseModelServiceInfo, format: str):
    """
    Show current status of the gateway of a serving.
    """
    try:
        gateway = read_gateway(
            organization=vessl_api.organization.name,
            service_name=service.name,
        )
    except VesslApiException as e:
        print(f"Failed to read gateway of serving {service.name}: {e.message}")
        sys.exit(1)

    if format == "json":
        print(json.dumps(gateway.to_dict(), default=str))
    else:
        print_gateway(gateway)


@cli.command("update", cls=VesslCommand)
@click.option(
    "--number",
    "-n",
    required=False,
    type=int,
    multiple=True,
    help="Number of revisions to launch."
)
@click.option(
    "--weight",
    "-w",
    required=False,
    type=int,
    multiple=True,
    help="Number of traffic weight for the revision",
)
@click.option(
    "--interactive",
    is_flag=True,
    type=click.BOOL,
    help="Update service interactively"
)
@service_name_option
def update(service: ResponseModelServiceInfo, number: List[int], weight: List[int], interactive: bool):
    """
    Update a revision's traffic weight.

    Example:
    
    $ vessl serve update --service my-service -n 1 -w 100 
    $ vessl serve update --service my-service -n 1 -w 60 -n 2 -w 40
    $ vessl serve update --service my-service --interactive 
    """
    # TODO(seokju) revisit later
    if not interactive:
        update_model_service(service, number, weight)
        return

    """
    Current Gateway
    """
    gateway_current = read_gateway(
        organization=vessl_api.organization.name, service_name=service.name
    )
    print_info(f"Current Endpoint Host: {gateway_current.endpoint}")
    print_info("Traffic Rules")
    if gateway_current.rules:
        current_rules = [
            {
                "Revision Number": i.revision_number,
                "Traffic Weight": f'{i.traffic_weight}%',
            }
            for i in gateway_current.rules
        ]
        print_table_tabulate(current_rules)

    """
    Current Revisions Status
    """
    revisions = list_revisions(organization=vessl_api.organization.name, service_name=service.name)
    revision_data = [
        {
            "Revision Number": revision.number,
            "Min Replicas": revision.revision_spec.autoscaling.min if revision.revision_spec.autoscaling else "N/A",
            "Max Replicas": revision.revision_spec.autoscaling.max if revision.revision_spec.autoscaling else "N/A",
            "Status": revision.status,
        }
        for revision in revisions
    ]
    print_info(f"Current Revisions")
    print_table_tabulate(revision_data)

    """
    Get Rollout Spec
    """
    target_revisions = []
    while True:
        weights = []
        print_info("Rollout Target")
        target_revisions_result = prompt_checkbox(
            "Choose revisions to launch",
            [f"Revision {rev.number}: {rev.message}" for rev in revisions],
        )
        if len(target_revisions_result) == 0:
            print_error("Please select at least one revision.")
            continue
        target_revisions = ([
            {
                'number': int(rev_summary.split(":")[0].split(" ")[1]),
                'message': ':'.join(rev_summary.split(":")[1:]).strip()
            } for rev_summary in target_revisions_result
        ])
        target_revisions.sort(key=lambda x: x['number'])
        weights = []
        for i, revision in enumerate(target_revisions):
            if i == len(target_revisions) - 1:
                remaining_weight = 100 - sum(weights)
                print_info(f"Last revision will take the rest of the traffic.({remaining_weight}%)")
                weights.append(remaining_weight)
            else:
                while True:
                    w = prompt_text(f"How much traffic should revision {revision['number']} receive?(in percentage)")
                    if not w.isdigit():
                        print_error("Please type an integer between 0 and 100.")
                    elif int(w) > 100 or int(w) < 0:
                        print_error("Please type an integer between 0 and 100.")
                    elif sum(weights) + int(w) > 100:
                        print_error("Total weight should not exceed 100.")
                    else:
                        weights.append(int(w))
                        break

        print_table_tabulate(
            [
                {
                    "Revision Number": revision['number'],
                    "Message": revision['message'],
                    "Traffic Weight": f'{weight}%',
                } for revision, weight in zip(target_revisions, weights)
            ],
        )
        if prompt_confirm("Do you want to proceed as above?"):
            break
    update_model_service(service, [r['number'] for r in target_revisions], weights)


@cli.command("create-yaml", cls=VesslCommand, help="Create a service.yaml file with .vessl.model.lock file")
@vessl_argument("service_name", type=str)
@vessl_argument("message", type=str)
@vessl_option("-k","--api-key", "use_api_key", type=bool, is_flag=True)
def create_yaml(
    service_name: str,
    message: str,
    use_api_key: bool = False,
):
    organization_name = _get_organization_name()

    lockfile_path = ".vessl.model.lock"
    lockfile = VesslModel.from_lockfile(lockfile_path)
    if lockfile is None:
        print_error("The lockfile is not found.")
        return

    try:
        msr = vessl_api.model_service_read_api(
            organization_name=organization_name,
            model_service_name=service_name,
        )
    except Exception as e:
        if e.status == 404:
            print_error(f"Model service {service_name} not found. You should first create a service.")
            return
        print_error(f"Failed to read model service: {e}")
        return

    print_info(f"Service name of {service_name} found.")

    # clusters = list_clusters()
    # cluster_name = prompt_choices("Cluster", [x.name for x in clusters])
    # cluster = list(filter(lambda x: x.name == cluster_name, clusters))[0]
    cluster = msr.kernel_cluster
    print_info(f"Using {cluster.name} cluster configured by the service.")

    presets = list_cluster_presets(cluster.id)
    preset_name = prompt_choices("Preset", [x.name for x in presets])
    preset = list(filter(lambda x: x.name == preset_name, presets))[0]

    secret_name = None
    if use_api_key:
        print_info("Select API key for authentication.")
        secrets = list_generic_secrets()
        if len(secrets) == 0:
            print_info("No secrets registered.")
            if prompt_confirm("Do you want to create a new secret?", default=True):
                secret_name = _create_secret()
            else:
                print_error("No secret selected.")
                return
        else:
            secret_names = [x.credentials_name for x in secrets]
            secret_names.append("Create a new secret")
            secret_name = prompt_choices("Secret", secret_names)
            if secret_name == "Create a new secret":
                secret_name = _create_secret()

    service = V1ServeRevisionServiceForm(
        expose=3000,
        healthcheck=V1PortPath(path="/",port=3000),
        monitoring=[V1PortPath(path="/metrics",port=3000)],
        autoscaling=V1Autoscaling(min=1, max=2, metric="cpu", target=50),
        auxiliary=V1AuxiliaryForm(
            runner_type=_get_runner_type(lockfile.type),
        )
    ).to_dict()

    form = {
        "name":service_name,
        "message":message,
        "env":(
            None
            if use_api_key is None or secret_name is None
            else {
                "SERVICE_AUTH_KEY": V1EnvForm(
                    secret=secret_name,
                    source="secret",
                ).to_dict()
            }
        ),
        "image": _generate_image_name(lockfile),
        "resources": V1ResourcesForm(
            cluster=cluster.name,
            preset=preset.name,
        ).to_dict(),
        "import": {
            "/model": _sanitize_model_form(V1ImportForm(
                model=V1ModelRefForm(
                    organization_name=organization_name,
                    model_repository_name=lockfile.repository_name,
                    model_number=lockfile.model_number,
                )
            ))
        },
        "run": [
            V1Command(
                command=lockfile.entrypoint,
                workdir="/model/"+os.getcwd().split("/")[-1],
            ).to_dict()
        ],
        "ports": [V1PortPath(port=3000).to_dict()],
        "service":service,
    }

    with open("service.yaml", "w") as f:
        cleaned = _sanitize(form)
        b = yaml.dump(cleaned, default_flow_style=False, sort_keys=False)
        b = b.replace("_import", "import")
        f.write(b)
    
    print_success("service.yaml created.")

def _create_secret() -> str:
    secret_name = prompt_text("Secret name")
    secret_value = prompt_text("Secret value")
    resp = vessl_api.secret_upsert_generic_secret_api(
        organization_name=vessl_api.organization.name,
        secret_upsert_generic_secret_api_input=secret_upsert_generic_secret_api_input.SecretUpsertGenericSecretAPIInput(
            secret_name=secret_name,
            value=secret_value,
        )
    )
    print_info(f"Secret {resp.credentials_name} created.")
    return resp.credentials_name

def _get_runner_type(model_runner_type: str) -> str:
    if model_runner_type == "vessl" or model_runner_type == "hf-transformers" or model_runner_type == "torch":
        return "vessl"
    elif model_runner_type == "bento":
        return "bento"
    else:
        raise ValueError(f"Unsupported model runner type: {model_runner_type}")

def _sanitize(yaml_obj):
    if isinstance(yaml_obj, dict):
        cleaned = dict((k, _sanitize(v)) for k, v in yaml_obj.items() if v is not None)
        return cleaned
    elif isinstance(yaml_obj, list):
        cleaned = [_sanitize(v) for v in yaml_obj if v is not None]
        return cleaned
    else:
        return yaml_obj

def _generate_image_name(
    vesslmodel: VesslModel,
):
    if vesslmodel.framework_type == "torch":
        return VESSL_SERVICE_TORCH_BASE_IMAGE_TEMPLATE.format(
            **{
                "pytorch_version": vesslmodel.pytorch_version,
                "cuda_version": vesslmodel.cuda_version,
            }
        )
    elif vesslmodel.framework_type == "tensorflow":
        return VESSL_SERVICE_TENSORFLOW_BASE_IMAGE_TEMPLATE.format(
            **{
                "tensorflow_version": vesslmodel.tensorflow_version,
                "cuda_version": vesslmodel.cuda_version,
            }
        )
    raise ValueError("Either pytorch_version or tensorflow_version must be provided")

def _sanitize_model_form(form: V1ImportForm):
    return f"vessl-model://{form.model.organization_name}/{form.model.model_repository_name}/{form.model.model_number}"


def _check_service_name_or_prompt(
    service_name: Optional[str],
    cluster_name: str,
    serverless: bool,
    no_prompt: bool,
) -> Tuple[str, ModelServiceType]:
    """
    Verifies (or prompts the user to choose) a service name.

    Arguments:
        service_name (str | None):
            Name of service, provided either in CLI argument or embedded in YAML.

        cluster_name (str):
            Name of the cluster, hinted in YAML. This is used as when we have to
            create a service.

        serverless (bool):
            Whether user has explicitly requested the service to be in serverless mode.

        no_prmopt (bool):
            True if the user has explicitly denied prompts or interactions.

    Returns:
        str: Name of the selected Service.
        ModelServiceType: Type of the selected Service.
    """

    if service_name:
        try:
            model_service_resp: ModelserviceModelServiceReadResponse = (
                vessl_api.model_service_read_api(
                    model_service_name=service_name,
                    organization_name=vessl_api.organization.name,
                )
            )
        except VesslApiException as e:
            if e.status == 404:
                print_info(f"Service '{service_name}' not found.")
                print_info("Automatically creating one...")
                print()
                return _create_service(
                    service_name=service_name, cluster_name=cluster_name, serverless=serverless
                )
            else:  # unexpected error
                raise e

        service_type = ModelServiceType(model_service_resp.type)
        if serverless and service_type != ModelServiceType.SERVERLESS:
            print_error(
                f"Error: service '{service_name}' has type {str(service_type.value).capitalize()}, "
                "but --serverless flag was given in the command line.\n"
                "\n"
                "Please check your parameters and try again."
            )
            sys.exit(1)

        return model_service_resp.name, service_type

    else:
        service_list_resp: ModelserviceModelServiceListResponse = vessl_api.model_service_list_api(
            organization_name=vessl_api.organization.name,
        )
        service_list: List[ResponseModelServiceInfo] = service_list_resp.results
        service_display_texts = [
            f"{s.name} (status: {str(s.status).capitalize()}; type: {str(s.type).capitalize()})"
            for s in service_list
        ]

        if no_prompt:
            print_error("Error: service name is required.")
            print()
            print_info("NOTE: Available services are:")
            example_count = 5
            for txt in service_display_texts[:example_count]:
                print_info(f"    - {txt}")
            if example_count < len(service_list):
                print_info(f"    - ({len(service_list)-example_count} more...)")
            sys.exit(1)

        chosen_service: Optional[ResponseModelServiceInfo] = prompt_choices(
            "Select service, or create a new one.",
            [("(Create a new service...)", None)]
            + [(txt, s) for txt, s in zip(service_display_texts, service_list)],
        )
        if chosen_service is None:
            return _create_service(
                service_name=None,
                cluster_name=cluster_name,
                serverless=serverless,
            )
        else:
            return chosen_service.name, ModelServiceType(chosen_service.type)


def _create_service(
    service_name: Optional[str], cluster_name: str, serverless: bool
) -> Tuple[str, ModelServiceType]:
    """
    Prompts the user to help create a Service.

    Arguments:
        service_name (str | None):
            Name of the service, if known.

        cluster_name (str):
            Name of the cluster, hinted in YAML. This is used to create the service.

        serverless (bool):
            Whether to create the new service as serverless mode.
            Only present if the user explicitly provided an option for it.

    Returns:
        str: Name of the new Service.
        ModelServiceType: Type of the new Service.
    """

    if service_name is None:
        service_name = prompt_text("Name for new service")

    service_type: ModelServiceType
    service_type = ModelServiceType.SERVERLESS if serverless else ModelServiceType.PROVISIONED
    print_info(f"Creating service {service_name} in {service_type.value.capitalize()} mode.")

    # We only have the cluster's name; we need to resolve its ID.
    all_clusters = list_clusters()
    matching_cluster_list = [c for c in all_clusters if c.name == cluster_name]
    if len(matching_cluster_list) != 1:
        print_error(f"Error: cluster '{cluster_name}' not found!")
        print()
        print_error(
            "There might be a typo, or the cluster might not be connected to this organization."
        )
        print_error("Please check your cluster and try again.")
        print()
        print_info(
            f"NOTE: there are {len(all_clusters)} cluster(s) connected to this organization:"
        )
        for c in all_clusters:
            print_info(f"    - {c.name} (status: {str(c.status).capitalize()})")
        sys.exit(1)
    cluster = matching_cluster_list[0]

    try:
        vessl_api.model_service_create_api(
            organization_name=vessl_api.organization.name,
            model_service_create_api_input=ModelServiceCreateAPIInput(
                name=service_name, kernel_cluster_id=cluster.id, service_type=service_type.value
            ),
        )
    except VesslApiException as e:
        print_error("Failed to create service")
        print_error_result(e.message)
        sys.exit(1)

    print_info(f"Successfully created service: {service_name}")

    return service_name, service_type
