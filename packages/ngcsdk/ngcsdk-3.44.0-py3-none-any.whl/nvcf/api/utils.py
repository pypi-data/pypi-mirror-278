#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#


from nvcf.constants import NVCF_GRPC_URL_MAPPING, NVCF_URL_MAPPING

from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV
from ngcbpc.errors import ResourceNotFoundException
from ngcbpc.util.utils import get_environ_tag
from registry.api.utils import (
    ChartRegistryTarget,
    get_chart_url,
    get_nvcr_relative_url,
    ImageRegistryTarget,
    ModelRegistryTarget,
)

env_mapping = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}


def get_nvcf_url_per_environment() -> str:
    """Return the appropriate URL for NVCF direct calls"""
    tag = get_environ_tag()
    env = env_mapping.get(tag)
    return NVCF_URL_MAPPING[env]


def get_nvcf_grpc_url_per_environment() -> str:
    """Return the appropriate grpc URL for NVCF grpc calls"""
    tag = get_environ_tag()
    env = env_mapping.get(tag)
    return NVCF_GRPC_URL_MAPPING[env]


def validate_transform_image(client, container_image: str) -> str:
    try:
        ImageRegistryTarget(container_image, org_required=True, tag_required=True)
        client.registry.image.info(container_image)
    except ResourceNotFoundException as e:
        raise ResourceNotFoundException(
            f"Container Image {container_image} not found in nvcr, use ngc registry image info"
            f" {container_image} to validate image information"
        ) from e

    # Prepend NVCR.io if not included
    if "nvcr.io/" not in container_image:
        image_repo_url = get_nvcr_relative_url()
        container_image = f"{image_repo_url}/{container_image}"

    return container_image


def validate_transform_model(client, model: str) -> dict:
    mrt = ModelRegistryTarget(model, version_required=True)
    client.registry.model.info(model)

    model_uri = (
        f"/v2/org/{mrt.org}/team/{mrt.team}/models/{mrt.name}/{mrt.version}/files"
        if mrt.team
        else f"/v2/org/{mrt.org}/models/{mrt.name}/{mrt.version}/files"
    )

    return {"name": mrt.name, "version": mrt.version, "uri": model_uri}


def validate_transform_helm_chart(client, helm_chart: str) -> str:
    ChartRegistryTarget(helm_chart, version_required=True)
    client.registry.chart.info_chart_version(helm_chart)

    chart_url = get_chart_url()
    helm_chart = f"{chart_url}/{helm_chart}"

    return helm_chart


def validate_transform_resource(client, resource: str) -> dict:
    mrt = ModelRegistryTarget(resource, version_required=True)
    client.registry.resource.info(resource)

    model_uri = (
        f"/v2/org/{mrt.org}/team/{mrt.team}/resources/{mrt.name}/{mrt.version}/files"
        if mrt.team
        else f"/v2/org/{mrt.org}/resources/{mrt.name}/{mrt.version}/files"
    )

    return {"name": mrt.name, "version": mrt.version, "uri": model_uri}
