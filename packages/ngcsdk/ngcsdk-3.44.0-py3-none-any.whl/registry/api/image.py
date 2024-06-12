#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from argparse import ArgumentTypeError
import csv
from fnmatch import fnmatch
from itertools import chain
import logging
import os
from typing import Any, Generator, List, Optional, Tuple, Union

import docker
from docker.errors import APIError, ImageNotFound, NotFound

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.api.pagination import pagination_helper
from ngcbpc.data.registry.GetManifestByTagResponse import GetManifestByTagResponse
from ngcbpc.data.registry.ImageArchitectureVariant import ImageArchitectureVariant
from ngcbpc.data.registry.ImageScanDetails import ImageScanDetails
from ngcbpc.data.registry.Repository import Repository
from ngcbpc.data.registry.RepositoryCreateRequest import RepositoryCreateRequest
from ngcbpc.data.registry.RepositoryImageDetailsList import RepositoryImageDetailsList
from ngcbpc.data.registry.RepositoryInfoUpdateRequest import RepositoryInfoUpdateRequest
from ngcbpc.data.registry.ScanIssue import ScanIssue
from ngcbpc.errors import (
    AccessDeniedException,
    AuthenticationException,
    InvalidArgumentError,
    NgcAPIError,
    NgcException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)
from ngcbpc.util.io_utils import question_yes_no
from ngcbpc.util.utils import contains_glob, extra_args, format_org_team
from registry.api.dockerwrappers import RegistryWrapper
from registry.api.search import RepositorySearchTransformer
from registry.api.utils import (
    get_label_set_labels,
    get_registry_url,
    ImageRegistryTarget,
)
from registry.data.publishing.Artifact import Artifact
from registry.data.publishing.PublishingRequest import PublishingRequest
from registry.data.publishing.Response import Response
from registry.errors import ImageTagNotFound
from registry.printer.image import ImagePrinter

IMAGE_METAVAR_TAGS = "<org>/[<team>/]<image>[:<tags>]"


logger = logging.getLogger(__name__)


class ImageAPI:
    PAGE_SIZE = 1000

    def __init__(self, connection: Connection = None, api_client=None):
        self.connection = connection
        self.config: Configuration = Configuration()
        self.api_client = api_client
        self.resource_type = "CONTAINER"
        self.printer = ImagePrinter()

    # Public SDK Functions
    @extra_args
    def list(
        self,
        pattern: Optional[str] = None,
        signed: Optional[bool] = False,
        access_type: Optional[str] = None,
        product_names: Optional[str] = None,
    ) -> Union[Generator[list[RepositorySearchTransformer], Any, None], list]:
        """List image given a pattern, returns either the list of repos, or the list of images

        Args:
            pattern: Name or pattern of images. Defaults to None.
            signed: If True, output only signed images. Defaults to False.
            access_type: If specified, output only images with matching access type. Defaults to None.
            product_names: If specified, output only images with matching product name. Defaults to None.

        Returns:
            Union[Generator[list[RepositorySearchTransformer], Any, None], list]: \
                Returns generator of list of found images.
        """
        self.config.validate_configuration(guest_mode_allowed=True, csv_allowed=True)
        irt = ImageRegistryTarget(pattern)
        repo_matcher = "/".join([f for f in [irt.org, irt.team, irt.image] if f]) or "*"
        org = irt.org or self.config.org_name
        team = irt.team or self.config.team_name

        # Only use the repo search if repo portion has a glob expression
        if contains_glob(repo_matcher):
            if access_type or product_names:
                return self.api_client.registry.search.search_repo(
                    org, team, repo_matcher, access_type=access_type, product_names=product_names
                )
            repos = self.api_client.registry.search.search_repo(org, team, repo_matcher, signed=signed)
            if not irt.tag:
                return repos

            images = self._get_images(repos)
            images = self._filter_images(images, irt.tag, signed_only=signed)
            return images

        # No glob in the repo, so we can just get the images for the repo directly.
        # NOTE: `_get_images()` expects a doubly-nested iterator, so we need two levels of brackets.
        images = self._get_images([[repo_matcher]], repo_name=repo_matcher)
        images = self._filter_images(images, irt.tag, signed_only=signed)
        return images

    @extra_args
    def info(
        self,
        image: str,
        layers: Optional[bool] = False,
        history: Optional[bool] = False,
        details: Optional[bool] = False,
        scan: Optional[bool] = False,
    ) -> Union[
        Tuple[Repository, ImageScanDetails],
        Tuple[
            RepositoryImageDetailsList, GetManifestByTagResponse, List[ImageScanDetails], List[ImageArchitectureVariant]
        ],
    ]:
        """Image info given an image name, returns either the info of the repo, or info on an image name

        Args:
            image: Full image name. <org>/[<team>/]<image>[:<tags>]
            layers: Include layer of image. Defaults to False.
            history: Include history of image. Defaults to False.
            details: Include details of image. Defaults to False.
            scan: Include scan of image. Defaults to False.

        Raises:
            ArgumentTypeError: If invalid input
            ResourceNotFoundException: If image is not found
            AuthenticationException: If access is denied

        Returns:
            Return depending on input image argument.
            If image tag is specified, return image repository and scan information
            If image tag is not specified, return image details, manifest, scan details and architecture variants
        """
        self.config.validate_configuration(guest_mode_allowed=True)
        if contains_glob(image):
            raise ArgumentTypeError("image tag doesn't accept glob-like wildcards.")

        irt = ImageRegistryTarget(image)
        repo_name = "/".join([f for f in [irt.org, irt.team, irt.image] if f])

        if not irt.tag:
            if layers:
                raise ArgumentTypeError("--layers requires an image tag.")
            if history:
                raise ArgumentTypeError("--history requires an image tag.")
            try:
                repo_info = self.get_repo_details(irt.org, irt.team, repo_name)
                scan_info = None
                if scan:
                    tag = repo_info.latestTag or "latest"
                    scan_info = self.get_scan_details(irt.org, irt.team, repo_name, tag)
            except ResourceNotFoundException:
                raise ResourceNotFoundException("Image repository '{}' could not be found.".format(image)) from None
            except AuthenticationException:
                raise AuthenticationException("Image repository '{}' access denied.".format(image)) from None
            return (repo_info, scan_info)

        if details:
            raise ArgumentTypeError("--details cannot be used with an image tag.")
        try:
            (image_list, image_details, scan_details) = self.extended_image_info(
                irt.org, irt.team, repo_name, irt.tag, scan
            )
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Image '{}' could not be found.".format(image)) from None
        except AuthenticationException:
            raise AuthenticationException("Image '{}' access denied.".format(image)) from None
        arch_details = self.get_architectures(image_list, irt.tag)
        return (image_list, image_details, scan_details, arch_details)

    @extra_args
    def remove(self, pattern: str, default_yes: Optional[bool] = False) -> None:
        """Remove a given image, or repository of images

        Args:
            pattern: Name or pattern of images. <org>/[<team>/]<image>[:<tags>]
            default_yes: Is confirmation enabled. Defaults to False.

        Raises:
            ArgumentTypeError: If invalid input.
            ResourceNotFoundException: If image is not found.
            AuthenticationException: If access is denied.
        """
        self.config.validate_configuration()
        irt = ImageRegistryTarget(pattern, org_required=True, name_required=True)
        repo_matcher = irt.local_path()

        if contains_glob(repo_matcher):
            raise ArgumentTypeError(
                f"pattern should be in format {IMAGE_METAVAR_TAGS}, where <image> cannot have any wildcards."
            )
        if irt.tag:
            # we need to match the tags and remove all the images - `repo_name:tag_name`
            repo_search_iterator = self.api_client.registry.search.search_repo(irt.org, irt.team, repo_matcher)
            images = self._get_images(repo_search_iterator)
            images = self._filter_images(images, irt.tag)

            if not images:
                _image = f"{repo_matcher}:{irt.tag}"
                if not contains_glob(_image):
                    raise ResourceNotFoundException(f"Image tag '{_image}' does not exist in the repository.")

                raise ResourceNotFoundException(f"No image tags found that matches the pattern '{_image}'.")
            for image in images:
                image_tag_name = f"{image.name}:{image.tag}"
                self._confirm_image_remove(image_tag_name, default_yes)
                try:
                    self.remove_image_tag(
                        org_name=irt.org, team_name=irt.team, repo_name=image.name, tag_name=image.tag
                    )
                except ResourceNotFoundException:
                    raise ResourceNotFoundException(f"Image '{image.name}:{image.tag}' could not be found.") from None

                self.printer.print_ok("Successfully removed image '{}'.".format(image_tag_name))

        else:
            # Since the repo_matcher cannot have glob wildcards, we know that we need to remove exactly 1 repo
            self._confirm_image_remove(repo_matcher, default_yes)
            try:
                self.remove_repo(irt.org, irt.team, repo_matcher)
            except ResourceNotFoundException:
                raise ResourceNotFoundException(
                    "Image repository '{}' could not be found.".format(repo_matcher)
                ) from None
            except AccessDeniedException:
                raise AccessDeniedException(
                    "Access Denied. Only org/team admin has permission to remove an image repository."
                ) from None
            self.printer.print_ok("Successfully removed image repository '{}'.".format(repo_matcher))

    @extra_args
    def create(
        self,
        image: str,
        desc: Optional[str] = None,
        overview: Optional[str] = None,
        label: Optional[List[str]] = None,
        label_set: Optional[List[str]] = None,
        logo: Optional[str] = None,
        publisher: Optional[str] = None,
        built_by: Optional[str] = None,
        multinode: Optional[bool] = False,
        display_name: Optional[str] = None,
    ) -> Repository:
        """Create an empty repository.

        Args:
            image: Full image name without tag. <org>/[<team>/]<image>
            desc: Description of image. Defaults to None.
            overview: Overview of image. Defaults to None.
            label: Label of image. Defaults to None.
            label_set: Label set of image. Defaults to None.
            logo: Logo of image. Defaults to None.
            publisher: Publisher of image. Defaults to None.
            built_by: Time of image built by. Defaults to None.
            multinode: Is image multinode. Defaults to False.
            display_name: Display name of image. Defaults to None.

        Raises:
            ValueError: If image tag is specified.
            ResourceAlreadyExistsException: If image not found.

        Returns:
            Repository: ngccli.data.registry.Repository object.
        """
        self.config.validate_configuration()
        target = ImageRegistryTarget(image)
        if target.tag:
            raise ValueError("Tag should not be specified when trying to create a repository.")

        metadata = {
            "builtBy": built_by,
            "description": overview,
            "displayName": display_name,
            "labelsV2": get_label_set_labels(self.api_client.registry.label_set, self.resource_type, label_set, label),
            "logo": logo,
            "publisher": publisher,
            "shortDescription": desc,
            "multinode": multinode,
            "name": target.image,
        }
        metadata = {k: v for k, v in metadata.items() if v is not None}

        try:
            response = self.create_repo_metadata(target.org, target.team, metadata)
        except ResourceAlreadyExistsException as e:
            raise ResourceAlreadyExistsException(f"Repository '{image}' already exists.") from e

        return response

    @extra_args
    def update(
        self,
        image: str,
        desc: Optional[str] = None,
        overview: Optional[str] = None,
        label: Optional[List[str]] = None,
        label_set: Optional[List[str]] = None,
        logo: Optional[str] = None,
        publisher: Optional[str] = None,
        built_by: Optional[str] = None,
        multinode: Optional[bool] = False,
        no_multinode: Optional[bool] = False,
        display_name: Optional[str] = None,
    ) -> None:
        """Update an image metadata.

        Args:
            image: Full image name. <org>/[<team>/]<image>[:<tags>]
            desc: Description of image. Defaults to None.
            overview: Overview of image. Defaults to None.
            label: Label of image. Defaults to None.
            label_set: Label set of image. Defaults to None.
            logo: Logo of image. Defaults to None.
            publisher: Publisher of image. Defaults to None.
            built_by: Time of image built by. Defaults to None.
            multinode: Is image multinode. Defaults to False.
            no_multinode: Is image not multinode. Defaults to False.
            display_name: Display name of image. Defaults to None.

        Raises:
            ArgumentTypeError: If invalid input image name.
        """
        self.config.validate_configuration()
        if multinode and no_multinode:
            raise ArgumentTypeError("Cannot set multinode and no_multinode")

        parsed_image = ImageRegistryTarget(image)
        metadata = {
            "builtBy": built_by,
            "description": overview,
            "displayName": display_name,
            "labelsV2": get_label_set_labels(self.api_client.registry.label_set, self.resource_type, label_set, label),
            "logo": logo,
            "publisher": publisher,
            "shortDescription": desc,
        }
        if multinode:
            metadata["isMultinodeEnabled"] = True
        elif no_multinode:
            metadata["isMultinodeEnabled"] = False

        metadata = {k: v for k, v in metadata.items() if v is not None}
        self.update_repo_metadata(parsed_image.org, parsed_image.team, parsed_image.local_path(), metadata)

    @extra_args
    def sign(
        self,
        image: str,
    ) -> None:
        """Sign an image in repository, for security

        Args:
            image: Full image name. <org>/[<team>/]<image>[:<tags>]

        Raises:
            NgcException: If image with no tags or http error response from signing endpoint.
            ResourceNotFoundException: If image is not found.
            AccessDeniedException: If permission denied.
        """
        self.config.validate_configuration()
        parsed_image = ImageRegistryTarget(image)
        if parsed_image.tag is None:
            try:
                details = self.get_repo_details(parsed_image.org, parsed_image.team, parsed_image.image_path())
                if not details.latestTag:
                    raise NgcException("Target '{}' has no tags available.".format(image))
            except ResourceNotFoundException:
                raise ResourceNotFoundException("Target '{}' could not be found.".format(image)) from None
            parsed_image.tag = details.latestTag
        dict_payload = {
            "artifactType": "CONTAINER",
            "targetArtifact": {
                "org": parsed_image.org,
                "team": parsed_image.team,
                "name": parsed_image.image,
                "version": parsed_image.tag,
            },
            "sign": True,
        }

        try:
            resp = self.sign_image(parsed_image.org, parsed_image.team, dict_payload)
            if resp.requestStatus.statusCode != "SUCCESS":
                logger.debug(resp.requestStatus.statusCode, resp.requestStatus.statusDescription)
                raise NgcException("Image '{}' signing failed.".format(image)) from None
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Image '{}' could not be found.".format(image)) from None
        except AccessDeniedException:
            raise AccessDeniedException("Access denied signing image '{}".format(image)) from None

    @extra_args
    def push(
        self,
        image: str,
        desc: Optional[str] = None,
        overview: Optional[str] = None,
        label: Optional[List[str]] = None,
        label_set: Optional[List[str]] = None,
        logo: Optional[str] = None,
        publisher: Optional[str] = None,
        built_by: Optional[str] = None,
        multinode: Optional[bool] = None,
        display_name: Optional[str] = None,
        default_yes: Optional[bool] = False,
        output: Optional[bool] = False,
    ) -> None:
        """Push an image to the repository

        Args:
            image: Full image name. nvcr.io/<org>/[<team>/]<image>[:<tags>]
            desc: Description of image. Defaults to None.
            overview: Overview of image. Defaults to None.
            label: Label of image. Defaults to None.
            label_set: Label set of image. Defaults to None.
            logo: Logo of image. Defaults to None.
            publisher: Publisher of image. Defaults to None.
            built_by: Time of image built by. Defaults to None.
            multinode: Is image multinode. Defaults to None.
            display_name: Display name of image. Defaults to None.
            default_yes: Is confirmation enabled. Defaults to False.
            output: Is output enabled. Defaults to False.
        """
        self.config.validate_configuration()
        metadata = {
            "builtBy": built_by,
            "description": overview,
            "displayName": display_name,
            "labelsV2": get_label_set_labels(self.api_client.registry.label_set, self.resource_type, label_set, label),
            "logo": logo,
            "publisher": publisher,
            "shortDescription": desc,
            "isMultinodeEnabled": multinode,
        }
        metadata = {k: v for k, v in metadata.items() if v is not None}

        registry_url = get_registry_url()
        client: docker.APIClient = RegistryWrapper(registry_url)
        self._registry_login(client, registry_url)
        parsed_image = ImageRegistryTarget(image)

        if parsed_image.tag is None:
            parsed_image.tag = "latest"

        pushed_target = self._push_image(client, parsed_image, accept_rename=default_yes, output=output)

        if any(metadata):
            if output:
                self.printer.print_ok("Setting repository metadata")
            self.update_repo_metadata(pushed_target.org, pushed_target.team, pushed_target.local_path(), metadata)
            if output:
                self.printer.print_ok("Repository metadata set.")

    @extra_args
    def pull(
        self,
        image: str,
        scan: Optional[str] = None,
    ) -> None:
        """Pull an image from the repository

        Args:
            image: Full image name. <org>/[<team>/]<image>[:<tags>]
            scan: Scan options. Defaults to None.

        Raises:
            ResourceNotFoundException: If image is not found.
            NgcAPIError: If image API response error.
            NgcException: If NGC related error.
        """
        self.config.validate_configuration(guest_mode_allowed=True)

        if scan:
            return self._pull_scan_report(image, scan)

        registry_url = get_registry_url()
        client: docker.APIClient = RegistryWrapper(registry_url)
        self._registry_login(client, registry_url)
        parsed_image = ImageRegistryTarget(image)

        # Mimic docker CLI's default tag of 'latest' if not specified
        if parsed_image.tag is None:
            parsed_image.tag = "latest"

        try:
            results = client.pull(parsed_image.image_path(), parsed_image.tag)
            for img in results:
                self.printer.print_image_pull_stream(img)
        except NotFound as err:
            raise ResourceNotFoundException(err.explanation or str(err)) from None
        except APIError as err:
            raise NgcAPIError(err.explanation or str(err)) from None
        except NgcException:
            raise
        except Exception as exc:
            raise NgcException(exc) from None
        return None

    def copy_metadata(self, target, source, output=False) -> None:
        self.config.validate_configuration(guest_mode_allowed=False)
        request = PublishingRequest()
        request.artifactType = self.resource_type
        request.sourceArtifact = self._create_publish_request_artifact(source, include_version=False, output=output)
        request.targetArtifact = self._create_publish_request_artifact(target, include_version=False, output=output)

        return self.api_client.registry.publish.copy_metadata_artifact(
            request, "containers", self.config.org_name, self.config.team_name
        )

    def copy_version(self, target, source, output=False) -> None:
        self.config.validate_configuration(guest_mode_allowed=False)
        request = PublishingRequest()
        request.artifactType = self.resource_type
        request.sourceArtifact = self._create_publish_request_artifact(source, output=output)
        request.targetArtifact = self._create_publish_request_artifact(
            target, implied_version=request.sourceArtifact.version, output=output
        )

        return self.api_client.registry.publish.copy_container_version_artifact(
            request, self.config.org_name, self.config.team_name
        )

    def update_visibility(self, target, allow_guest, discoverable, public, output=False) -> None:
        self.config.validate_configuration(guest_mode_allowed=False)

        request = PublishingRequest()
        request.artifactType = self.resource_type
        request.targetArtifact = self._create_publish_request_artifact(target, output=output)

        request.publishToPublic = public
        request.publishWithGuestAccess = allow_guest
        request.publishAsListedToPublic = discoverable

        return self.api_client.registry.publish.update_visibility(
            request, "containers", self.config.org_name, self.config.team_name
        )

    def publish_artifact(
        self,
        target,
        source,
        allow_guest,
        discoverable,
        public,
        sign,
        access_type=None,
        product_names=None,
        output=False,
    ):
        self.config.validate_configuration(guest_mode_allowed=False)

        request = PublishingRequest()
        request.artifactType = self.resource_type

        # visibilities
        request.publishToPublic = public
        request.publishWithGuestAccess = allow_guest
        request.publishAsListedToPublic = discoverable

        # under product
        request.accessType = access_type
        request.productNames = product_names

        # signing
        request.sign = sign

        # versions, image source and target must contain versions
        # user source version(implied) if target version not specified
        version = None
        if source:
            request.sourceArtifact = self._create_publish_request_artifact(source, output=output)
            version = request.sourceArtifact.version
        request.targetArtifact = self._create_publish_request_artifact(target, implied_version=version, output=output)

        self.api_client.registry.publish.publish_artifact(
            request, "containers", self.config.org_name, self.config.team_name
        )

    def _validate_publish_arguments(
        self,
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
        self.api_client.registry.publish.validate_args(
            target,
            source,
            metadata_only,
            version_only,
            visibility_only,
            allow_guest,
            discoverable,
            public,
            sign,
            access_type,
            product_names,
        )
        # below requires source
        # publish to public(legacy publish, no accesstype or productnames)
        if (
            not (access_type and product_names)  # non unified catalog
            and not (visibility_only or metadata_only or version_only)  # intention is to publish
            and not (source and target)
        ):
            raise InvalidArgumentError(
                "You must specify `source` and `target` argument when making a publishing request"
            )

    @extra_args
    def publish(
        self,
        target,
        source: Optional[str] = None,
        metadata_only=False,
        version_only=False,
        visibility_only=False,
        allow_guest: Optional[bool] = False,
        discoverable: Optional[bool] = False,
        public: Optional[bool] = False,
        sign: Optional[bool] = False,
        access_type: Optional[str] = None,
        product_names: Optional[List[str]] = None,
        output=False,
    ):
        """Publishes a docker image with various options for metadata, versioning, and visibility.

        This method manages the publication of docker images to a repository, handling
        different aspects of the publication such as metadata only, version only, and
        visibility adjustments. It validates the combination of arguments provided
        and processes the publication accordingly.

        Args:
            target: The target repository for the docker image.
            source: The identifier of the source docker image.
            metadata_only: If True, only the metadata of the source will be copied to the target.
            version_only: If True, only the version of the source will be copied to the target.
            visibility_only: If True, updates the visibility settings of the target.
            allow_guest: If True, allows guest access to the target.
            discoverable: If True, makes the target discoverable.
            public: If True, makes the target publicly available.
            sign: If True, signs the target.
            access_type: Specifies the type of access for the target.
            product_names: List of product names associated with the target.
            output: If True, output details of the operation.

        Returns:
            None

        Raises:
            InvalidArgumentError: If the arguments provided are invalid or insufficient
            for the requested operation. Specific conditions that raise this error include:
                - Specifying one of 'product-name' or 'access-type' without the other.
                - Specifying more than one of 'metadata_only', 'version_only', or 'visibility_only'.
                - Specifying 'source' and 'visibility_only' together.
                - Omitting 'source' when required by 'metadata_only', 'version_only', or general publication.
                - Attempting to set 'discoverable' without 'public' or 'allow_guest' being True.
        """

        self._validate_publish_arguments(
            target,
            source,
            metadata_only,
            version_only,
            visibility_only,
            allow_guest,
            discoverable,
            public,
            sign,
            access_type,
            product_names,
        )

        if metadata_only:
            self.copy_metadata(target, source, output=output)
        elif version_only:
            self.copy_version(target, source, output=output)
        elif visibility_only:
            self.update_visibility(target, allow_guest, discoverable, public, output=output)
        else:
            self.publish_artifact(
                target, source, allow_guest, discoverable, public, sign, access_type, product_names, output=output
            )
        if output:
            self.printer.print_ok(f"Successfully published {target}")
        logger.debug("Successfully published %s", target)

    # End of Public SDK Functions
    def _digest_for_tag(self, org, team, name, tag):
        """Returns a dict in the format of {architecture: sha256_digest}"""
        try:
            tag_digests = self.get_digest_for_tag(org, team, name, tag)
        except ImageTagNotFound:
            self.printer.print_error(f"The tag '{tag}' was not found.")
            return None
        except ResourceNotFoundException:
            self.printer.print_error(f"The repo '{name}' was not found.")
            return None
        logger.debug("Tag %s has %s architecture(s)", tag, len(tag_digests))

        return tag_digests

    def _pull_scan_report(self, image, scan):
        self.config.validate_configuration()
        irt = ImageRegistryTarget(image)
        if not irt.tag:
            raise ArgumentTypeError("--scan requires an image tag.")

        tag_digests = self._digest_for_tag(irt.org, irt.team, irt.image, irt.tag)
        multi_arch = len(tag_digests) > 1
        file_written = False
        for arch_type, digest in tag_digests.items():
            scan_details = self.get_scan_report(irt.org, irt.team, irt.image, irt.tag, digest)
            scan_info = ImageScanDetails(scan_details)
            if multi_arch:
                nm, ext = os.path.splitext(scan)
                filename = f"{nm}-{arch_type}{ext}"
            else:
                filename = scan
            if not scan_info.scanIssues:
                continue

            # Need to count the number of issues and parse out the headers from ScanIssue properties
            file_written = True
            num_issues = 0
            fieldnames = []
            for key, value in ScanIssue.__dict__.items():
                if isinstance(value, property):
                    fieldnames.append(key)

            # Write the issues to a CSV file
            with open(filename, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for issue in scan_info.scanIssues:
                    writer.writerow(issue.toDict())
                    num_issues += 1
            self.printer.print_ok(f"Wrote {num_issues} issues to file {filename}")
        if not file_written:
            self.printer.print_ok("No issues found. Skipping file write.")

    def _push_image(self, client: docker.APIClient, parsed_image, accept_rename=False, output=False):
        try:
            results = client.push(parsed_image.image_path(), parsed_image.tag)
            if output:
                for msg in results:
                    self.printer.print_image_push_stream(msg)

        except ImageTagNotFound as exc:
            self.printer.print_error(
                "Error: "
                + str(exc)
                + "\nImage must be tagged in format: <registry>/<org>/[<team>/]<image-name>[:<tag>]"
            )
            parsed_image = self._tag_and_push(client, parsed_image, accept_rename, output=output)
            # _tag_and_push calls this function also, so return early as to not print the success message twice
            return parsed_image

        except (APIError, NgcException, ImageNotFound) as exc:
            raise exc

        if output:
            self.printer.print_ok("Successfully pushed '{}' to the registry.".format(str(parsed_image)))
        return parsed_image

    def _tag_and_push(self, client: docker.APIClient, parsed_image, accept_rename, output=False):
        suggested_name = self._generate_suggested_tag(parsed_image, client.registry_url)
        msg = "Would you like to tag '{}' as '{}' and push?".format(str(parsed_image), suggested_name)
        if question_yes_no(msg, default="no", default_yes=accept_rename):
            self._tag_image(client, parsed_image, suggested_name)

            return self._push_image(client, ImageRegistryTarget(suggested_name), output=output)

        raise NgcException("Aborted image tag and push operation.")

    @staticmethod
    def _tag_image(client: docker.APIClient, parsed_image, suggested_name):
        parsed_suggested_name = ImageRegistryTarget(suggested_name)
        try:
            client.tag(str(parsed_image), parsed_suggested_name.image_path(), parsed_suggested_name.tag)
        except ImageNotFound:
            raise NgcException("Error: Image '{}' not found. Tagging image failed.".format(str(parsed_image))) from None
        else:
            logger.debug("Image '%s' successfully tagged '%s'", parsed_image.image_path(), suggested_name)

    def _generate_suggested_tag(self, parsed_image, registry_url):
        team = parsed_image.team or self.config.team_name
        if team == "no-team":
            team = None

        filtered_path = [
            x
            for x in [registry_url, parsed_image.org or self.config.org_name, team, parsed_image.image]
            if x is not None
        ]
        full_path = "/".join(filtered_path)
        suggested_tag = full_path + ":" + parsed_image.tag
        return suggested_tag

    def _registry_login(self, client: docker.APIClient, registry_url: str):
        username = "$oauthtoken"
        app_key = self.config.app_key

        if app_key:
            self.printer.print_ok("Logging in to {}...".format(registry_url), end=" ")
            try:
                client.login(username, app_key)
            except (APIError, ConnectionError) as err:
                self.printer.print_error("login failed.")
                raise NgcException(err) from None
            else:
                self.printer.print_ok("login successful.")
        else:
            logger.debug("Operating in guest mode - not logging in to registry")

    @staticmethod
    def _confirm_image_remove(image, default):
        msg = 'Are you sure you would like to remove "{}"?'.format(image)

        if not question_yes_no(msg, default_yes=default):
            raise NgcException("Remove confirmation failed, remove cancelled.")

    @staticmethod
    def get_architectures(image_obj, tag) -> List[ImageArchitectureVariant]:
        """Returns a list of an image's `architectureVariants` that can be used to get details about an image."""
        if isinstance(image_obj, RepositoryImageDetailsList):
            image_obj = image_obj.toDict()
        images = image_obj.get("images", [])
        if not images:
            # No architecture information
            return []
        image = [img for img in images if img["tag"] == tag]
        if image:
            return image[0].get("architectureVariants", [])
        return []

    @staticmethod
    def _parse_repo_name(repo_name):
        repo_name = repo_name.split("/")
        org = repo_name.pop(0)
        try:
            image = repo_name.pop()
        except IndexError:
            raise ValueError("name of the image not found while parsing the repo name") from None
        # we try to get the team embedded in the pattern
        try:
            team = repo_name.pop()
        except IndexError:
            team = None
        return org, team, image

    @staticmethod
    def _get_repo_url(org, team, repo=None, page_size=None):
        """We need to create the image url - `/v2/org/{org-name}/team/{team-name}/repos`"""
        org_team = format_org_team(org, team)
        parts = ["v2", org_team, "repos", repo]
        ep = "/".join([part for part in parts if part])
        if page_size:
            ep = f"{ep}?page-size={ImageAPI.PAGE_SIZE}"
        return ep

    def _get_image_url(self, org, team, repo, image_id_or_tag=None):
        """We need to create the image url
        - `/v2/org/{org-name}/team/{team-name}/repos/{repo-name}/images/{image_id}`"""
        repo_url = self._get_repo_url(org, team, repo)
        return "/".join([itm for itm in [repo_url, "images", image_id_or_tag] if itm])

    def _get_scan_url(self, org, team, repo, tag, digest=None):
        """Endpoint for image scan status"""
        repo_url = self._get_repo_url(org, team, repo)
        if digest:
            parts = [repo_url, "images", tag, "digest", digest, "scan"]
        else:
            parts = [repo_url, "images", tag, "scan"]
        return "/".join(parts)

    @staticmethod
    def _get_publickey_url():
        """Endpoint for retrieving the image signing publickey"""
        return "v2/catalog/containers/public-key"

    def list_images(self, repo_name):
        if not repo_name:
            return []
        org, team, repo = self._parse_repo_name(repo_name)
        url = self._get_image_url(org, team, repo)
        list_image_dicts = list(
            pagination_helper(self.connection, url, org_name=org, team_name=team, operation_name="list_images")
        )
        if not list_image_dicts:
            return []
        # `list_image_dicts` will have the following structure, depending on the total number of images.
        # [
        #     {"images": [...]},
        #     {"images": [...]},
        #     {"images": [...]},
        # ]
        all_images = {"images": []}
        for image_dict in list_image_dicts:
            all_images["images"].extend(image_dict["images"])
        image_list = RepositoryImageDetailsList(all_images)

        def _set_image_name(image):
            setattr(image, "name", repo_name)
            return image

        return list(map(_set_image_name, image_list.images or []))

    def get_digest_for_tag(self, org, team, repo, tag):
        """Returns a dict in the format of {architecture: sha256_digest}"""
        response = self.connection.make_api_request(
            "GET",
            self._get_image_url(org, team, repo),
            auth_org=org,
            auth_team=team,
            operation_name="get_tag_digests",
        )
        image_list = response.get("images")
        if not image_list:
            raise ResourceNotFoundException(f"No images found for the repo '{repo}'.")
        images = [img for img in image_list if img["tag"] == tag]
        if not images:
            raise ImageTagNotFound(f"Tag '{tag}' was not found.")
        image = images[0]
        return {arch["architecture"]: arch["digest"] for arch in image["architectureVariants"]}

    def get_repo_details(self, org_name, team_name, repo_name):
        """Returns information about a repository, such as:
        * Description
        * Labels
        * Latest Tag
        * Image Size
        """
        org, team, repo = self._parse_repo_name(repo_name)
        url = self._get_repo_url(org, team, repo)
        params = {"resolve-labels": "true"}
        response = self.connection.make_api_request(
            "GET",
            url,
            auth_org=org_name,
            auth_team=team_name,
            params=params,
            operation_name="get_repo_details",
        )
        return Repository(response)

    def get_scan_details(self, org_name, team_name, repo_name, tag):
        org, team, repo = self._parse_repo_name(repo_name)
        url = self._get_scan_url(org, team, repo, tag)
        try:
            scan_data = self.connection.make_api_request(
                "GET",
                url,
                auth_org=org_name,
                auth_team=team_name,
                operation_name="get_repo_scan_details",
            )
        except ResourceNotFoundException:
            # No scan info available; set the values to empty.
            scan_data = {}
        return ImageScanDetails(scan_data)

    def create_repo_metadata(self, org, team, metadata):
        """Create an empty image repository."""
        request = RepositoryCreateRequest(metadata)
        request.isValid()

        response = self.connection.make_api_request(
            "POST",
            self._get_repo_url(org, team),
            payload=request.toJSON(),
            auth_org=org,
            auth_team=team,
            operation_name="create_repo_metadata",
        )

        return Repository(response)

    def update_repo_metadata(self, org_name, team_name, repo_name, metadata):
        org, team, repo = self._parse_repo_name(repo_name)

        request_payload = RepositoryInfoUpdateRequest(metadata)
        request_payload.isValid()

        response = self.connection.make_api_request(
            "PATCH",
            self._get_repo_url(org, team, repo),
            payload=request_payload.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="update_repo_metadata",
        )

        return response

    def remove_repo(self, org_name, team_name, repo_name):
        _org, _team, _image = self._parse_repo_name(repo_name)
        response = self.connection.make_api_request(
            "DELETE",
            self._get_repo_url(_org, _team, _image),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="delete_repo",
        )
        return response

    def remove_image_tag(self, org_name, team_name, repo_name, tag_name):
        _org, _team, _image = self._parse_repo_name(repo_name)
        response = self.connection.make_api_request(
            "DELETE",
            self._get_image_url(_org, _team, _image, tag_name),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="delete_image_tag",
        )
        return response

    def sign_image(self, org_name, team_name, dict_payload) -> Response:
        request_payload = PublishingRequest(dict_payload)
        request_payload.isValid()
        logger.debug(request_payload)
        response = self.connection.make_api_request(
            "POST",
            endpoint=self._get_image_signing_url(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="sign_image",
            payload=request_payload.toJSON(),
        )
        return Response(response)

    def info_image_tag(self, org_name, team_name, repo_name, tag_name):
        _org, _team, _image = self._parse_repo_name(repo_name)
        url = self._get_image_url(_org, _team, _image, tag_name)
        response = self.connection.make_api_request(
            "GET", url, auth_org=org_name, auth_team=team_name, operation_name="info_image_tag"
        )
        return GetManifestByTagResponse(response)

    def extended_image_info(self, org_name, team_name, repo_name, tag_name, scan=False):
        """Concurrently requests information about the images in a given repository for more detail"""
        org, team, image = self._parse_repo_name(repo_name)
        tag_list_url = self._get_image_url(org, team, image)
        tag_info_url = self._get_image_url(org, team, image, tag_name)
        tag_list = list(
            pagination_helper(
                self.connection,
                tag_list_url,
                org_name=org,
                team_name=team,
                operation_name="list_images",
            )
        )
        # `tag_list` will have the following structure, depending on the total number of images.
        # [
        #     {"images": [...]},
        #     {"images": [...]},
        #     {"images": [...]},
        # ]
        all_tags = {"images": []}
        for tag_dict in tag_list:
            all_tags["images"].extend(tag_dict["images"])
        tag_info = self.connection.make_api_request(
            "GET",
            tag_info_url,
            auth_org=org,
            auth_team=team,
            operation_name="get_tag_details",
        )
        scan_info = []
        if scan:
            arch_digests = self.get_digest_for_tag(org, team, image, tag_name)
            for arch, digest in arch_digests.items():
                scan_url = self._get_scan_url(org, team, image, tag_name, digest)
                response = self.connection.make_api_request(
                    "GET", scan_url, auth_org=org_name, auth_team=team_name, operation_name="image digest scan info"
                )
                # The response doesn't contain the arch info, so return it in a tuple with the image scan.
                # We can then parse that tuple during printing to display that information.
                scan_info.append((response, arch))
        # scan_info will be an empty list when called with scan=False, but the ImageScanDetails object will still be
        # valid.
        return (
            RepositoryImageDetailsList(all_tags),
            GetManifestByTagResponse(tag_info),
            [(ImageScanDetails(info[0]), info[1]) for info in scan_info],
        )

    def start_scan(self, org, team, repo, tag):
        """Marks the image represented by `repo:tag` to be scanned. Returns immediately with no return value."""
        base_url = self._get_image_url(org, team, repo, tag)
        url = "/".join([base_url, "scan"])
        self.connection.make_api_request(
            "POST", url, auth_org=org, auth_team=team, operation_name="start_scan", json_response=False
        )

    def start_digest_scan(self, org, team, repo, tag, digest):
        """Marks the image represented by `repo:tag` and the image digest to be scanned. This is required because
        multi-arch images will not be scanned by tag alone.

        Returns immediately with no return value.
        """
        base_url = self._get_image_url(org, team, repo, tag)
        url = "/".join([base_url, "digest", digest, "scan"])
        self.connection.make_api_request(
            "POST", url, auth_org=org, auth_team=team, operation_name="start_digest_scan", json_response=False
        )

    def get_scan_report(self, org, team, repo, tag, digest=None):
        url = self._get_scan_url(org, team, repo, tag, digest=digest)
        return self.connection.make_api_request("GET", url, auth_org=org, auth_team=team, operation_name="scan_report")

    def get_publickey(self):
        url = self._get_publickey_url()
        return self.connection.make_api_request("GET", url, json_response=False, operation_name="image publickey")

    def _get_images(self, repos, repo_name=None):
        images = []
        for repo_search in repos or []:
            for repo in repo_search or []:
                repo_name = repo_name or repo.resourceId
                images.append(self.list_images(repo_name=repo_name))
        return chain(*images)

    @staticmethod
    def _filter_images(images, tag_matcher, signed_only=False):
        if tag_matcher:
            images = [image for image in images if fnmatch(image.tag, tag_matcher)]
        if signed_only:
            images = [image for image in images if hasattr(image, "isSigned") and image.isSigned]
        return images

    @staticmethod
    def _get_image_signing_url():
        """Endpoint for signing an image"""
        return "v2/catalog/containers/signature"

    def _create_publish_request_artifact(
        self, _target, include_version=True, implied_version=None, output=False
    ) -> Artifact:
        # Need a tag to publish; try getting the latest tag. If there is no tag available for the source, the
        # `_get_latest_tag()` method will raise an exception.
        _target_artifact = Artifact()
        _target_obj = ImageRegistryTarget(_target)
        # if include_version
        #                versioned      |    not versioned
        # source       do nothing       |   get latest version on source
        # target       do nothing       |   use source version, fallback to get latest version on target
        # if not include_version, omit version in request
        if include_version:
            if _target_obj.tag:
                _target_artifact.version = _target_obj.tag
            elif implied_version:
                _target_artifact.version = implied_version
                if output:
                    self.printer.print_ok(f"No tag specified for {_target}; using implied tag: {implied_version}.")
                logger.debug("No tag specified for %s; using implied tag: %s.", _target, implied_version)
            else:
                _target_artifact.version = self.get_repo_details(_target_obj.org, _target_obj.team, _target).latestTag
                if output:
                    self.printer.print_ok(
                        f"No tag specified for {_target}; using latest tag: {_target_artifact.version}."
                    )
                logger.debug("No tag specified for %s; using latest tag: %s.", _target, _target_artifact.version)

        _target_artifact.org = _target_obj.org
        _target_artifact.team = _target_obj.team
        _target_artifact.name = _target_obj.image
        return _target_artifact


class GuestImageAPI(ImageAPI):
    def _get_repo_url(self, org=None, team=None, repo=None, page_size=None):
        """we need to create the url for public repos
        `/v2/repos/{org-name}/{team-name}/{repo-name}`"""
        ep = "v2/repos"
        if org:
            ep = "/".join([ep, "{}".format(org)])
        if team:
            ep = "/".join([ep, "{}".format(team)])
        if repo:
            ep = "/".join([ep, repo])
        if page_size:
            ep = "?".join([ep, "page-size={}".format(ImageAPI.PAGE_SIZE)])
        return ep

    def _get_image_url(self, org=None, team=None, repo=None, image_id_or_tag=None):
        """we need to create the url for public image
        `/v2/repos/{org-name}/{team-name}/{repo-name}/images/{image-tag}`"""
        ep = self._get_repo_url(org, team, repo)
        ep = "/".join([ep, "images"])
        if image_id_or_tag:
            ep = "/".join([ep, image_id_or_tag])
        return ep
