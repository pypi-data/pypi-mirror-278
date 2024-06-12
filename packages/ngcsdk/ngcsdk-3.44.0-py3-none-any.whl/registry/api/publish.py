#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from typing import List, Optional

from ngcbpc.errors import InvalidArgumentError


class PublishAPI:
    PAGE_SIZE = 1000

    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def validate_args(
        target,
        source,
        metadata_only=False,
        version_only=False,
        visibility_only=False,
        allow_guest: Optional[bool] = False,
        discoverable: Optional[bool] = False,
        public: Optional[bool] = False,
        sign: Optional[bool] = False,  # pylint: disable=unused-argument
        access_type: Optional[str] = None,
        product_names: Optional[List[str]] = None,
    ):
        """This is common validation for all artifact types,
        each artifact type should impose artifact specific validations"""
        if bool(product_names) ^ bool(access_type):
            raise InvalidArgumentError(
                "If specify one of 'product-name' or 'access-type', you must specify the other."
            ) from None
        if sum([metadata_only, version_only, visibility_only]) > 1:
            raise InvalidArgumentError(
                "You can only specify at most one in the argument list: [`metadata_only`,`version_only`,"
                " `visibility_only`]."
            )
        if source and visibility_only:
            raise InvalidArgumentError(
                "You cannot specify a `source` argument when making a `visibility_only` publishing request"
            )
        # copy metadata
        if metadata_only and not (source and target):
            raise InvalidArgumentError(
                "You must specify `source` and `target` argument when making a `metadata_only` publishing request"
            )
        # copy version
        if version_only and not (source and target):
            raise InvalidArgumentError(
                "You must specify `source` and `target` argument when making a `version_only` publishing request"
            )
        # visibility
        if discoverable and not (allow_guest or public):
            raise InvalidArgumentError(
                "discoverable",
                "An item cannot be published as 'discoverable' unless either 'public' or 'allow_guest' is True",
            )

    @staticmethod
    def get_base_url(artifact_type):
        """Return the base URL.  Most endpoints should be built off of this."""
        return f"v2/catalog/{artifact_type}"

    @staticmethod
    def get_product_base_url(artifact_type):
        """
        Return the base URL for publishing an entity under a Product.
        For models, resources, helm-charts, and images. To publish a collection under a Product,
        use the `get_base_url`.
        """
        return f"v2/catalog/{artifact_type}/product"

    def publish_artifact(self, publish_request, artifact_type, org=None, team=None):
        """Publish an artifact: Model, Resource, Helm-Chart"""
        is_unified_catalog = publish_request.toDict().get("productNames", None) and publish_request.toDict().get(
            "accessType", None
        )
        if is_unified_catalog:
            url = self.get_product_base_url(artifact_type)
        else:
            url = f"{self.get_base_url(artifact_type)}/publish"
        return self.connection.make_api_request(
            "POST",
            url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} publish",
        )

    # pylint: disable=unused-argument
    def publish_collection(self, publish_request, artifact_type, org=None, team=None):
        """Publish a collection by copying collection items and publishing collection metadata."""
        url = self.get_base_url("collections")
        ops_urls = []
        ops_urls.append(("copy collection metadata", f"{url}/metadata/copy"))
        ops_urls.append(("publish collection", f"{url}/metadata/share"))
        responses = []
        payload = publish_request.toJSON()
        for operation, url in ops_urls:
            responses.append(
                (
                    operation,
                    self.connection.make_api_request(
                        "POST",
                        url,
                        payload=payload,
                        auth_org=org,
                        auth_team=team,
                        extra_scopes=["artifact"],
                        renew_token=True,
                        operation_name=operation,
                    ),
                )
            )
        return responses

    def copy_metadata_artifact(self, publish_request, artifact_type, org=None, team=None):
        """Copy the metadata of an artifact instead of a deep copy."""
        url = f"{self.get_base_url(artifact_type)}/metadata/copy"
        return self.connection.make_api_request(
            "POST",
            url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} metadata copy",
        )

    def copy_container_version_artifact(self, publish_request, org=None, team=None):
        """Copy the specified version of a container with no metadata changes to the main artifact."""

        for key in ("publishToPublic", "publishAsListedToPublic", "publishWithGuestAccess"):
            setattr(publish_request, key, None)

        file_url = self.get_base_url("containers") + "/images/copy"
        return self.connection.make_api_request(
            "POST",
            file_url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name="post containers version files copy",
        )

    def copy_version_artifact(self, publish_request, artifact_type, org=None, team=None):
        """Copy the specified version of an artifact with no metadata changes to the main artifact."""

        for key in ("publishToPublic", "publishAsListedToPublic", "publishWithGuestAccess"):
            setattr(publish_request, key, None)

        meta_url = f"{self.get_base_url(artifact_type)}/versions/metadata/copy"
        file_url = f"{self.get_base_url(artifact_type)}/versions/files/copy"

        # First, copy the version metadata
        self.connection.make_api_request(
            "POST",
            meta_url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} version metadata copy",
        )
        # Next, copy the file(s) for the version
        return self.connection.make_api_request(
            "POST",
            file_url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} version files copy",
        )

    def update_visibility(self, publish_request, artifact_type, org=None, team=None):
        """Update the visibility settings without changing the metadata or versions/files."""
        url = f"{self.get_base_url(artifact_type)}/share"
        # Only the target info is needed
        publish_request.sourceArtifact = None

        return self.connection.make_api_request(
            "POST",
            url,
            payload=publish_request.toJSON(),
            auth_org=org,
            auth_team=team,
            extra_scopes=["artifact"],
            renew_token=True,
            operation_name=f"post {artifact_type} update visibility",
        )
