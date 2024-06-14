import json

import click
from bpkio_api.models import BaseResource, ServiceIn, SourceIn
from bpkio_cli.core.resource_trail import ResourceTrail
from bpkio_cli.utils.url_builders import get_service_handler, get_source_handler


def retrieve_resource(
    id: int | str | None = None,
    endpoint_path: list = [],
):
    ctx = click.get_current_context()
    resource_context: ResourceTrail = ctx.obj.resources
    api = ctx.obj.api
    if not id:
        id = resource_context.last()
    endpoint = api.get_endpoint_from_path(endpoint_path)

    parent_id = resource_context.parent()
    if parent_id:
        resource = endpoint.retrieve(parent_id, id)
    else:
        resource = endpoint.retrieve(id)

        # Record the resource
        if ctx.obj.cache and hasattr(resource, "id"):
            ctx.obj.cache.record(resource)

    return resource


def get_api_endpoint(path: list):
    api = click.get_current_context().obj.api
    return api.get_endpoint_from_path(path)


def get_content_handler(
    resource,
    replacement_fqdn=None,
    extra_url=None,
    additional_query_params=[],
    additional_headers=[],
    subplaylist_index=None,
    user_agent=None,
    session=None,
):
    api = click.get_current_context().obj.api

    if isinstance(resource, SourceIn):
        return get_source_handler(
            resource,
            extra_url=extra_url,
            additional_query_params=additional_query_params,
            additional_headers=additional_headers,
            subplaylist_index=subplaylist_index,
            user_agent=user_agent,
        )

    if isinstance(resource, ServiceIn):
        if session:
            additional_query_params = additional_query_params + (
                f"bpkio_sessionid={session}",
            )

        return get_service_handler(
            resource,
            replacement_fqdn=replacement_fqdn,
            extra_url=extra_url,
            additional_query_params=additional_query_params,
            additional_headers=additional_headers,
            subplaylist_index=subplaylist_index,
            api=api,
            user_agent=user_agent,
        )
