#
# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

import logging

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV
from ngcbpc.data.model.AIPlaygroundResponse import AIPlaygroundResponse
from ngcbpc.errors import ResourceNotFoundException
from ngcbpc.util.utils import extra_args, format_org_team
from registry.api.utils import get_environ_tag, ModelRegistryTarget
from registry.constants import MODEL_SERVICE_URL_MAPPING

logger = logging.getLogger(__name__)

environ_tag = get_environ_tag()
env = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}.get(environ_tag)
ENDPOINT_VERSION = "v1" if Configuration().base_url == MODEL_SERVICE_URL_MAPPING[env] else "v2"


class PlaygroundAPI:
    """Playground can be considered as a subresource of model"""

    def __init__(self, connection: Connection, api_client=None):
        self.config = Configuration()
        self.connection = connection
        self.api_client = api_client

    # PUBLIC FUNCTIONS

    @extra_args
    def info(self, target: str) -> AIPlaygroundResponse:
        """Retrieve info for a playground. assume org[/team]/name, guest mode is allowed,
        guest mode determined in configuration"""

        self.config.validate_configuration(guest_mode_allowed=True)
        mrt = ModelRegistryTarget(target, org_required=False, name_required=True)
        return self._get_playground_info(org=mrt.org, team=mrt.team, name=mrt.name)

    # END PUBLIC Functions

    def _get_playground_info(self, org: str = None, team: str = None, name: str = None) -> AIPlaygroundResponse:
        """make request to get playground info"""

        try:
            # endpoint is different for guest mode, guest mode determined by self.config
            if self.config.is_guest_mode:
                endpoint = GuestPlaygroundAPI.get_playground_endpoint(org=org, team=team, name=name)
            else:
                endpoint = self.get_playground_endpoint(org=org, team=team, name=name)
            logger.debug("endpoint used for playground info is: %s", endpoint)

            resp = self.connection.make_api_request(
                "GET",
                endpoint,
                auth_org=org,
                auth_team=team,
                operation_name="get playground info",
            )
            return AIPlaygroundResponse(resp)
        except ResourceNotFoundException as e:
            _target = "/".join([i for i in [org, team, name] if i])
            raise ResourceNotFoundException(f"Target '{_target}' could not be found.") from e

    @staticmethod
    def get_playground_endpoint(org: str = None, team: str = None, name: str = None) -> str:
        """Create a playground model endpoint.
        /v2[/org/<org>[/team/<team>]]/models/playground/<name>
        """

        # /v2[/org/<org>[/team/<team>]]/models/playground/<name>
        parts = [ENDPOINT_VERSION, format_org_team(org, team), "models/playground", name]
        return "/".join([part for part in parts if part])


class GuestPlaygroundAPI(PlaygroundAPI):
    @staticmethod
    def get_playground_endpoint(org: str = None, team: str = None, name: str = None) -> str:
        """Guest mode playground endpoint is different:
        /v2[/org/<org>[/team/<team>]]/models/<model name>/playground
        """

        # /v2[/org/<org>[/team/<team>]]/models/<model name>/playground
        parts = [ENDPOINT_VERSION, "models", org, team, name, "playground"]
        return "/".join([part for part in parts if part])
