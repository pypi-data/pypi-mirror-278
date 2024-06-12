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
from __future__ import annotations

from fnmatch import fnmatch
import http
import json
from typing import Any, Callable, Generator, Optional, TYPE_CHECKING, Union

from nvcf.api.gdn_nvcf_grpc_client.grpc_service_pb2 import (  # pylint: disable = no-name-in-module
    ModelInferRequest,
    ModelInferResponse,
    ModelStreamInferResponse,
)
from nvcf.api.invocation_handler import (
    HTTPSInvocationHandler,
    TritonGRPCInvocationHandler,
)
from nvcf.api.utils import (
    validate_transform_helm_chart,
    validate_transform_image,
    validate_transform_model,
    validate_transform_resource,
)

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.api.utils import DotDict
from ngcbpc.constants import SCOPED_KEY_PREFIX
from ngcbpc.environ import NVCF_SAK
from ngcbpc.errors import InvalidArgumentError, NgcAPIError, NgcException
from ngcbpc.util.utils import extra_args, parse_key_value_pairs

if TYPE_CHECKING:
    import ngcsdk

    import ngccli.api.apiclient

    Client = Union[ngccli.api.apiclient.APIClient, ngcsdk.APIClient]


class FunctionAPI:
    def __init__(self, connection: Connection = None, api_client: Client = None) -> None:
        self.connection = connection
        self.config = Configuration()
        self.client = api_client

    @staticmethod
    def _construct_function_ep(
        org_name: str,
        team_name: Optional[str] = None,
        function_id: Optional[str] = None,
        function_version_id: Optional[str] = None,
    ) -> str:
        parts = ["v2/orgs", org_name]

        if team_name:
            parts.extend(["teams", team_name])
        parts.extend(["nvcf", "functions"])

        if function_id:
            parts.extend([function_id, "versions"])

        if function_version_id:
            parts.append(function_version_id)

        return "/".join(parts)

    @extra_args
    def list(
        self,
        function_id: Optional[str] = None,
        name_pattern: Optional[str] = None,
        access_filter: Optional[list[str]] = None,
    ) -> DotDict:
        """List functions available to the organization. Currently set.

        Args:
            function_id: Optional parameter to list only versions of a specific function. Defaults to None.

            name_pattern: Optional parameter to filter functions that contain this name. Supports wildcards.

            access_filter: Optional parameter to filter functions by their access
            to the account to ["private","public", "authorized"].

        Returns:
            dict: Keyed List of Functions.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_function_ep(org_name, team_name, function_id)
        if access_filter:
            query = "?visibility=" + ",".join(access_filter)
            url += query
        response = self.connection.make_api_request(
            "GET",
            url,
            auth_org=org_name,
            auth_team=team_name,
            operation_name="list function",
        )
        if name_pattern:
            response = {
                "functions": [fn for fn in response.get("functions", []) if fnmatch(fn.get("name"), name_pattern)]
            }
        return DotDict(response)

    @extra_args
    def info(self, function_id: str, function_version_id: str) -> dict:
        """Get information about a given function and version id.

        Args:
            function_id: Function's ID.
            function_version_id: Function's version ID.

        Returns:
            dict: JSON Response of NVCF function information.
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_function_ep(org_name, team_name, function_id, function_version_id)
        response = self.connection.make_api_request(
            "GET",
            url,
            auth_org=org_name,
            auth_team=team_name,
            operation_name="get function",
        )
        return DotDict(response)

    @extra_args
    def delete(self, function_id: str, function_version_id: str):
        """Delete a function or function version"""
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_function_ep(org_name, team_name, function_id, function_version_id)
        try:
            self.connection.make_api_request(
                "DELETE",
                url,
                auth_org=org_name,
                auth_team=team_name,
                operation_name="delete function",
            )
        except NgcAPIError as e:
            if (
                e.response.status_code != http.client.NO_CONTENT
            ):  # Delete endpoint throws 204 which by default throws exception.
                raise NgcAPIError(e) from None

    @extra_args
    def create(
        self,
        name: str,
        inference_url: str,
        health_uri: Optional[str] = None,
        container_image: Optional[str] = None,
        helm_chart: Optional[str] = None,
        helm_chart_service: Optional[str] = None,
        models: Optional[list[str]] = None,
        function_id: Optional[str] = None,
        inference_port: Optional[int] = None,
        container_args: Optional[str] = None,
        api_body_format: Optional[str] = None,
        container_environment_variables: Optional[list[str]] = None,
        tags: Optional[list[str]] = None,
        resources: Optional[list[str]] = None,
    ) -> DotDict:
        """Create a function with the input specification provided by input.

        Args:
            name: Display name of the function.

            inference_url: Endpoint you wish to use to do invocations.

            health_uri: Health endpoint for inferencing

            container_image: Container Image.

            models: Triton compatible models.

            helm_chart: Helm Chart URL.

            helm_chart_service: Only necessary when helm chart is specified.

            function_id: If provided, generate another version of the same function.

            inference_port: Optional port override which inference is forwarded to.

            container_args: Optional list of arguments to provide to container.

            api_body_format: Optional body format to use.

            container_environment_variables: List of key pair values to pass as variables to container.
                In form ["key1:value1", "key2:value2"]

            tags: Optional list of tags to create the function with.

            resources: Optional list of resources.
        Raises:
            InvalidArgumentError: If neither container image, models, or helm chart is provided, this is thrown.
            ResourceNotFoundException: If the image or model or helm chart cannot be found.

        Returns:
            DotDict: Function Response provided by NVCF
        """
        self.config.validate_configuration()
        org_name: str = self.config.org_name
        team_name: Optional[str] = self.config.team_name
        url = self._construct_function_ep(org_name, team_name, function_id)

        if helm_chart and (container_image or models):
            raise InvalidArgumentError("Can not include helm chart with models or image")

        if not models and not container_image and not helm_chart:
            raise InvalidArgumentError("Must include either models and/or a container image or helm chart")

        if container_image:
            container_image = validate_transform_image(self.client, container_image)

        function_models: list[dict] = []
        for model in models or []:
            function_models.append(validate_transform_model(self.client, model))

        if helm_chart:
            if not helm_chart_service:
                raise InvalidArgumentError("Must include a helm chart service name if helm chart is included")
            helm_chart = validate_transform_helm_chart(self.client, helm_chart)

        function_resources: list[dict] = []
        for resource in resources or []:
            function_resources.append(validate_transform_resource(self.client, resource))

        if container_environment_variables:
            container_environment_variables = [
                {"key": k, "value": v} for k, v in parse_key_value_pairs(container_environment_variables).items()
            ]

        payload: dict[str, Any] = {
            "name": name,
            "healthUri": health_uri,
            "inferenceUrl": inference_url,
            "inferencePort": inference_port,
            "containerArgs": container_args,
            "containerEnvironment": container_environment_variables,
            "models": function_models,
            "containerImage": container_image,
            "apiBodyFormat": api_body_format,
            "helmChart": helm_chart,
            "helmChartServiceName": helm_chart_service,
            "tags": tags,
            "resources": function_resources,
        }
        payload = {key: val for key, val in payload.items() if val}

        response = self.connection.make_api_request(
            "POST",
            url,
            payload=json.dumps(payload),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="create function",
        )
        return DotDict(response)

    @extra_args
    def invoke(
        self,
        function_id: str,
        payload: dict,
        function_version_id: Optional[str] = None,
        starfleet_api_key: Optional[str] = None,
        asset_ids: Optional[list[str]] = None,
        output_zip_path: Optional[str] = None,
        polling_request_timeout: Optional[int] = 300,
        pending_request_timeout: Optional[int] = 600,
        pending_request_interval: Optional[float] = 1.0,
    ) -> DotDict:
        """
        Args:
            function_id: ID of NVCF Function being invoked.

            payload: JSON payload specific to the function you are invoking.
            The shape should adhere to your function's API SPEC.

            starfleet_api_key: Key with invocation access to the function.

            function_version_id: Optionally provide a version id to invoke a specific version of a function.

            asset_ids: Asset ids that are referenced in the payload.

            output_zip: If output provides a zip file, this is the location to save the zip file.
        Raises:
            NgcException: Matching HTTP Response code if fails in any way.

        Returns:
            Dictionary corresponding to JSON response from function invoked.
        """
        conf_sf_key = None
        if self.config.app_key and self.config.app_key.startswith(SCOPED_KEY_PREFIX):
            conf_sf_key = self.config.app_key
        starfleet_api_key = starfleet_api_key or conf_sf_key or NVCF_SAK
        if not starfleet_api_key:
            # Will only present this through SDK, CLI has additional method of passing in through getpaswd
            raise NgcException("Please set the environment variable $NVCF_SAK or pass key in as sak_key")

        with HTTPSInvocationHandler(
            starfleet_api_key=starfleet_api_key,
        ) as invocation_handler:
            return DotDict(
                invocation_handler.make_invocation_request(
                    function_id,
                    data=payload,
                    function_version_id=function_version_id,
                    asset_ids=asset_ids,
                    output_zip_path=output_zip_path,
                    polling_request_timeout=polling_request_timeout,
                    pending_request_timeout=pending_request_timeout,
                    pending_request_interval=pending_request_interval,
                )
            )

    @extra_args
    def invoke_stream(
        self,
        function_id: str,
        payload: dict,
        starfleet_api_key: str = None,
        function_version_id: Optional[str] = None,
        asset_ids: Optional[list[str]] = None,
        request_timeout: Optional[int] = 300,
    ) -> Generator[bytes, None, None]:
        """
        Args:
            function_id: ID of NVCF Function being invoked.

            payload: JSON payload specific to the function you are invoking.
            The shape should adhere to your function's API SPEC.

            starfleet_api_key: Key with invocation access to the function.

            function_version_id: Optionally provide a version id to invoke a specific version of a function.

        Raises:
            NgcException: Matching HTTP Response code if fails in any way.

        Returns:
            Generator[bytes, None, None]: Streaming response of function invocation.
        """
        conf_sf_key = None
        if self.config.app_key and self.config.app_key.startswith(SCOPED_KEY_PREFIX):
            conf_sf_key = self.config.app_key
        starfleet_api_key = starfleet_api_key or conf_sf_key or NVCF_SAK
        if not starfleet_api_key:
            # Will only present this through SDK, CLI has additional method of passing in through getpaswd
            raise NgcException("Please set the environment variable $NVCF_SAK or pass key in as sak_key")

        with HTTPSInvocationHandler(
            starfleet_api_key=starfleet_api_key,
        ) as invocation_handler:
            return invocation_handler.make_streaming_invocation_request(
                function_id,
                data=payload,
                function_version_id=function_version_id,
                asset_ids=asset_ids,
                request_timeout=request_timeout,
            )

    @extra_args
    def invoke_grpc(
        self,
        function_id: str,
        starfleet_api_key: str,
        function_request: Any,
        grpc_stub_function: Callable,
        function_version_id: Optional[str] = None,
    ) -> Any:
        """
        Args:
            function_id: ID of GRPC NVCF Function being invoked.

            starfleet_api_key: Key with invocation access to the function.

            function_request: GRPC Payload specific to the function you are invoking.

            grpc_stub_function: GRPC Stub function to invoke.

            function_version_id: Optionally provide a version id to invoke a specific version of a function.

        Raises:
            NgcException: Matching HTTP Response code if fails in any way.

        Returns:
            Any: GRPC Response of function invocation.
        """
        conf_sf_key = None
        if self.config.app_key and self.config.app_key.startswith(SCOPED_KEY_PREFIX):
            conf_sf_key = self.config.app_key
        starfleet_api_key = starfleet_api_key or conf_sf_key or NVCF_SAK
        if not starfleet_api_key:
            # Will only present this through SDK, CLI has additional method of passing in through getpaswd
            raise NgcException("Please set the environment variable $NVCF_SAK or pass key in as sak_key")

        metadata = [("function-id", function_id), ("authorization", "Bearer " + starfleet_api_key)]
        if function_version_id:
            metadata += [("function-version-id", function_version_id)]

        return grpc_stub_function(function_request, metadata=metadata)

    @extra_args
    def invoke_stream_grpc(
        self,
        function_id: str,
        starfleet_api_key: str,
        function_request: Any,
        grpc_stub_function: Callable,
        function_version_id: Optional[str] = None,
    ) -> Any:
        """
        Args:
            function_id: ID of GRPC NVCF Function being invoked.

            starfleet_api_key: Key with invocation access to the function.

            function_request: GRPC Payload specific to the function you are invoking.

            grpc_stub_function: GRPC Stub function to invoke.

            function_version_id: Optionally provide a version id to invoke a specific version of a function.

        Raises:
            NgcException: Matching HTTP Response code if fails in any way.

        Returns:
            Any: GRPC Response of function invocation.
        """
        conf_sf_key = None
        if self.config.app_key and self.config.app_key.startswith(SCOPED_KEY_PREFIX):
            conf_sf_key = self.config.app_key
        starfleet_api_key = starfleet_api_key or conf_sf_key or NVCF_SAK
        if not starfleet_api_key:
            # Will only present this through SDK, CLI has additional method of passing in through getpaswd
            raise NgcException("Please set the environment variable $NVCF_SAK or pass key in as sak_key")

        metadata = [("function-id", function_id), ("authorization", "Bearer " + starfleet_api_key)]
        if function_version_id:
            metadata += [("function-version-id", function_version_id)]

        return grpc_stub_function(iter([function_request]), metadata=metadata)

    @extra_args
    def invoke_grpc_triton(
        self,
        function_id: str,
        function_request: ModelInferRequest,
        starfleet_api_key: Optional[str] = None,
        function_version_id: Optional[str] = None,
    ) -> ModelInferResponse:
        """
        Args:
            function_id: ID of Triton based GRPC NVCF Function being invoked.

            function_request: GRPC Payload specific to the function you are invoking.

            starfleet_api_key: Key with invocation access to the function.

            function_version_id: Optionally provide a version id to invoke a specific version of a function.


        Returns:
            ModelInferResponse: GRPC Response of function invocation
        """
        conf_sf_key = None
        if self.config.app_key and self.config.app_key.startswith(SCOPED_KEY_PREFIX):
            conf_sf_key = self.config.app_key
        starfleet_api_key = starfleet_api_key or conf_sf_key or NVCF_SAK
        if not starfleet_api_key:
            # Will only present this through SDK, CLI has additional method of passing in through getpaswd
            raise NgcException("Please set the environment variable $NVCF_SAK or pass key in as sak_key")

        with TritonGRPCInvocationHandler(
            starfleet_api_key=starfleet_api_key,
        ) as invocation_handler:
            return invocation_handler.make_invocation_request(
                function_id=function_id,
                function_request=function_request,
                function_version_id=function_version_id,
            )

    @extra_args
    def invoke_stream_grpc_triton(
        self,
        function_id: str,
        function_request: ModelInferRequest,
        starfleet_api_key: Optional[str] = None,
        function_version_id: Optional[str] = None,
    ) -> list[ModelStreamInferResponse]:
        """
        Args:
            function_id: ID of Triton based GRPC NVCF Function being invoked.

            function_request: GRPC Payload specific to the function you are invoking.

            starfleet_api_key: Key with invocation access to the function.

            function_version_id: Optionally provide a version id to invoke a specific version of a function.
        Returns:
            ModelStreamInferResponse: Streaming response of function invocation
        """
        conf_sf_key = None
        if self.config.app_key and self.config.app_key.startswith(SCOPED_KEY_PREFIX):
            conf_sf_key = self.config.app_key
        starfleet_api_key = starfleet_api_key or conf_sf_key or NVCF_SAK
        if not starfleet_api_key:
            # Will only present this through SDK, CLI has additional method of passing in through getpaswd
            raise NgcException("Please set the environment variable $NVCF_SAK or pass key in as sak_key")

        output = []
        with TritonGRPCInvocationHandler(
            starfleet_api_key=starfleet_api_key,
        ) as invocation_handler:
            for stream_resp in invocation_handler.make_streaming_invocation_request(
                function_id=function_id,
                function_request=function_request,
                function_version_id=function_version_id,
            ):
                output.append(stream_resp)
        return output
