import click
import cloup
from bpkio_api.models import (
    AdInsertionService,
    ContentReplacementService,
    ContentReplacementSlot,
    ServiceIn,
    VirtualChannelService,
    VirtualChannelSlot,
)
from bpkio_cli.commands.creators.ad_insertion import create_ad_insertion_service_command
from bpkio_cli.commands.creators.services import create_service_command
from bpkio_cli.commands.creators.slot_iterators import (
    clear_slots_command,
    replicate_slots_command,
)
from bpkio_cli.commands.creators.virtual_channel import (
    create_virtual_channel_service_command,
)
from bpkio_cli.commands.creators.virtual_channel_populate import (
    populate_virtual_channel_slots_command,
)
from bpkio_cli.commands.creators.virtual_channel_slot import create_slot_command
from bpkio_cli.commands.logs import create_logs_command
from bpkio_cli.commands.template_crud import create_resource_group
from bpkio_cli.commands.template_crud_slots import create_child_resource_group
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.click_helpers import retrieve_resource

default_fields = ["id", "name", "type", "serviceId", "state", "format"]


def add_services_section(cli):
    root_endpoint = "services"
    root: cloup.Group = create_resource_group(
        "service",
        resource_class=ServiceIn,
        endpoint_path=[root_endpoint],
        aliases=["svc", "services"],
        with_content_commands=["all"],
        default_fields=default_fields,
        traversal_commands=[source_commands],
        extra_commands=[
            create_service_command(),
            create_logs_command,
        ],
    )

    return cli.section(
        "Services",
        root,
        create_resource_group(
            "content-replacement",
            resource_class=ContentReplacementService,
            endpoint_path=[root_endpoint, "content_replacement"],
            aliases=["cr"],
            default_fields=default_fields,
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                clear_slots_command(),
                replicate_slots_command(),
                create_logs_command,
                add_slots_commands(
                    resource_class=ContentReplacementSlot,
                    parent_path=[root_endpoint, "content_replacement"],
                    default_fields=[
                        "id",
                        "name",
                        "relativeStartTime",
                        "relativeEndTime",
                        "duration",
                        "replacement.id",
                        "replacement.name",
                    ],
                ),
            ],
        ),
        create_resource_group(
            "ad-insertion",
            resource_class=AdInsertionService,
            endpoint_path=[root_endpoint, "ad_insertion"],
            aliases=["dai", "ssai"],
            default_fields=[
                "id",
                "name",
                "type",
                "sub_type",
                "serviceId",
                "state",
                "format",
            ],
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                create_ad_insertion_service_command(),
                create_logs_command,
            ],
        ),
        create_resource_group(
            "virtual-channel",
            resource_class=VirtualChannelService,
            endpoint_path=[root_endpoint, "virtual_channel"],
            aliases=["vc"],
            default_fields=default_fields,
            with_content_commands=["all"],
            traversal_commands=[source_commands],
            extra_commands=[
                clear_slots_command(),
                create_virtual_channel_service_command(),
                populate_virtual_channel_slots_command(),
                replicate_slots_command(),
                create_logs_command,
                add_slots_commands(
                    resource_class=VirtualChannelSlot,
                    parent_path=[root_endpoint, "virtual_channel"],
                    default_fields=[
                        "id",
                        "name",
                        "type",
                        "relativeStartTime",
                        "relativeEndTime",
                        "duration",
                        "replacement.id",
                        "replacement.name",
                        "category.id",
                        "category.name",
                    ],
                    extra_commands=[create_slot_command()],
                ),
            ],
        ),
    )


def add_slots_commands(resource_class, parent_path, default_fields, extra_commands=[]):
    return create_child_resource_group(
        "slot",
        resource_class=resource_class,
        endpoint_path=parent_path + ["slots"],
        aliases=["slots"],
        default_fields=default_fields,
        extra_commands=extra_commands,
    )


def source_commands(endpoint_path: str):
    # COMMAND: SOURCE
    @cloup.command(help="Select the main source used by the service", aliases=["src"])
    @cloup.option(
        "--id",
        "id_only",
        is_flag=True,
        default=False,
        help="Return just the ID of the source",
    )
    @click.pass_obj
    def source(obj: AppContext, id_only, **kwargs):
        resource = retrieve_resource(endpoint_path=endpoint_path)
        source = None
        if hasattr(resource, "source"):
            source = obj.api.sources.retrieve(resource.source.id)
        elif hasattr(resource, "baseLive"):
            source = obj.api.sources.retrieve(resource.baseLive.id)

        obj.response_handler.treat_single_resource(source, id_only=id_only)

    # COMMAND: ADS
    @cloup.command(
        help="Select the ad server behind the service",
        name="ad-server",
        aliases=["ads"],
    )
    @cloup.option(
        "--id",
        "id_only",
        is_flag=True,
        default=False,
        help="Return just the ID of the source",
    )
    @click.pass_obj
    def ad_server(obj: AppContext, id_only, **kwargs):
        resource = retrieve_resource(endpoint_path=endpoint_path)
        source = None
        keys = ["vodAdInsertion", "adBreakInsertion", "liveAdReplacement"]
        for k in keys:
            if hasattr(resource, k):
                o = getattr(resource, k)
                if o is not None:
                    source = obj.api.sources.retrieve(o.adServer.id)
                    obj.response_handler.treat_single_resource(source, id_only=id_only)
                    return source

        click.secho("This service has no ad server")

    # COMMAND: PROFILE
    @cloup.command(
        help="Select the ad server behind the service",
        name="transcoding-profile",
        aliases=["profile", "prf"],
    )
    @cloup.option(
        "--id",
        "id_only",
        is_flag=True,
        default=False,
        help="Return just the ID of the source",
    )
    @click.pass_obj
    def profile(obj: AppContext, id_only, **kwargs):
        resource = retrieve_resource(endpoint_path=endpoint_path)
        if (
            hasattr(resource, "transcodingProfile")
            and resource.transcodingProfile is not None
        ):
            id = resource.transcodingProfile.id
            if id is not None:
                profile = obj.api.transcoding_profiles.retrieve(id)
                obj.response_handler.treat_single_resource(profile, id_only=id_only)
                return profile

        click.secho("This service has no transcoding profile")

    return [source, ad_server, profile]
