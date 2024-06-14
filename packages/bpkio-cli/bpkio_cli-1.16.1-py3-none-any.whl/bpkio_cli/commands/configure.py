import json
import re
import uuid

import bpkio_cli.click_options as bic_options
import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_api.api import DEFAULT_FQDN, BroadpeakIoApi
from bpkio_api.credential_provider import TenantProfileProvider
from bpkio_cli.click_mods.option_eat_all import OptionEatAll
from bpkio_cli.commands.hello import hello
from bpkio_cli.commands.logs import get_available_pages
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.initialize import initialize
from bpkio_cli.core.response_handler import ResponseHandler
from bpkio_cli.writers.players import StreamPlayer


# Command: INIT
# To be attached to the root group
@cloup.command(help="Initialize the tool, and create a first tenant profile")
@click.pass_context
def init(ctx):
    cp = TenantProfileProvider()

    if not cp.has_default_tenant():
        ctx.invoke(add)

    click.secho("All done!  You're ready to go now", fg="yellow")


# Group: CONFIG
@cloup.group(
    aliases=["config", "cfg"],
    help="Configure how the CLI works",
    show_subcommand_aliases=True,
)  # type: ignore
@click.pass_obj
def configure(obj):
    pass


# Command: SET
@configure.command(help="Set a configuration option")
@click.argument("key", required=True)
@click.argument("value", required=True)
def set(key, value):
    if "." in key:
        key_parts = key.split(".")
        section = key_parts[0]
        key = ".".join(key_parts[1:])
        CONFIG.set_config(key, value, section=section)
    else:
        CONFIG.set_config(key, value)


# Command: EDIT
@configure.command(help="Edit the config file")
def edit():
    config_file = CONFIG.config_path
    click.edit(filename=str(config_file), editor=CONFIG.get("editor"))


# Sub-Group: TENANTS
@configure.group(
    aliases=["tenant", "tnt"],
    help="Define CLI credential profiles to be able to easily switch tenant",
)
@click.pass_obj
def tenants(obj):
    pass


# Command: LIST
@tenants.command(help="List the tenants previously configured", aliases=["ls"])
@bic_options.output_formats
@click.option(
    "-s",
    "--sort",
    "sort_fields",
    cls=OptionEatAll,
    type=tuple,
    help="List of fields used to sort the list. Append ':desc' to sort in descending order",
)
@click.option(
    "--labels",
    "labels_only",
    is_flag=True,
    type=bool,
    default=False,
    help="Return the labels only, 1 per line. This can be useful for piping to other tools",
)
def list(sort_fields, labels_only, list_format):
    cp = TenantProfileProvider()
    tenants = cp.list_tenants()
    if labels_only:
        tenants = [t.label for t in tenants]
        click.echo("\n".join(tenants))
    else:
        ResponseHandler().treat_list_resources(
            resources=tenants,
            select_fields=["label", "id", "fqdn"],
            sort_fields=sort_fields,
            format=list_format,
        )


# Command: SWITCH
@tenants.command(help="Switch the tenant used for subsequent invocations")
@click.argument("tenant", required=False, metavar="<tenant-label>")
@click.pass_context
def switch(ctx, tenant):
    if not tenant:
        cp = TenantProfileProvider()
        tenant_list = cp.list_tenants()
        tenant_list = sorted(tenant_list, key=lambda t: t.label)
        choices = [
            dict(value=t.label, name=f"{t.label} ({t.id})  -  {t.fqdn}")
            for t in tenant_list
        ]

        tenant = prompt.fuzzy(message="Select a tenant", choices=choices)

    # Reinitialize the app context
    ctx.obj = initialize(tenant=tenant, requires_api=True)

    # Write it to the .tenant file
    TenantProfileProvider().store_tenant_label_in_working_directory(tenant)

    # show tenant info to the user for validation
    ctx.invoke(hello)


# Command: ADD
@tenants.command(help="Store credentials for a new tenant")
@click.argument("label", required=False)
@click.pass_context
def add(ctx, label):
    cp = TenantProfileProvider()
    verify_ssl = CONFIG.get("verify-ssl", "bool_or_str")

    api_key = prompt.secret(
        message="API Key for the Tenant",
        long_instruction="Get your API key from the broadpeak.io webapp",
        validate=lambda candidate: BroadpeakIoApi.is_valid_api_key_format(candidate),
        invalid_message="Invalid API Key",
    )
    fqdn = prompt.text(
        message="Domain name for the API endpoints",
        default=DEFAULT_FQDN,
        long_instruction="You can also paste the URL to the webapp, if you don't know the API endpoint",
        validate=lambda url: BroadpeakIoApi.is_correct_entrypoint(
            url, api_key, verify_ssl=verify_ssl
        ),
        filter=lambda url: BroadpeakIoApi.normalise_fqdn(url),
        invalid_message=(
            "This URL does not appear to be a broadpeak.io application, "
            "or your API key does not give you access to it"
        ),
    )

    # Test the API key by initialising the API with it
    bpk_api = BroadpeakIoApi(api_key=api_key, fqdn=fqdn, verify_ssl=verify_ssl)

    # Parse the API
    tenant = bpk_api.get_self_tenant()
    tenant_id = tenant.id

    default_name = label or tenant.name
    default_name = re.sub(r"[^a-zA-Z0-9-_]", "_", default_name)
    # If there is no default profile yet, suggest that one instead
    if not cp.has_default_tenant():
        default_name = "default"

    key = prompt.text(
        message="Profile label",
        default=default_name,
        long_instruction="This label will be used to identify the tenant in the future. Make it short, easy and memorable.",
        validate=lambda s: bool(re.match(r"^[a-zA-Z0-9_-]*$", s)),
        invalid_message="Please only use alphanumerical characters",
    )

    # Create a dict
    config = {"api_key": api_key, "id": tenant.id}

    if fqdn != DEFAULT_FQDN:
        config["fqdn"] = fqdn

    cp.add_tenant(key, config)

    click.echo(
        f'A profile named "{key}" for tenant {tenant_id} has been added to {cp.inifile}'
    )

    if key != "default":
        click.echo(
            f"You can now simply use `bic --tenant {key} COMMAND` to work within that tenant's account"
        )
    else:
        click.echo(
            "You can now simply use `bic COMMAND` to work within that tenant's account"
        )

    do_switch = prompt.confirm(
        message="Do you want to switch to this tenant now?", default=True
    )

    if do_switch:
        ctx.invoke(switch, tenant=key)


# Command: INFO
@tenants.command(help="Show information about a tenant")
@click.argument("tenant_label", required=False)
def info(tenant_label):
    cp = TenantProfileProvider()

    if not tenant_label:
        tenant_label = cp.get_tenant_label_from_working_directory()
    if not cp.has_tenant_label(tenant_label):
        raise click.ClickException(f"Tenant '{tenant_label}' not found")
    tenant = cp.get_tenant_profile(tenant_label=tenant_label)

    for k, v in dict(tenant).items():
        click.echo(f"{k} = {v}")


# Command: EDIT
@tenants.command(help="Edit the tenant credential file manually")
def edit():
    cp = TenantProfileProvider()

    click.edit(filename=str(cp.inifile), editor=CONFIG.get("editor"))


# Command: PASSWORD
@tenants.command(help="Retrieve or change the API key for the current tenant")
@click.argument("tenant_label", required=False)
@click.argument("new_password", required=False)
def password(tenant_label, new_password):
    cp = TenantProfileProvider()

    if not tenant_label:
        tenant_label = cp.get_tenant_label_from_working_directory()

    if not cp.has_tenant_label(tenant_label):
        raise click.ClickException(f"Tenant '{tenant_label}' not found")
    tenant = cp.get_tenant_profile(tenant_label=tenant_label)

    if new_password:
        cp.replace_tenant_password(key=tenant_label, password=new_password)
    else:
        # click.echo(f"API Key for tenant `{tenant_label}`: ", nl=False)
        click.echo(tenant.api_key)


# Command: POSTMAN
@tenants.command(help="Export as Postman environment")
@click.argument("tenant_label", required=False)
def postman(tenant_label):
    cp = TenantProfileProvider()

    if not tenant_label:
        tenant_label = cp.get_tenant_label_from_working_directory()

    if not cp.has_tenant_label(tenant_label):
        raise click.ClickException(f"Tenant '{tenant_label}' not found")
    tenant = cp.get_tenant_profile(tenant_label=tenant_label)

    keys = [
        {
            "key": "API_TOKEN",
            "value": tenant.api_key,
            "type": "secret",
            "enabled": True,
        },
        {
            "key": "API_ROOT",
            "value": f"{tenant.fqdn}/v1",
            "type": "default",
            "enabled": True,
        },
        {
            "key": "API_FQDN",
            "value": tenant.fqdn,
            "type": "default",
            "enabled": True,
        },
        {
            "key": "TENANT_ID",
            "value": tenant.id,
            "type": "default",
            "enabled": True,
        },
    ]

    env = dict(
        id=str(uuid.uuid4()), name=f"bpk.io tenant - {tenant_label}", values=keys
    )

    with open(f"{tenant_label}.postman_environment.json", "w") as f:
        json.dump(env, f, indent=4)

    click.secho(
        f"Environment file saved to {tenant_label}.postman_environment.json", fg="green"
    )


# Sub-Group: PLAYERS
@configure.group(
    help="Management of player configurations",
    aliases=["player", "pl"],
)
@click.pass_obj
def players(obj):
    pass


# Command: LIST
@players.command(help="List the players already configured", aliases=["ls"])
@bic_options.output_formats
@click.option(
    "-s",
    "--sort",
    "sort_fields",
    cls=OptionEatAll,
    type=tuple,
    help="List of fields used to sort the list. Append ':desc' to sort in descending order",
)
@click.option(
    "--labels",
    "labels_only",
    is_flag=True,
    type=bool,
    default=False,
    help="Return the labels only, 1 per line. This can be useful for piping to other tools",
)
def list(sort_fields, labels_only, list_format):
    pl = StreamPlayer()
    ppl = pl.available_player_templates()
    if labels_only:
        ppl = [p for p in ppl.keys()]
        click.echo("\n".join(ppl))
    else:
        ppl = [v for k, v in ppl.items()]
        ResponseHandler().treat_list_resources(
            resources=ppl,
            # select_fields=["label", "id", "fqdn"],
            sort_fields=sort_fields,
            format=list_format,
        )


# Sub-Group: LOGS
@configure.group(
    name="log-pages",
    help="Management of log page configurations",
    aliases=["log-page"],
)
@click.pass_obj
def log_pages(obj):
    pass


# Command: LIST
@log_pages.command(help="List the log pages already configured", aliases=["ls"])
@bic_options.output_formats
@click.option(
    "-s",
    "--sort",
    "sort_fields",
    cls=OptionEatAll,
    type=tuple,
    help="List of fields used to sort the list. Append ':desc' to sort in descending order",
)
@click.option(
    "--labels",
    "labels_only",
    is_flag=True,
    type=bool,
    default=False,
    help="Return the labels only, 1 per line. This can be useful for piping to other tools",
)
def list(sort_fields, labels_only, list_format):
    ppl = get_available_pages(CONFIG)
    if labels_only:
        ppl = [p for p in ppl.keys()]
        click.echo("\n".join(ppl))
    else:
        ppl = [v for k, v in ppl.items()]
        ResponseHandler().treat_list_resources(
            resources=ppl,
            # select_fields=["label", "id", "fqdn"],
            sort_fields=sort_fields,
            format=list_format,
        )
