#
# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import argparse
from builtins import int
from collections.abc import Iterable
import datetime
from itertools import chain
import logging
from operator import xor
import os
from typing import List, Optional, Union

from ngcbpc.api.authentication import Authentication
from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.api.pagination import pagination_helper_use_page_reference
from ngcbpc.constants import CANARY_ENV, PRODUCTION_ENV, STAGING_ENV, TRANSFER_STATES
from ngcbpc.data.model.ArtifactAttribute import ArtifactAttribute
from ngcbpc.data.model.Model import Model
from ngcbpc.data.model.ModelCreateRequest import ModelCreateRequest
from ngcbpc.data.model.ModelResponse import ModelResponse
from ngcbpc.data.model.ModelUpdateRequest import ModelUpdateRequest
from ngcbpc.data.model.ModelVersion import ModelVersion
from ngcbpc.data.model.ModelVersionCreateRequest import ModelVersionCreateRequest
from ngcbpc.data.model.ModelVersionFileListResponse import ModelVersionFileListResponse
from ngcbpc.data.model.ModelVersionListResponse import ModelVersionListResponse
from ngcbpc.data.model.ModelVersionResponse import ModelVersionResponse
from ngcbpc.data.model.ModelVersionUpdateRequest import ModelVersionUpdateRequest
from ngcbpc.errors import (
    InvalidArgumentError,
    NgcException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)
from ngcbpc.printer.transfer import TransferPrinter
from ngcbpc.transfer import async_download, http_uploader
from ngcbpc.transfer.utils import get_download_files
from ngcbpc.util.file_utils import get_file_contents, tree_size_and_count
from ngcbpc.util.utils import confirm_remove, extra_args, format_org_team
from registry.api.utils import (
    add_credentials_to_request,
    filter_version_list,
    get_environ_tag,
    get_label_set_labels,
    handle_public_dataset_no_args,
    ModelRegistryTarget,
    verify_link_type,
)
from registry.constants import MODEL_SERVICE_URL_MAPPING
from registry.transformer.image import RepositorySearchTransformer

logger = logging.getLogger(__name__)

PAGE_SIZE = 1000

environ_tag = get_environ_tag()
env = {PRODUCTION_ENV: "prod", CANARY_ENV: "canary", STAGING_ENV: "stg"}.get(environ_tag)
ENDPOINT_VERSION = "v1" if Configuration().base_url == MODEL_SERVICE_URL_MAPPING[env] else "v2"


class ModelAPI:
    def __init__(self, connection: Connection, api_client=None):
        self.config = Configuration()
        self.connection = connection
        self.api_client = api_client
        self.transfer_printer = TransferPrinter()

    # PUBLIC FUNCTIONS
    @extra_args
    def download_version(
        self,
        target: str,
        destination: Optional[str] = ".",
        file_patterns: Optional[List[str]] = None,
        exclude_patterns: Optional[List[str]] = None,
    ) -> None:
        """Download the specified model version.

        Args:
            target: Full model name. org/[team/]name[:version]
            destination: Description of model. Defaults to ".".
            file_patterns: Inclusive filter of model files. Defaults to None.
            exclude_patterns: Eclusive filter of model files. Defaults to None.

        Raises:
            NgcException: If unable to download.
            ResourceNotFoundException: If model is not found.

        """
        self.config.validate_configuration(guest_mode_allowed=True)
        # non-list, use org/team from target
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True, version_required=False)

        if not mrt.version:
            mrt.version = self._get_latest_version(mrt)
            target += f":{mrt.version}"
            self.transfer_printer.print_ok(f"No version specified, downloading latest version: '{mrt.version}'.")

        download_dir = os.path.abspath(destination)
        if not os.path.isdir(download_dir):
            raise NgcException(f"The path: '{destination}' does not exist.")
        try:
            version_resp = self.get_version(mrt.org, mrt.team, mrt.name, mrt.version)
            version_status = version_resp.modelVersion.status
            if version_status != "UPLOAD_COMPLETE":
                raise NgcException(f"'{target}' is not in state UPLOAD_COMPLETE.")
        except ResourceNotFoundException:
            raise ResourceNotFoundException(f"'{target}' could not be found.") from None

        self.transfer_printer.print_download_message("Getting files to download...\n")
        all_files = list(self.get_version_files(target, mrt.org, mrt.team))
        all_files_path_size = {f.path: f.sizeInBytes for f in all_files}
        dl_files, total_size = get_download_files(
            {f.path: f.sizeInBytes for f in all_files}, [], file_patterns, None, exclude_patterns
        )
        dl_files_with_size = {f: all_files_path_size.get(f, 0) for f in dl_files}
        paginated = not (file_patterns or exclude_patterns)
        if paginated:
            logger.debug("Downloading all files for model '%s' version '%s'", mrt.name, mrt.version)
        else:
            logger.debug("Downloading %s files for model '%s' version '%s'", len(dl_files), mrt.name, mrt.version)
        url = self.get_direct_download_URL(mrt.name, mrt.version, org=mrt.org, team=mrt.team)
        # Need to match the old output where the files are within a subfolder
        download_dir = f"{download_dir}/{mrt.name}_v{mrt.version}"
        started_at = datetime.datetime.now()
        (
            elapsed,
            download_count,
            download_size,
            failed_count,
            _,
            _,
        ) = async_download.direct_download_files(
            "model",
            mrt.name,
            mrt.org,
            mrt.team,
            mrt.version,
            url,
            paginated,
            dl_files_with_size,
            total_size,
            download_dir,
        )
        ended_at = datetime.datetime.now()
        status = "FAILED" if failed_count else "COMPLETED"
        return self.transfer_printer.print_async_download_transfer_summary(
            "model", status, download_dir, elapsed, download_count, download_size, started_at, ended_at
        )

    @extra_args
    def upload_version(
        self,
        target: str,
        source: Optional[str] = ".",
        gpu_model: Optional[str] = None,
        memory_footprint: Optional[str] = None,
        num_epochs: Optional[int] = None,
        batch_size: Optional[int] = None,
        accuracy_reached: Optional[float] = None,
        description: Optional[str] = None,
        link: Optional[str] = None,
        link_type: Optional[str] = None,
        dry_run: Optional[bool] = False,
        credential_files: Optional[List[str]] = None,
        metric_files: Optional[List[str]] = None,
    ) -> None:
        """Upload a model version.

        Args:
            target: Full model name. org/[team/]name[:version]
            source: Source location of model. Defaults to the current directory.
            gpu_model: GPU model of model. Defaults to None.
            memory_footprint: Memory footprint of model. Defaults to None.
            num_epochs: Epoch number of model. Defaults to None.
            batch_size: Batch size of model. Defaults to None.
            accuracy_reached: Accuracy of model. Defaults to None.
            description: Description of model. Defaults to None.
            link: Link of model. Defaults to None.
            link_type: Link type of model. Defaults to None.
            dry_run: Is this a dry run. Defaults to False.
            credential_files: Credential files of model. Defaults to None.
            metric_files: Metric files of model. Defaults to None.

        Raises:
            NgcException: If failed to upload model.
            argparse.ArgumentTypeError: If invalid input model name.
            ResourceAlreadyExistsException: If model resource already existed.
            ResourceNotFoundException: If model cannot be find.
        """
        self.config.validate_configuration()
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True, version_required=True)

        transfer_path = os.path.abspath(source)
        if not os.path.exists(transfer_path):
            raise NgcException("The path: '{0}' does not exist.".format(transfer_path))

        verify_link_type(link_type)
        version_req = ModelVersionCreateRequest(
            {
                "versionId": mrt.version,
                "accuracyReached": accuracy_reached,
                "batchSize": batch_size,
                "description": description,
                "gpuModel": gpu_model,
                "memoryFootprint": memory_footprint,
                "numberOfEpochs": num_epochs,
            }
        )

        if link and link_type:
            version_req.otherContents = [ArtifactAttribute({"key": link_type, "value": link})]

        if xor(bool(link), bool(link_type)):
            raise argparse.ArgumentTypeError("Invalid arguments: --link and --link-type must be used together.")

        version_req = add_credentials_to_request(version_req, credential_files, metric_files)

        version_req.isValid()
        try:
            if not dry_run:
                self.create_version(mrt.org, mrt.team, mrt.name, version_req)
        except ResourceAlreadyExistsException:
            version_resp = self.get_version(mrt.org, mrt.team, mrt.name, mrt.version)
            version_status = version_resp.modelVersion.status
            if version_status != "UPLOAD_PENDING":
                raise ResourceAlreadyExistsException("Target '{}' already exists.".format(mrt)) from None
        except ResourceNotFoundException:
            target_base = "/".join([x for x in [mrt.org, mrt.team, mrt.name] if x is not None])
            raise ResourceNotFoundException("Target '{}' not found.".format(target_base)) from None

        if dry_run:
            self.transfer_printer.print_ok("Files to be uploaded:")
        transfer_size, file_count = tree_size_and_count(
            transfer_path,
            omit_links=False,
            print_paths=dry_run,
            dryrun_option=dry_run,
            check_max_size=True,
        )
        if dry_run:
            self.transfer_printer.print_upload_dry_run(transfer_size, file_count)
            return None
        ep = self.get_multipart_files_endpoint(org=mrt.org, team=mrt.team)
        full_url = self.connection.create_full_URL(ep)

        headers = Authentication.auth_header(auth_org=mrt.org, auth_team=mrt.team)
        started_at = datetime.datetime.now()
        (
            elapsed,
            upload_count,
            upload_size,
            failed_count,
            upload_total_size,
            total_file_count,
            _,
        ) = http_uploader.upload_directory(
            transfer_path,
            full_url,
            mrt.name,
            mrt.version,
            mrt.org,
            mrt.team,
            "model",
            headers=headers,
            operation_name="model upload_version",
        )
        ended_at = datetime.datetime.now()
        xfer_id = f"{mrt.name}[version={mrt.version}]"
        if failed_count or upload_count == 0:
            status = TRANSFER_STATES["FAILED"]
        elif upload_size != upload_total_size or upload_count != total_file_count:
            status = TRANSFER_STATES["TERMINATED"]
        else:
            status = TRANSFER_STATES["COMPLETED"]
            self._update_upload_complete(mrt.org, mrt.team, mrt.name, mrt.version)
        self.transfer_printer.print_async_upload_transfer_summary(
            "model", xfer_id, status, transfer_path, elapsed, upload_count, upload_size, started_at, ended_at
        )
        return None

    @extra_args
    def update(
        self,
        target: str,
        application: Optional[str] = None,
        framework: Optional[str] = None,
        model_format: Optional[str] = None,
        precision: Optional[str] = None,
        short_description: Optional[str] = None,
        description: Optional[str] = None,
        overview_filename: Optional[str] = None,
        bias_filename: Optional[str] = None,
        explainability_filename: Optional[str] = None,
        privacy_filename: Optional[str] = None,
        safety_security_filename: Optional[str] = None,
        display_name: Optional[str] = None,
        label: List[Optional[str]] = None,
        label_set: List[Optional[str]] = None,
        logo: Optional[str] = None,
        public_dataset_name: Optional[str] = None,
        public_dataset_link: Optional[str] = None,
        public_dataset_license: Optional[str] = None,
        memory_footprint: Optional[str] = None,
        built_by: Optional[str] = None,
        publisher: Optional[str] = None,
        batch_size: Optional[int] = None,
        num_epochs: Optional[int] = None,
        accuracy_reached: Optional[float] = None,
        gpu_model: Optional[str] = None,
        set_latest: Optional[bool] = None,
    ) -> Union[Model, ModelVersion]:
        """Update a model or model version.

        Args:
            target: Full model name. org/[team/]name[:version]
            application: Application of model. Defaults to None.
            framework: Framework of model. Defaults to None.
            model_format: Format of model. Defaults to None.
            precision: Precision of model. Defaults to None.
            short_description: Short description of model. Defaults to None.
            description: Description of model. Defaults to None.
            overview_filename: Overview of model filename. Defaults to None.
            bias_filename: Bias filename of model. Defaults to None.
            explainability_filename: Explainability filename of model. Defaults to None.
            privacy_filename: Privacy filename of model. Defaults to None.
            safety_security_filename: Safety security filename of model. Defaults to None.
            display_name: Display name of model. Defaults to None.
            label (Lis: Label of model. Defaults to None.
            label_set (Lis: Label set of model. Defaults to None.
            logo: Logo of model. Defaults to None.
            public_dataset_name: Public dataset name of model. Defaults to None.
            public_dataset_link: Public dataset link of model. Defaults to None.
            public_dataset_license: Public dataset license of model. Defaults to None.
            memory_footprint: Memory footprint of model. Defaults to None.
            built_by: Time model is built by. Defaults to None.
            publisher: Model publisher. Defaults to None.
            batch_size: Model batch size. Defaults to None.
            num_epochs: Epoch number of model. Defaults to None.
            accuracy_reached: Accuracy of model. Defaults to None.
            gpu_model: GPU model of model. Defaults to None.
            set_latest: Model set latest. Defaults to None.

        Raises:
            ResourceNotFoundException: If model is not found

        """
        self.config.validate_configuration(guest_mode_allowed=True)
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
        org_name = mrt.org
        team_name = mrt.team

        if mrt.version:
            self._validate_update_version(locals())
            version_update_req = ModelVersionUpdateRequest(
                {
                    "accuracyReached": accuracy_reached,
                    "batchSize": batch_size,
                    "gpuModel": gpu_model,
                    "memoryFootprint": memory_footprint,
                    "numberOfEpochs": num_epochs,
                    "description": description,
                }
            )
            version_update_req.isValid()

            try:
                model = self.update_version(
                    org_name=org_name,
                    team_name=team_name,
                    model_name=mrt.name,
                    version=mrt.version,
                    version_update_request=version_update_req,
                    set_latest=set_latest,
                )
            except ResourceNotFoundException:
                raise ResourceNotFoundException(f"Model version '{target}' was not found.") from None

            return model

        self._validate_update_model(locals())
        model_update_dict = {
            "application": application,
            "framework": framework,
            "modelFormat": model_format,
            "precision": precision,
            "shortDescription": short_description,
            "description": get_file_contents(overview_filename, "--overview-filename"),
            "displayName": display_name,
            "labelsV2": get_label_set_labels(self.api_client.registry.label_set, "MODEL", label_set, label),
            "logo": logo,
            "publicDatasetUsed": handle_public_dataset_no_args(
                public_dataset_name=public_dataset_name,
                public_dataset_link=public_dataset_link,
                public_dataset_license=public_dataset_license,
            ),
            "builtBy": built_by,
            "publisher": publisher,
            "bias": get_file_contents(bias_filename, "--bias-filename"),
            "explainability": get_file_contents(explainability_filename, "--explainability-filename"),
            "privacy": get_file_contents(privacy_filename, "--privacy-filename"),
            "safetyAndSecurity": get_file_contents(safety_security_filename, "--safety-security-filename"),
        }
        model_update_request = ModelUpdateRequest(model_update_dict)
        model_update_request.isValid()
        try:
            resp = self.connection.make_api_request(
                "PATCH",
                self._get_models_endpoint(org=org_name, team=team_name, name=mrt.name),
                payload=model_update_request.toJSON(),
                auth_org=org_name,
                auth_team=team_name,
                operation_name="update model",
            )
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Model '{}' was not found.".format(target)) from None
        return ModelResponse(resp).model

    @extra_args
    def create(
        self,
        target: str,
        application: str,
        framework: str,
        model_format: str,
        precision: str,
        short_description: str,
        overview_filename: Optional[str] = None,
        bias_filename: Optional[str] = None,
        explainability_filename: Optional[str] = None,
        privacy_filename: Optional[str] = None,
        safety_security_filename: Optional[str] = None,
        display_name: Optional[str] = None,
        label: List[Optional[str]] = None,
        label_set: List[Optional[str]] = None,
        logo: Optional[str] = None,
        public_dataset_name: Optional[str] = None,
        public_dataset_link: Optional[str] = None,
        public_dataset_license: Optional[str] = None,
        built_by: Optional[str] = None,
        publisher: Optional[str] = None,
    ) -> Model:
        """Create a Model.

        Args:
            target: Full name of model. org/[team/]name[:version]
            application: Application of model.
            framework: Framework of model.
            model_format: Format of model.
            precision: Precision of model.
            short_description: Short description of model.
            overview_filename: Overview filename of model. Defaults to None.
            bias_filename: Bias_filename of model. Defaults to None.
            explainability_filename: Explainability filename of model. Defaults to None.
            privacy_filename: Privacy filename of model. Defaults to None.
            safety_security_filename: Safety security filename of model. Defaults to None.
            display_name: Display name of model. Defaults to None.
            labels: Label of model. Defaults to None.
            label_sets: Label set of model. Defaults to None.
            logo: Logo of model. Defaults to None.
            public_dataset_name: Public dataset name of model. Defaults to None.
            public_dataset_link: Public dataset link of model. Defaults to None.
            public_dataset_license: Public dataset license of model. Defaults to None.
            built_by: Time of model built by. Defaults to None.
            publisher: Publisher of model. Defaults to None.

        Raises:
            ResourceAlreadyExistsException: _description_

        Returns:
            Model: _description_
        """
        self.config.validate_configuration()
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True, version_allowed=False)
        org_name = mrt.org
        team_name = mrt.team

        model_create_dict = {
            # required
            "name": mrt.name,
            "application": application,
            "framework": framework,
            "modelFormat": model_format,
            "precision": precision,
            "shortDescription": short_description,
            # optional
            "description": get_file_contents(overview_filename, "--overview-filename"),
            "displayName": display_name,
            "labelsV2": get_label_set_labels(self.api_client.registry.label_set, "MODEL", label_set, label),
            "logo": logo,
            "publicDatasetUsed": handle_public_dataset_no_args(
                public_dataset_name=public_dataset_name,
                public_dataset_link=public_dataset_link,
                public_dataset_license=public_dataset_license,
            ),
            "builtBy": built_by,
            "publisher": publisher,
            "bias": get_file_contents(bias_filename, "--bias-filename"),
            "explainability": get_file_contents(explainability_filename, "--explainability-filename"),
            "privacy": get_file_contents(privacy_filename, "--privacy-filename"),
            "safetyAndSecurity": get_file_contents(safety_security_filename, "--safety-security-filename"),
        }
        model_create_request = ModelCreateRequest(model_create_dict)
        model_create_request.isValid()

        try:
            return self._create(org_name=org_name, team_name=team_name, mcr=model_create_request)
        except ResourceAlreadyExistsException:
            raise ResourceAlreadyExistsException("Model '{}' already exists.".format(target)) from None

    @extra_args
    def info(
        self,
        target: str,
    ) -> Union[ModelResponse, ModelVersionResponse]:
        """Retrieve metadata for a model or model version.

        Args:
            target: Full model name. org/[team/]name[:version]

        Raises:
            ResourceNotFoundException: If model is not found.

        Returns:
            Union[ModelResponse, ModelVersionResponse]: model or model version depending on input
        """
        self.config.validate_configuration(guest_mode_allowed=True)
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True)

        if mrt.version:
            try:
                version_resp = self.get_version(
                    org_name=mrt.org, team_name=mrt.team, model_name=mrt.name, version=str(mrt.version)
                )
            except ResourceNotFoundException:
                raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
            return version_resp

        try:
            model_resp = self.get(mrt.org, mrt.team, mrt.name)
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
        return model_resp

    @extra_args
    def list(
        self,
        target: Optional[str] = None,
        org: Optional[str] = None,
        team: Optional[str] = None,
        order: Optional[str] = None,
        access_type: Optional[str] = None,
        product_names: Optional[str] = None,
    ) -> Union[List[ModelVersion], List[RepositorySearchTransformer]]:
        """List model(s) or model version(s).

        Args:
            target: Name or pattern of models. Defaults to None.
            org: Organization. Defaults to None.
            team: Team. Defaults to None.
            order: Order by. Defaults to None.
            access_type: Access type filter of models. Defaults to None.
            product_names: Product type filter of models. Defaults to None.

        Raises:
            argparse.ArgumentTypeError: invalid input target

        Returns:
            Union[List[ModelVersion], List[RepositorySearchTransformer]]: \
                list of model version or list of models depending on input
        """
        self.config.validate_configuration(guest_mode_allowed=True, csv_allowed=True)
        mrt = ModelRegistryTarget(target, glob_allowed=True)
        org = org or mrt.org or self.config.org_name
        team = team or mrt.team or self.config.team_name

        if mrt.version is None:
            if order:
                raise argparse.ArgumentTypeError(
                    "--sort argument is not valid for a model target, please specify a version."
                )
            if access_type or product_names:
                return self.api_client.registry.search.search_model(
                    org, team, target, access_type=access_type, product_names=product_names
                )
            return self.api_client.registry.search.search_model(org, team, target)

        if order is None:
            order = "SEMVER_DESC"
        try:
            version_list = self.list_versions(org, team, mrt.name, order=order)
        except ResourceNotFoundException:
            version_list = []
        version_list = filter_version_list(version_list, mrt.version)
        return version_list

    @extra_args
    def remove(self, target: str, default_yes: Optional[bool] = False):
        """Remove model or model version.

        Args:
            target: Full model name. org/[team/]name[:version]
            default_yes: Is confirmation enabled. Defaults to False.

        Raises:
            ResourceNotFoundException: If model is not found.
        """
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
        confirm_remove(target=target, default=default_yes)

        if mrt.version:
            try:
                self.remove_version(org_name=mrt.org, team_name=mrt.team, model_name=mrt.name, version=mrt.version)
            except ResourceNotFoundException:
                raise ResourceNotFoundException(f"Model version '{target}' could not be found.") from None
        else:
            try:
                self.remove_model(org_name=mrt.org, team_name=mrt.team, model_name=mrt.name)
            except ResourceNotFoundException:
                raise ResourceNotFoundException(f"Model '{target}' could not be found.") from None

    # END PUBLIC Functions

    @staticmethod
    def _get_models_endpoint(org: str = None, team: str = None, name: str = None) -> str:
        """Create a models endpoint.

        /v2[/org/<org>[/team/<team>[/<name>]]]/models
        """
        parts = [ENDPOINT_VERSION, format_org_team(org, team), "models", name]
        return "/".join([part for part in parts if part])

    def get_versions_endpoint(self, org: str = None, team: str = None, name: str = None, version: str = None) -> str:
        """Create a versions endpoint."""

        ep = self._get_models_endpoint(org=org, team=team, name=name)
        ep = "/".join([ep, "versions"])

        # version can be zero
        if version is not None:
            ep = "/".join([ep, str(version)])

        return ep

    def get_files_endpoint(
        self, org: str = None, team: str = None, name: str = None, version: str = None, file_: str = None
    ) -> str:
        """Create a files endpoint."""

        ep = self.get_versions_endpoint(org=org, team=team, name=name, version=version)
        ep = "/".join([ep, "files"])

        if file_:
            ep = "/".join([ep, str(file_)])

        return ep

    @staticmethod
    def get_multipart_files_endpoint(org: str = None, team: str = None) -> str:
        org_team = format_org_team(org, team)
        return f"{ENDPOINT_VERSION}/{org_team}/files/multipart"

    def get_direct_download_URL(
        self, name: str, version: str, org: str = None, team: str = None, filepath: str = None
    ) -> str:
        ep = f"{ENDPOINT_VERSION}/{format_org_team(org, team)}/models/{name}/{version}/files"
        if filepath:
            ep = f"{ep}?path={filepath}"
        return self.connection.create_full_URL(ep)

    def get_download_files_URL(self, name: str, version: str, org: str = None, team: str = None) -> str:
        """Since the file download goes through the AsyncDownload class and not the API Connection class, we need to
        return the full URL, not just the endpoint part.
        """
        org_team = format_org_team(org, team)
        ep = "/".join([ENDPOINT_VERSION, org_team, "models", name, "versions", version, "files"])
        return self.connection.create_full_URL(ep)

    def get(self, org_name: str, team_name: str, model_name: str) -> ModelResponse:
        """Get a model."""
        params = {"resolve-labels": "true"}
        resp = self.connection.make_api_request(
            "GET",
            self._get_models_endpoint(org=org_name, team=team_name, name=model_name),
            auth_org=org_name,
            auth_team=team_name,
            params=params,
            operation_name="get model",
        )
        return ModelResponse(resp)

    def _create(self, org_name: str, team_name: str, mcr: ModelCreateRequest) -> ModelResponse:
        resp = self.connection.make_api_request(
            "POST",
            self._get_models_endpoint(org=org_name, team=team_name),
            payload=mcr.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="create model",
        )

        return ModelResponse(resp).model

    def update_model(self, model_name: str, org_name: str, team_name: str, model_update_request: ModelUpdateRequest):
        resp = self.connection.make_api_request(
            "PATCH",
            self._get_models_endpoint(org=org_name, team=team_name, name=model_name),
            payload=model_update_request.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="update model",
        )
        return ModelResponse(resp).model

    def _validate_update_version(self, args_dict):
        """Helper Function for update given a version is provided"""
        invalid_args = [arg[1] for arg in self.model_only_args if args_dict[arg[0]] is not None]
        if invalid_args:
            raise argparse.ArgumentTypeError(f"Invalid argument(s) for model version: '{invalid_args}'")
        if all(args_dict[arg[0]] is None for arg in self.version_only_args):
            raise argparse.ArgumentTypeError(
                "No arguments provided for model version update request, there is nothing to do."
            )

    def _validate_update_model(self, args_dict):
        """Helper Function for update given a version is not provided"""
        invalid_args = [f"{arg[1]}" for arg in self.version_only_args if args_dict[arg[0]] is not None]
        if invalid_args:
            raise argparse.ArgumentTypeError(f"Invalid argument(s): {invalid_args}.  Only valid for model-versions.")
        if all(args_dict[arg[0]] is None for arg in self.model_only_args):
            raise argparse.ArgumentTypeError("No arguments provided for model update, there is nothing to do.")

    def remove_model(self, org_name: str, team_name: str, model_name: str):
        """Remove a model."""

        self.connection.make_api_request(
            "DELETE",
            self._get_models_endpoint(org=org_name, team=team_name, name=model_name),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="remove model",
        )

    def list_versions(
        self, org_name: str, team_name: str, model_name: str, page_size: int = PAGE_SIZE, order: str = None
    ) -> Iterable[ModelVersion]:
        """Get a list of versions for a model."""

        base_url = self.get_versions_endpoint(org=org_name, team=team_name, name=model_name)
        query = "{url}?page-size={page_size}".format(url=base_url, page_size=page_size)
        if order:
            query = "{q}&sort-order={sort}".format(q=query, sort=order)
        return chain(
            *[
                ModelVersionListResponse(res).modelVersions
                for res in pagination_helper_use_page_reference(
                    self.connection, query, org_name=org_name, team_name=team_name, operation_name="list model versions"
                )
                if ModelVersionListResponse(res).modelVersions
            ]
        )

    def get_version(self, org_name: str, team_name: str, model_name: str, version: str) -> ModelVersionResponse:
        """Get a model version."""

        resp = self.connection.make_api_request(
            "GET",
            self.get_versions_endpoint(org=org_name, team=team_name, name=model_name, version=version),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="get model version",
        )
        return ModelVersionResponse(resp)

    def create_version(
        self, org_name: str, team_name: str, model_name: str, version_create_request: ModelVersionCreateRequest
    ) -> ModelVersionResponse:
        """Create a model version."""

        resp = self.connection.make_api_request(
            "POST",
            self.get_versions_endpoint(org=org_name, team=team_name, name=model_name),
            payload=version_create_request.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="create model version",
        )
        return ModelVersionResponse(resp)

    def update_version(
        self,
        org_name: str,
        team_name: str,
        model_name: str,
        version: str,
        version_update_request: ModelVersionUpdateRequest,
        set_latest: bool = False,
    ) -> ModelVersionResponse:
        """Update a model version."""

        url = self.get_versions_endpoint(org=org_name, team=team_name, name=model_name, version=version)
        if set_latest:
            url += "?set-latest=true"

        resp = self.connection.make_api_request(
            "PATCH",
            url,
            payload=version_update_request.toJSON(),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="update model version",
        )
        return ModelVersionResponse(resp)

    def remove_version(self, org_name: str, team_name: str, model_name: str, version: str):
        """Remove a model version."""

        self.connection.make_api_request(
            "DELETE",
            self.get_versions_endpoint(org=org_name, team=team_name, name=model_name, version=version),
            auth_org=org_name,
            auth_team=team_name,
            operation_name="remove model version",
        )

    def list_files_for_model(
        self, model_name: str, model_version: str, org_name: str, team_name: str, page_size: int = PAGE_SIZE
    ):
        """Direct API call to get a list of files for a model."""
        base_url = self.get_files_endpoint(org=org_name, team=team_name, name=model_name, version=model_version)
        query = "{url}?page-size={page_size}".format(url=base_url, page_size=page_size)

        return chain(
            *[
                ModelVersionFileListResponse(res).modelFiles
                for res in pagination_helper_use_page_reference(
                    self.connection, query, org_name=org_name, team_name=team_name, operation_name="list model files"
                )
                if ModelVersionFileListResponse(res).modelFiles
            ]
        )

    @extra_args
    def list_files(self, target: str, org: Optional[str] = None, team: Optional[str] = None):
        """Get a list of files for a model."""
        self.config.validate_configuration(guest_mode_allowed=True)
        mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
        if not mrt.version:
            raise InvalidArgumentError("Cannot list files for a model target; please specify a version")

        org_name = mrt.org or org or self.connection.configuration.org_name
        team_name = mrt.team or team or self.connection.configuration.team_name
        return self.list_files_for_model(
            model_name=mrt.name, model_version=mrt.version, org_name=org_name, team_name=team_name
        )

    def _get_latest_version(self, target):
        try:
            model_resp = self.get(target.org, target.team, target.name)
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
        if not model_resp.model.latestVersionIdStr:
            raise NgcException("Target '{}' has no version available for download.".format(target))

        return model_resp.model.latestVersionIdStr

    def get_version_files(self, target, org_name, team_name):
        try:
            file_list = self.list_files(target, org_name, team_name)
        except ResourceNotFoundException:
            mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
            raise ResourceNotFoundException(
                f"Files could not be found for target '{mrt.name}:{mrt.version}'."
            ) from None
        return file_list

    def _update_upload_complete(self, org_name, team_name, model_name, version):
        version_req = ModelVersionUpdateRequest({"status": "UPLOAD_COMPLETE"})
        self.update_version(org_name, team_name, model_name, version, version_req)

        # These lists are used for argument validate.

    model_only_args = [
        ("application", "--application"),
        ("framework", "--framework"),
        ("model_format", "--format"),
        ("precision", "--precision"),
        ("short_description", "--short-desc"),
        ("display_name", "--display-name"),
        ("bias_filename", "--bias-filename"),
        ("explainability_filename", "--explainability-filename"),
        ("privacy_filename", "--privacy-filename"),
        ("safety_security_filename", "--safety-security-filename"),
        ("label", "--label"),
        ("logo", "--logo"),
        ("public_dataset_name", "--public-dataset-name"),
        ("public_dataset_link", "--public-dataset-link"),
        ("public_dataset_license", "--public-dataset-license"),
        ("built_by", "--built-by"),
        ("overview_filename", "--overview-filename"),
        ("publisher", "--publisher"),
        ("label_set", "--label-set"),
    ]
    version_only_args = [
        ("gpu_model", "--gpu-model"),
        ("memory_footprint", "--memory-footprint"),
        ("num_epochs", "--num-epochs"),
        ("batch_size", "--batch-size"),
        ("accuracy_reached", "--accuracy-reached"),
        ("description", "--description"),
        ("set_latest", "--set-latest"),
    ]


class GuestModelAPI(ModelAPI):
    def _get_models_endpoint(self, org: str = None, team: str = None, name: str = None):
        """Create a guest models endpoint.
        /{ENDPOINT_VERSION}/models[/<org>[/<team>[/<name>]]]
        """
        ep = f"{ENDPOINT_VERSION}/models"
        if org:
            ep = "/".join([ep, org])
        if team:
            ep = "/".join([ep, team])
        if name:
            ep = "/".join([ep, name])
        return ep

    def get_direct_download_URL(self, name: str, version: str, org: str = None, team: str = None, filepath: str = None):
        org_team = format_org_team(org, team)
        ep = "/".join([item for item in (ENDPOINT_VERSION, "models", org_team, name, version, "files") if item])
        if filepath:
            ep = f"{ep}?path={filepath}"
        return self.connection.create_full_URL(ep)
