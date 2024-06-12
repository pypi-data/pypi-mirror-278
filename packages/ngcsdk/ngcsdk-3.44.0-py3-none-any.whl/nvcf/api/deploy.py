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

from datetime import datetime, timedelta
import json
from typing import Any, Iterator, Optional

from nvcf.api.deployment_spec import DeploymentSpecification

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.api.utils import DotDict
from ngcbpc.errors import NgcException, ResourceNotFoundException
from ngcbpc.util.datetime_utils import calculate_date_range, dhms_to_isoduration
from ngcbpc.util.utils import extra_args


class DeployAPI:
    def __init__(self, connection: Connection, api_client=None) -> None:
        self.connection = connection
        self.client = api_client
        self.config = Configuration()

    @staticmethod
    def _construct_deploy_ep(
        org_name: str,
        team_name: Optional[str] = None,
        function_id: Optional[str] = None,
        function_version_id: Optional[str] = None,
    ):
        ep: str = f"v2/orgs/{org_name}"
        if team_name:
            ep += f"/teams/{team_name}"
        ep += "/nvcf"
        if function_id and function_version_id:
            ep += f"/deployments/functions/{function_id}/versions/{function_version_id}"
        return ep

    @staticmethod
    def _construct_logs_ep(
        org_name: str,
        function_id: Optional[str] = None,
        team_name: Optional[str] = None,
        function_version_id: Optional[str] = None,
        job_id: Optional[str] = None,
    ) -> str:
        ep: str = f"v2/orgs/{org_name}"
        if team_name:
            ep += f"/teams/{team_name}"
        ep += "/nvcf/logs"

        if job_id:
            ep += f"/{job_id}"
            return ep

        ep += f"/functions/{function_id}"
        if function_version_id:
            ep += f"/versions/{function_version_id}"
        return ep

    @extra_args
    def info(self, function_id: str, function_version_id: str) -> DotDict:
        """Get information about a given function's deployment"""
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_deploy_ep(org_name, team_name, function_id, function_version_id)
        response = self.connection.make_api_request(
            "GET", url, auth_org=org_name, auth_team=team_name, operation_name="get deployment"
        )
        return DotDict(response)

    @extra_args
    def delete(self, function_id: str, function_version_id: str):
        """Delete a given deployment"""
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_deploy_ep(org_name, team_name, function_id, function_version_id)
        return self.connection.make_api_request(
            "DELETE", url, auth_org=org_name, auth_team=team_name, operation_name="delete deployment"
        )

    @extra_args
    def update(
        self,
        function_id: str,
        function_version_id: str,
        deployment_specifications: list[DeploymentSpecification],
    ) -> DotDict:
        """Update a given deployment"""
        self.config.validate_configuration()
        org_name = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_deploy_ep(org_name, team_name, function_id, function_version_id)

        # make request
        dep_specs = [{key: val for key, val in vars(dep_spec).items() if val} for dep_spec in deployment_specifications]
        payload: dict[str, Any] = {"deploymentSpecifications": dep_specs}

        payload = {key: val for key, val in payload.items() if val}

        response = self.connection.make_api_request(
            "PUT",
            url,
            payload=json.dumps(payload),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="update deployment",
        )
        return DotDict(response)

    @extra_args
    def create(
        self,
        function_id: str,
        function_version_id: str,
        deployment_specifications: list[DeploymentSpecification],
    ) -> DotDict:
        """Create a deployment with a function id, version and a set of available deployment specifications"""
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_deploy_ep(org_name, team_name, function_id, function_version_id)

        # Check if function exists
        try:
            self.client.cloud_function.functions.info(function_id, function_version_id)
        except ResourceNotFoundException as e:
            raise NgcException(f"Function {function_id}:{function_version_id} doesn't exist") from e

        # Check if function deployment already exists
        try:
            self.info(function_id, function_version_id)
            raise NgcException("This function already has a deployment")
        except ResourceNotFoundException:
            pass

        # make request
        dep_specs = [{key: val for key, val in vars(dep_spec).items() if val} for dep_spec in deployment_specifications]
        payload: dict[str, str] = {"deploymentSpecifications": dep_specs}

        payload = {key: val for key, val in payload.items() if val}
        response = self.connection.make_api_request(
            "POST",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(payload),
            operation_name="create deployment",
        )
        return DotDict(response)

    @extra_args
    def list_cluster_groups(self) -> DotDict:
        """Get the available cluster groups given your organization"""
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url: str = f"{self._construct_deploy_ep(org_name, team_name)}/clusterGroups"
        resp = self.connection.make_api_request(
            "GET", url, auth_org=org_name, auth_team=team_name, operation_name="get cluster groups"
        )
        return DotDict(resp)

    @extra_args
    def query_logs(
        self,
        function_id: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        duration: Optional[timedelta] = None,
        function_version_id: Optional[str] = None,
    ) -> Iterator[dict]:
        """Deployment logs.

        Args:
            function_id: Id of function logs are pulled from.
            duration: Specifies the duration of time, either after begin-time or before end-time.
                Format: [nD][nH][nM][nS]. Default: 1 day, doesn't respect decimal measurements.
            start_time: Specifies the start time for querying logs. Default: None.
            end_time: Specifies the end_time time for querying logs. Default: Now.
            function_version_id: Optional version to specify for function id.

        Returns:
            Iterator: Use to recieve logs one by one.
        """
        default_duration = dhms_to_isoduration("1H")
        parsed_duration = dhms_to_isoduration(duration) if duration else None

        (from_date, to_date) = calculate_date_range(
            start_time,
            end_time,
            parsed_duration,
            default_duration=default_duration,
            datetime_format="%Y-%m-%d %H:%M:%S",
        )
        org_name = self.config.org_name
        team_name = self.config.team_name
        url: str = self._construct_logs_ep(
            org_name, team_name=team_name, function_id=function_id, function_version_id=function_version_id
        )

        parameters = [
            {"name": "start", "value": from_date},
            {"name": "end", "value": to_date},
        ]
        payload = {"parameters": parameters}
        resp = self.connection.make_api_request(
            "POST",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(payload),
            operation_name="query logs",
        )
        job_id, metadata = resp.get("jobId", ""), resp.get("metadata", {})
        total_pages, next_page = metadata.get("totalPages", 0), metadata.get("page", 0) + 1
        yield from resp.get("data", [])

        job_url = self._construct_logs_ep(org_name=org_name, team_name=team_name, job_id=job_id)
        next_format_url = job_url + "?page={next_page}&page_size=100"
        while total_pages >= next_page:
            next_url = next_format_url.format(next_page=next_page)
            resp = self.connection.make_api_request(
                "GET", next_url, auth_org=org_name, auth_team=team_name, operation_name="query logs"
            )

            yield from resp.get("data", [])
            next_page += 1
