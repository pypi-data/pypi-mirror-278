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

#
from ngcbpc.api.configuration import Configuration
from ngcbpc.api.pagination import pagination_helper
from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV
from ngcbpc.data.model.DeploymentParameters import DeploymentParameters
from ngcbpc.data.model.DeploymentParametersListResponse import (
    DeploymentParametersListResponse,
)
from ngcbpc.data.model.DeploymentUrlResponse import DeploymentUrlResponse
from ngcbpc.data.model.Response import Response
from registry.api.utils import get_environ_tag
from registry.constants import MODEL_SERVICE_URL_MAPPING

environ_tag = get_environ_tag()
env = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}.get(environ_tag)
ENDPOINT_VERSION = "v1" if Configuration().base_url == MODEL_SERVICE_URL_MAPPING[env] else "v2"


def get_deploy_url(name, csp, artifact_type, version, org, team=None):
    # ModelDeployConfigurer
    """Get the parts for starting a deployment as a list."""
    parts = [ENDPOINT_VERSION, "csps", artifact_type, "org", org]
    if team:
        parts.extend(["team", team])
    parts.extend([name, "versions", version, "deployments", csp])
    return "/".join(parts)


def get_url(name, org, artifact_type, csp=None, team=None):
    """Get the URL for CRUD operations as a list."""
    parts = [ENDPOINT_VERSION, "org", org]
    if team:
        parts.extend(["team", team])
    parts.extend([artifact_type, name, "deployments"])
    if csp:
        parts.append(csp)
    parts.append("params")
    return "/".join(parts)


def get_public_list_url(name, org, artifact_type, team=None):
    parts = [ENDPOINT_VERSION, "deploy", "csps", artifact_type, org]
    if team:
        parts.append(team)
    parts.extend([name, "deployments", "params"])
    return "/".join(parts)


class DeployAPI:
    def __init__(self, connection):
        self.connection = connection

    def start(self, name, csp, deployment_request, artifact_type, version, org, team=None):
        """Retrieve deployment URL for an artifact."""
        endpoint = get_deploy_url(name, csp, artifact_type, version, org, team=team)
        payload = deployment_request.toJSON()
        response = self.connection.make_api_request(
            "POST",
            endpoint,
            payload=payload,
            auth_org=org,
            auth_team=team,
            operation_name="post image deploy url",
        )
        return DeploymentUrlResponse(response)

    def create(self, org, name, artifact_type, csp, create_request, team=None):
        """Create default deployment parameter set for a particular artifact."""
        endpoint = get_url(name, org, artifact_type, csp, team=team)
        payload = create_request.toJSON()
        response = self.connection.make_api_request(
            "POST",
            endpoint,
            payload=payload,
            auth_org=org,
            auth_team=team,
            operation_name="post artifact deploy create",
        )
        return DeploymentParameters(response)

    def remove(self, org, name, artifact_type, csp, team=None):
        """Remove a default deployment set for an artifact."""
        endpoint = get_url(name, org, artifact_type, csp=csp, team=team)
        response = self.connection.make_api_request(
            "DELETE", endpoint, auth_org=org, auth_team=team, operation_name="delete artifact deploy remove"
        )
        return Response(response)

    def info(self, org, name, artifact_type, csp, team=None, inherit=True):
        """GET the default deployment parameters for an artifact."""
        endpoint = get_url(name, org, artifact_type, csp=csp, team=team)
        response = self.connection.make_api_request(
            "GET",
            endpoint,
            params={"inherit-csp-parameters": inherit},
            auth_org=org,
            auth_team=team,
            operation_name="get artifact deploy info",
        )
        return DeploymentParameters(response)

    def update(self, org, name, artifact_type, csp, update_request, team=None):
        """Update default deployment parameter set for a particular artifact."""
        endpoint = get_url(name, org, artifact_type, csp, team=team)
        payload = update_request.toJSON()
        response = self.connection.make_api_request(
            "PATCH",
            endpoint,
            payload=payload,
            auth_org=org,
            auth_team=team,
            operation_name="patch artifact deploy update",
        )
        return DeploymentParameters(response)

    def list(self, org, name, artifact_type, team=None):
        """GET a list of available CSP deployments for an artifact."""
        url_base = get_public_list_url(name, org, artifact_type, team=team)
        endpoint = f"{url_base}?"  # Hack for pagination
        for page in pagination_helper(
            self.connection, endpoint, org_name=org, team_name=team, operation_name="get artifact deploy list"
        ):
            yield DeploymentParametersListResponse(page)
