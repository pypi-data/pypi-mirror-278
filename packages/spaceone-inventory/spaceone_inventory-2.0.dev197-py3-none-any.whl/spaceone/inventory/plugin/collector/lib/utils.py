import logging

from spaceone.core.error import *
from spaceone.core import utils
from spaceone.inventory.plugin.collector.error.response import (
    ERROR_NOT_SUPPORTED_RESOURCE_TYPE,
    ERROR_REQUIRED_PARAMETER_FOR_RESOURCE_TYPE,
)
from spaceone.inventory.plugin.collector.model import (
    CloudService,
    CloudServiceType,
    Reference,
)
from spaceone.inventory.plugin.collector.lib.metadata import (
    convert_cloud_service_type_meta,
    convert_cloud_service_meta,
)

_LOGGER = logging.getLogger(__name__)


def make_cloud_service_type(
    name,
    group,
    provider,
    metadata_path,
    is_primary=False,
    is_major=False,
    service_code=None,
    tags=None,
    labels=None,
) -> dict:
    if tags is None:
        tags = {}
    if labels is None:
        labels = []

    cloud_service_type = CloudServiceType(
        name=name,
        group=group,
        provider=provider,
        json_metadata=utils.dump_json(
            convert_cloud_service_type_meta(metadata_path), 4
        ),
        is_primary=is_primary,
        is_major=is_major,
        service_code=service_code,
        tags=tags,
        labels=labels,
    )

    return cloud_service_type.dict()


def make_cloud_service(
    name: str,
    cloud_service_type: str,
    cloud_service_group: str,
    provider: str,
    data: dict,
    ip_addresses: list = None,
    account: str = None,
    instance_type: str = None,
    instance_size: float = None,
    region_code: str = None,
    reference: Reference = None,
    tags: dict = None,
) -> dict:
    if ip_addresses is None:
        ip_addresses = []
    if instance_size is None:
        instance_size = 0
    if tags is None:
        tags = {}

    cloud_service = CloudService(
        name=name,
        cloud_service_type=cloud_service_type,
        cloud_service_group=cloud_service_group,
        provider=provider,
        json_data=utils.dump_json(data, 4),
        json_metadata=utils.dump_json(
            convert_cloud_service_meta(
                provider, cloud_service_group, cloud_service_type
            ),
            4,
        ),
        ip_addresses=ip_addresses,
        account=account,
        instance_type=instance_type,
        instance_size=instance_size,
        region_code=region_code,
        reference=reference,
        tags=tags,
    )

    return cloud_service.dict()


def make_response(
    match_keys: list,
    cloud_service_type: dict = None,
    cloud_service: dict = None,
    region: dict = None,
    metric: dict = None,
    namespace: dict = None,
    resource_type: str = "inventory.CloudService",
) -> dict:
    response = {
        "state": "SUCCESS",
        "resource_type": resource_type,
        "match_keys": match_keys,
    }

    if resource_type == "inventory.CloudServiceType":
        if cloud_service_type is not None:
            response["cloud_service_type"] = cloud_service_type
            return response
        else:
            raise ERROR_REQUIRED_PARAMETER_FOR_RESOURCE_TYPE(
                resource_type=resource_type, key="cloud_service_type"
            )
    elif resource_type == "inventory.CloudService":
        if cloud_service is not None:
            response["cloud_service"] = cloud_service
            return response
        else:
            raise ERROR_REQUIRED_PARAMETER_FOR_RESOURCE_TYPE(
                resource_type=resource_type, key="cloud_service"
            )
    elif resource_type == "inventory.Region":
        if region is not None:
            response["region"] = region
            return response
        else:
            raise ERROR_REQUIRED_PARAMETER_FOR_RESOURCE_TYPE(
                resource_type=resource_type, key="region"
            )
    elif resource_type == "inventory.Metric":
        if metric is not None:
            response["metric"] = metric
            return response
        else:
            raise ERROR_REQUIRED_PARAMETER_FOR_RESOURCE_TYPE(
                resource_type=resource_type, key="metric"
            )
    elif resource_type == "inventory.Namespace":
        if namespace is not None:
            response["namespace"] = namespace
            return response
        else:
            raise ERROR_REQUIRED_PARAMETER_FOR_RESOURCE_TYPE(
                resource_type=resource_type, key="namespace"
            )
    else:
        raise ERROR_NOT_SUPPORTED_RESOURCE_TYPE(resource_type=resource_type)


def make_error_response(
    error: Exception,
    provider: str,
    cloud_service_group: str,
    cloud_service_type: str,
    resource_type: str = "inventory.CloudService",
    region_name: str = "",
) -> dict:
    if isinstance(error, ERROR_BASE):
        error_message = error.message
    else:
        error_message = str(error)

    _LOGGER.error(
        f"[make_error_response] {provider}.{cloud_service_group}.{cloud_service_type}: {error_message}",
        exc_info=True,
    )
    return {
        "state": "FAILURE",
        "resource_type": "inventory.ErrorResource",
        "error_message": error_message,
        "error_data": {
            "provider": provider,
            "cloud_service_group": cloud_service_group,
            "cloud_service_type": cloud_service_type,
            "resource_type": resource_type,
        },
    }
