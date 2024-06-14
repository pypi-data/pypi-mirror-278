import json as j

import bpkio_api.models as models
import bpkio_cli.click_options as bic_options
import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.api import BroadpeakIoApi
from bpkio_api.helpers.recorder import SessionRecorder, SessionSection
from bpkio_api.models import TranscodingProfile, TranscodingProfileIn
from bpkio_cli.click_mods import ApiResourceGroup
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.exceptions import BroadpeakIoCliError
from bpkio_cli.core.response_handler import save_json, save_resource
from bpkio_cli.utils.arrays import order_by_dict_keys
from bpkio_cli.utils.editor import edit_payload
from bpkio_cli.utils.json import is_json
from bpkio_cli.writers.breadcrumbs import display_resource_info
from bpkio_cli.writers.tables import display_table

default_fields = ["id", "name", "layers"]


def get_profile_skeleton():
    return {
        "packaging": {},
        "servicetype": "offline_transcoding",
        "transcoding": {
            "jobs": [],
            "common": {},
        },
    }


def get_admin_endpoint():
    ctx = click.get_current_context()
    if ctx.obj.tenant.id == 1:
        return ctx.obj.api.transcoding_profiles
    else:
        admin_tenant = ctx.obj.tenant_provider.get_admin_tenant(fqdn=ctx.obj.api.fqdn)
        if not admin_tenant:
            raise BroadpeakIoCliError(
                "Admin tenant not found. You can only create profiles if you have admin rights"
            )
        admin_api = BroadpeakIoApi(
            tenant=admin_tenant,
            verify_ssl=CONFIG.get("verify-ssl", "bool_or_str"),
        )
        return admin_api.transcoding_profiles


def get_profile_resource(tenant=None):
    ctx = click.get_current_context()
    id = ctx.obj.resources.last()
    return ctx.obj.api.transcoding_profiles.retrieve(id, tenant_id=tenant)


def create_profile_as_admin(profile, tenant=None, upsert=False):
    if tenant:
        profile.tenantId = tenant

    # set the correct context to create the API
    endpoint = get_admin_endpoint()
    if upsert:
        return endpoint.upsert(profile=profile, if_exists="retrieve", tenant_id=tenant)
    else:
        return endpoint.create(profile=profile)


# # --- TRANSCODING PROFILES Group
@cloup.group(
    cls=ApiResourceGroup,
    aliases=["prf", "profiles", "transcoding-profile"],
    show_subcommand_aliases=True,
    resource_class=TranscodingProfile,
)
@cloup.argument(
    "profile_id",
    help=(
        "The identifier of the transcoding profile to work with. "
        "Leave empty for commands operating on a list of profiles."
    ),
)
@click.pass_obj
def profile(obj, profile_id: str):
    """Manage Transcoding Profiles"""

    @SessionRecorder.do_not_record
    def show_breadcrumb():
        if profile_id:
            # TODO - find a way of passing the target tenant (admin mode)
            profile = obj.api.transcoding_profiles.retrieve(profile_id)
            display_resource_info(profile)

    show_breadcrumb()


# --- LIST Command
@cloup.command(
    help="Retrieve a list of all Transcoding Profiles", aliases=["ls"], name="list"
)
@bic_options.list(default_fields=default_fields)
@bic_options.output_formats
@bic_options.tenant(required=False)
@click.pass_obj
def lst(
    obj: AppContext,
    list_format,
    select_fields,
    sort_fields,
    id_only,
    return_first,
    tenant,
):
    SessionRecorder.record(
        SessionSection(
            title="List of Transcoding Profiles", description="This is for a test"
        )
    )

    profiles = obj.api.transcoding_profiles.list(tenant_id=tenant)

    obj.response_handler.treat_list_resources(
        profiles,
        select_fields=select_fields,
        sort_fields=sort_fields,
        format=list_format,
        id_only=id_only,
        return_first=return_first
    )


# --- INFO Command
@cloup.command(
    help="Retrieve detailed info about a single Transcoding Profile, by its ID",
)
@click.option(
    "--content/--no-content",
    "with_content",
    is_flag=True,
    default=True,
    help="Add or hide summary information about the content of the resource",
)
@bic_options.tenant(required=False)
@click.pass_obj
def info(obj: AppContext, tenant, with_content):
    profile = get_profile_resource(tenant)

    obj.response_handler.treat_single_resource(profile)

    if with_content:
        pack = {
            k.replace("--", "").replace("=", ""): v
            for k, v in profile.json_content["packaging"].items()
        }
        display_table(pack)

        common = {
            k: click.style(v, dim=True)
            for k, v in profile.json_content["transcoding"]["common"].items()
        }
        jobs = [
            dict(common, **job) for job in profile.json_content["transcoding"]["jobs"]
        ]
        jobs = order_by_dict_keys(jobs)

        display_table(jobs)


# --- GET Command
@cloup.command(
    aliases=["retrieve", "json"],
    help="Get the JSON representation of a single Transcoding Profile "
    "or list of Transcoding Profiles",
)
@click.option(
    "-c",
    "--content",
    "content_only",
    is_flag=True,
    default=False,
    help="Extract the actual profile's JSON and pretty print it",
)
@click.option(
    "--save",
    is_flag=True,
    default=False,
    help="Save the profile payload into a JSON file",
)
@bic_options.tenant(required=False)
@click.pass_obj
def get(obj: AppContext, tenant, content_only, save):
    try:
        profile = get_profile_resource(tenant)
        profile_id = profile.id

        if content_only:
            profile = profile.json_content

        obj.response_handler.treat_single_resource(profile, format="json")

        if save:
            if content_only:
                save_json(
                    profile,
                    f"TranscodingProfileContent_{profile_id}",
                    "Profile configuration",
                )
            else:
                save_resource(profile)

    except Exception:
        profiles = obj.api.transcoding_profiles.list(tenant_id=tenant)
        if content_only:
            # TODO - Dirty code. Needs resolving, maybe at level of the SDK
            bare_profiles = []
            for profile in profiles:
                new_pro = j.loads(profile.json())
                new_pro["_expanded_content"] = profile.json_content
                bare_profiles.append(new_pro)
            profiles = bare_profiles

        obj.response_handler.treat_list_resources(
            profiles,
            format="json",
        )


# --- SEARCH Command
@cloup.command(
    help="Retrieve a list of all Transcoding Profiles that match given "
    "terms in all or selected fields"
)
@bic_options.search
@bic_options.list(default_fields=default_fields)
@bic_options.output_formats
@bic_options.tenant(required=False)
@click.pass_obj
def search(
    obj: AppContext,
    tenant,
    single_term,
    search_terms,
    search_fields,
    list_format,
    select_fields,
    sort_fields,
    id_only,
    return_first,
):
    search_def = bic_options.validate_search(single_term, search_terms, search_fields)

    profiles = obj.api.transcoding_profiles.search(filters=search_def, tenant_id=tenant)

    obj.response_handler.treat_list_resources(
        profiles,
        select_fields=select_fields,
        sort_fields=sort_fields,
        format=list_format,
        id_only=id_only,
        return_first=return_first,
    )


# --- CREATE Command
@cloup.command(help="[ADMIN] Create a Transcoding Profile")
@bic_options.tenant(required=True)
@cloup.option("--from", "from_file", type=click.File("r"), required=False, default=None)
@cloup.option("--name", type=str, required=False, default=None)
@click.pass_obj
def create(obj: AppContext, tenant: int, from_file, name: str):
    # get the content of the profile
    if from_file:
        content = j.loads(from_file.read())
    else:
        content = get_profile_skeleton()

    payload = edit_payload(content, is_json=True)
    if not is_json(payload):
        raise ValueError("The content of the profile is not valid JSON")

    if not name:
        name = prompt.text(message="Name")

    # build the profile object for creation
    tpro = TranscodingProfileIn(content=payload, name=name, tenant_id=None)

    out_profile = create_profile_as_admin(tpro, tenant)

    obj.response_handler.treat_single_resource(out_profile)


# --- UPDATE Command
@cloup.command(aliases=["put", "edit"], help="[ADMIN] Update a Transcoding Profile")
@click.option(
    "-c",
    "--content",
    "content_only",
    is_flag=True,
    default=False,
    help="Update the content of the profile, as a JSON payload",
)
@bic_options.tenant(required=True)
@click.pass_obj
def update(obj: AppContext, tenant: int, content_only: bool):
    profile = get_profile_resource(tenant)
    profile.tenantId = tenant

    if content_only:
        edited_content = edit_payload(profile.json_content, is_json=True)
        edited_profile = profile
        profile.content = edited_content
    else:
        edited_profile = edit_payload(profile, is_json=True)

    endpoint = get_admin_endpoint()
    edited_profile = endpoint.update(profile.id, edited_profile)

    click.secho(f"Resource {profile.id} updated", fg="green")
    obj.response_handler.treat_single_resource(edited_profile)


# --- DELETE Command
@cloup.command(help="[ADMIN] Delete a Transcoding Profile, by its ID")
@click.confirmation_option(
    prompt="Are you sure you want to delete this transcoding profile?"
)
@click.pass_obj
def delete(obj: AppContext):
    profile = get_profile_resource()
    endpoint = get_admin_endpoint()

    endpoint.delete(profile.id)

    # remove from cache
    obj.cache.remove(profile)

    click.secho(f"Resource {profile.id} deleted", fg="green")


# --- SELECT Commmand
@cloup.command(
    aliases=["set"],
    help="Select a specific Transcoding Profile to set the context on",
)
@click.pass_obj
def select(obj: AppContext):
    profiles = obj.api.transcoding_profiles.list()

    choices = [dict(value=s, name=f"{s.id:>8}  -  {s.name}") for s in profiles]
    resource = prompt.fuzzy(message="Select a Transcoding Profile", choices=choices)

    obj.response_handler.treat_single_resource(resource)


# --- USAGE Command
@cloup.command(help="Find all Services that use the profile")
@bic_options.list(default_fields=["id", "name", "type"])
@bic_options.output_formats
@click.pass_obj
def usage(
    obj: AppContext,
    list_format,
    select_fields,
    sort_fields,
    id_only,
    return_first,
    **kwargs,
):
    select_fields = list(select_fields)

    profile = get_profile_resource()
    id = profile.id

    services = obj.api.services.list()

    selected_services = []
    for service in services:
        svc = obj.api.services.retrieve(service.id)

        if isinstance(svc, models.VirtualChannelService):
            if svc.transcodingProfile and svc.transcodingProfile.id == id:
                selected_services.append(svc)

        if isinstance(svc, models.AdInsertionService):
            if svc.transcodingProfile and svc.transcodingProfile.id == id:
                selected_services.append(svc)

    obj.response_handler.treat_list_resources(
        selected_services,
        select_fields=select_fields,
        sort_fields=sort_fields,
        format=list_format,
        id_only=id_only,
        return_first=return_first,
    )


# ===

profile.add_section(
    cloup.Section("CRUD commands", [get, info, lst, search, create, update, delete])
)

profile.add_section(cloup.Section("Traversal commands", [select, usage]))
