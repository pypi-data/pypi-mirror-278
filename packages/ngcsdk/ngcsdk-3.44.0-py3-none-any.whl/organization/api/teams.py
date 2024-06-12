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

from typing import Optional

from ngcbpc.api.pagination import pagination_helper
from ngcbpc.constants import API_VERSION, PAGE_SIZE
from ngcbpc.data.api.TeamCreateRequest import TeamCreateRequest
from ngcbpc.data.api.TeamCreateResponse import TeamCreateResponse
from ngcbpc.data.api.TeamListResponse import TeamListResponse
from ngcbpc.data.api.TeamResponse import TeamResponse
from ngcbpc.data.api.TeamUpdateRequest import TeamUpdateRequest
from ngcbpc.util.utils import extra_args


class TeamAPI:
    def __init__(self, connection):
        self.connection = connection

    def get_teams(self, org_name: str):
        """Get list of teams from an org."""
        query = f"{API_VERSION}/org/{org_name}/teams?page-size={PAGE_SIZE}"
        return self._helper_get_teams(query, org_name=org_name)

    @extra_args
    def list(self, org: Optional[str] = None):
        """Get list of teams from an org."""
        self.connection.configuration.validate_configuration(csv_allowed=True)
        org_name = org or self.connection.configuration.org_name
        return self.get_teams(org_name=org_name)

    def get_team_details(self, name: str, org_name: str):
        """Get details of a given team name."""
        response = self.connection.make_api_request(
            "GET",
            f"{API_VERSION}/org/{org_name}/teams/{name}",
            auth_org=org_name,
            auth_team=name,
            operation_name="get team details",
        )
        return TeamResponse(response).team

    @extra_args
    def info(self, name: str, org: Optional[str] = None):
        """Get details of a given team name."""
        self.connection.configuration.validate_configuration()
        org_name = org or self.connection.configuration.org_name
        return self.get_team_details(name=name, org_name=org_name)

    def create_team(self, name: str, description: str, org_name: str):
        """Creates a team in an organization."""
        team_create_request = TeamCreateRequest()
        team_create_request.name = name
        team_create_request.description = description
        response = self.connection.make_api_request(
            "POST",
            f"{API_VERSION}/org/{org_name}/teams",
            payload=team_create_request.toJSON(False),
            auth_org=org_name,
            operation_name="create team",
        )
        return TeamCreateResponse(response).team

    @extra_args
    def create(self, name: str, description: str, org: Optional[str] = None):
        """Creates a team in an organization."""
        self.connection.configuration.validate_configuration()
        org_name = org or self.connection.configuration.org_name
        return self.create_team(name=name, description=description, org_name=org_name)

    def update_team_info(self, name: str, description: str, org_name: str):
        """Updates team information in an organization."""
        team_update_request = TeamUpdateRequest()
        team_update_request.description = description
        response = self.connection.make_api_request(
            "PATCH",
            f"{API_VERSION}/org/{org_name}/teams/{name}",
            payload=team_update_request.toJSON(False),
            auth_org=org_name,
            auth_team=name,
            operation_name="update team info",
        )
        # todo: return team object when API is updated
        return response

    @extra_args
    def update(self, name: str, description: str, org: Optional[str] = None):
        """Updates team information in an organization."""
        self.connection.configuration.validate_configuration()
        org_name = org or self.connection.configuration.org_name
        return self.update_team_info(name=name, description=description, org_name=org_name)

    def remove_team(self, name: str, org_name: str):
        """Removes a team from an organization."""
        response = self.connection.make_api_request(
            "DELETE",
            f"{API_VERSION}/org/{org_name}/teams/{name}",
            auth_org=org_name,
            auth_team=name,
            operation_name="remove team",
        )
        return response

    @extra_args
    def remove(self, name: str, org: Optional[str] = None):
        """Removes a team from an organization."""
        self.connection.configuration.validate_configuration()
        org_name = org or self.connection.configuration.org_name
        return self.remove_team(name=name, org_name=org_name)

    def _helper_get_teams(self, query, org_name=None):
        """Helper command to get list of all the teams using pagination."""
        teams_list_pages = pagination_helper(self.connection, query, org_name=org_name, operation_name="get teams")
        list_of_teams = []
        for page in teams_list_pages:
            list_of_teams.extend(TeamListResponse(page).teams)
        return list_of_teams
