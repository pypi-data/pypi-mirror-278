import builtins

import bpkio_cli.utils.prompt as prompt
import click
import cloup
from bpkio_cli.core.app_context import AppContext
from bpkio_cli.core.click_helpers import retrieve_resource
from bpkio_cli.core.config_provider import ConfigProvider


def create_logs_command(endpoint_path, **kwargs):
    # COMMAND
    @cloup.group(help="Retrieve logs for a service")
    def logs():
        pass

    # COMMAND: OPEN
    @logs.command(help="Open the datadog logs for the given service", aliases=["log"])
    @click.option(
        "-p",
        "--page",
        default="CHOICE",
        help="The specific datadog page to open",
        type=str,
        is_flag=False,
        flag_value="CHOICE",
        metavar="<log-page-label>"
    )
    @click.pass_obj
    def open(obj: AppContext, page: str):
        resource = retrieve_resource(endpoint_path=endpoint_path)

        # pass a set of useful parameters for placeholder replacement
        # in the URL (and page name)
        params = resource.get_all_fields_and_properties()

        # Read the first line from the .last_session file (if it exists)
        # and add it as a parameter "sessionId"
        try:
            with builtins.open(".last_session", "r") as f:
                params["sessionId"] = f.readline().strip()
        except FileNotFoundError:
            pass

        # Determine what page to open
        pages = get_available_pages(obj.config, **params)

        if page not in pages:
            if page != "CHOICE":
                click.secho(f"No page '{page}' in the config", fg="red")

            page = prompt_for_page(pages)

        # go and find the URL for it
        url = pages[page]["url"]

        open_page(url, **params)

    return logs


def get_available_pages(config_provider: ConfigProvider, **kwargs):
    log_pages = config_provider.get_section_items("logs")
    output = {}
    
    for k, v in log_pages.items():
        (desc, url) = v.split("||")
        if kwargs:
            output[k] = dict(name=k, label=desc.format(**kwargs), url=url)
        else:
            output[k] = dict(name=k, label=desc, url=url)
    return output


def prompt_for_page(pages):
    player = prompt.fuzzy(
        message="What log page do you want to open?",
        choices=[dict(name=f"{k:<12}  -  {v['label']}", value=k) for k, v in pages.items()],
    )
    return player


def open_page(page_url: str, **kwargs):
    try:
        full_url = page_url.format(**kwargs)
    except KeyError as e:
        key = str(e).strip("'")
        if ":" in key:
            key, default = key.split(":", 1)
            kwargs[key] = default
            full_url = page_url.format(**kwargs)
        else:
            raise ValueError(f"No value provided for the placeholder '{key}'.")

    click.launch(full_url)
