#
# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from itertools import chain

from ngcbpc.api.configuration import Configuration
from ngcbpc.command.args_validation import (
    check_add_args_columns,
    check_valid_columns,
    ReadFile,
    SingleUseAction,
)
from ngcbpc.command.clicommand import CLICommand
from ngcbpc.constants import CANARY_ENV, CONFIG_TYPE, DISABLE_TYPE, ENABLE_TYPE
from ngcbpc.data.model.ArtifactListResponse import ArtifactListResponse
from ngcbpc.data.model.Collection import Collection
from ngcbpc.data.model.CollectionCategoryType import CollectionCategoryTypeEnum
from ngcbpc.data.model.CollectionCreateRequest import CollectionCreateRequest
from ngcbpc.data.model.CollectionListResponse import CollectionListResponse
from ngcbpc.data.model.CollectionResponse import CollectionResponse
from ngcbpc.data.model.CollectionUpdateRequest import CollectionUpdateRequest
from ngcbpc.errors import InvalidArgumentError, NgcAPIError
from ngcbpc.util.utils import confirm_remove, get_columns_help, get_environ_tag
from ngccli.modules.client import Client
from registry.api.utils import get_label_set_labels, SimpleRegistryTarget
from registry.command.publish import (
    ALLOW_GUEST_HELP,
    DISCOVERABLE_HELP,
    METADATA_HELP,
    PUBLIC_HELP,
    Publisher,
    VISIBILITY_HELP,
)
from registry.command.registry import RegistryCommand
from registry.constants import CollectionArtifacts
from registry.printer.collection import CollectionOutput, CollectionPrinter

PUBLISH_TYPE = ENABLE_TYPE if (get_environ_tag() <= CANARY_ENV) else DISABLE_TYPE


class CollectionSubCommand(RegistryCommand):
    CMD_NAME = "collection"
    HELP = "Collection Commands"
    DESC = "Collection Commands"
    CLI_HELP = ENABLE_TYPE

    collection_metavar = "org/[team/]collection_name"

    # Info help
    collection_target_arg_help = f"Collection. Format: {collection_metavar}."

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser

        self.printer = CollectionPrinter()
        self.config = Configuration()

        client = Client(api_key=self.config.app_key, base_url=self.config.base_url)
        self.collection_api = client.registry.collection
        self.label_set_api = client.registry.label_set
        self.search_api = client.registry.search
        self.publish_api = client.registry.publish
        self.resource_type = "COLLECTION"

    CREATE_HELP = "Create a collection."
    collection_create_arg_help = "Collection to create.  Format: Org/[team/]name."
    create_display_arg_help = "Human-readable name for the collection."
    create_format_arg_help = "Format of the collection."
    create_label_arg_help = "A label that applies to the collection.  Can be used multiple times."
    label_set_help = (
        "Name of the label set. Format: org/[team/]name. "
        "Labels from the label set will be combined with the label argument. Can be used multiple times. "
    )
    create_logo_arg_help = "A link to the logo for the collection."
    create_overview_arg_help = "A markdown file with an overview of the collection."
    create_owner_arg_help = "Name of the owner of this collection."
    create_publisher_arg_help = "The publishing organization."
    create_shortdesc_arg_help = "A brief description of the collection."
    create_image_arg_help = (
        "Name of an image to include in the collection.  Can be used multiple times.  Format: org/[team/]name."
    )
    create_model_arg_help = (
        "Name of a model to include in the collection.  Can be used multiple times.  Format: org/[team/]name."
    )
    create_resource_arg_help = (
        "Name of a resource to include in the collection.  Can be used multiple times.  Format: org/[team/]name."
    )
    create_chart_arg_help = (
        "Name of a chart to include in the collection.  Can be used multiple times.  Format: org/[team/]name."
    )
    category_choices = CollectionCategoryTypeEnum
    create_category_arg_help = f"Field for describing collection's use case. Choices are: {', '.join(category_choices)}"

    @CLICommand.command(help=CREATE_HELP, description=CREATE_HELP, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=collection_create_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=create_display_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments("--label-set", metavar="<label-set>", help=label_set_help, type=str, action="append")
    @CLICommand.arguments("--label", metavar="<label>", help=create_label_arg_help, type=str, action="append")
    @CLICommand.arguments(
        "--logo", metavar="<logo>", help=create_logo_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--overview-filename", metavar="<path>", help=create_overview_arg_help, type=str, action=ReadFile, default=""
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=create_owner_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher",
        metavar="<publisher>",
        help=create_publisher_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--short-desc",
        metavar="<desc>",
        help=create_shortdesc_arg_help,
        type=str,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--add-image", metavar="<image>", help=create_image_arg_help, action="append", dest="images", default=[]
    )
    @CLICommand.arguments(
        "--add-model", metavar="<model>", help=create_model_arg_help, action="append", dest="models", default=[]
    )
    @CLICommand.arguments(
        "--add-resource",
        metavar="<resource>",
        help=create_resource_arg_help,
        action="append",
        dest="resources",
        default=[],
    )
    @CLICommand.arguments(
        "--add-chart", metavar="<chart>", help=create_chart_arg_help, action="append", dest="charts", default=[]
    )
    @CLICommand.arguments(
        "--category",
        metavar="<category>",
        help=create_category_arg_help,
        type=str.upper,
        required=True,
        action=SingleUseAction,
        choices=category_choices,
    )
    def create(self, args):
        """Create a collection"""
        self.config.validate_configuration(guest_mode_allowed=False)

        reg_target = SimpleRegistryTarget(args.target, org_required=True, name_required=True)

        collection_request = CollectionCreateRequest(
            {
                "name": reg_target.name,
                "displayName": args.display_name,
                "labels": None,
                "labelsV2": get_label_set_labels(self.label_set_api, self.resource_type, args.label_set, args.label),
                "logo": args.logo,
                "description": args.overview_filename,  # Read from the markdown file
                "builtBy": args.built_by,
                "publisher": args.publisher,
                "shortDescription": args.short_desc,
                "category": args.category,
            }
        )
        artifacts_request = self._get_artifacts_request_dict(args.images, args.charts, args.models, args.resources)

        collection_response = self.collection_api.create_collection(
            collection_request, reg_target.org, team=reg_target.team
        )
        artifacts_response, errors = self.collection_api.make_artifacts_requests(
            artifacts_request, reg_target.org, reg_target.name, team=reg_target.team, verb="PUT"
        )
        collection_response = CollectionResponse(collection_response)
        if not collection_response.collection:
            collection_response.collection = Collection()

        self.printer.print_collection_create_results(collection_response.collection, artifacts_response, errors)
        for _, error_list in errors.items():
            if error_list:
                raise NgcAPIError("Create encountered errors.")

    INFO_HELP = "Display information about a collection in the registry."

    @staticmethod
    def _get_artifacts_request_dict(images, charts, models, resources):
        """Return a artifact request dict with elements consisting of the tuple (name, api_target)"""
        header_apitarget_artifacts = (
            ("Images", CollectionArtifacts["IMAGES"].value, images),
            ("Charts", CollectionArtifacts["HELM_CHARTS"].value, charts),
            ("Models", CollectionArtifacts["MODELS"].value, models),
            ("Resources", CollectionArtifacts["RESOURCES"].value, resources),
        )

        request_dict = {}
        for header, apitarget, artifacts in header_apitarget_artifacts:
            request_dict[header] = set()
            for artifact in artifacts:
                artifact_target = SimpleRegistryTarget(artifact, org_required=True, name_required=True)
                request_dict[header].add((artifact_target.org, artifact_target.team, artifact_target.name, apitarget))

        return request_dict

    @CLICommand.command(help=INFO_HELP, description=INFO_HELP)
    @CLICommand.arguments("target", metavar="<target>", help=collection_target_arg_help, type=str, default=None)
    def info(self, args):
        """Get information about a collection"""
        self.config.validate_configuration(guest_mode_allowed=True)
        reg_target = SimpleRegistryTarget(args.target, org_required=True, name_required=True)
        has_key = bool(self.config.app_key)

        # Reponses are asynchronous and come in any order, need to construct into relevant objects
        collection = CollectionResponse()
        artifacts_dict = {"Images": [], "Charts": [], "Models": [], "Resources": []}
        for response in self.collection_api.get_info(reg_target.org, reg_target.team, reg_target.name, has_key=has_key):
            if "collection" in response:
                collection = CollectionResponse(response)
            elif "artifacts" in response and response["artifacts"]:
                artifacts = ArtifactListResponse(response).artifacts
                if artifacts[0].artifactType == "MODEL":
                    artifacts_dict["Models"] = artifacts
                elif artifacts[0].artifactType == "REPOSITORY":
                    artifacts_dict["Images"] = artifacts
                elif artifacts[0].artifactType == "HELM_CHART":
                    artifacts_dict["Charts"] = artifacts
                elif artifacts[0].artifactType == "MODEL_SCRIPT":
                    artifacts_dict["Resources"] = artifacts
                else:
                    raise ValueError(f"Unrecognized response type '{artifacts[0].artifactType}'")

        self.printer.print_collection_info(collection.collection, artifacts_dict)

    LIST_HELP = "Display a list of available collections in the registry."
    collection_list_arg_help = (
        "Filter the search by allowing wildcards for Collection(s). "
        f"Format: {collection_metavar}. "
        f'To target Collection(s), use "{collection_metavar}". '
        'Org, team, and name support the wildcards "*" and "?". '
        'Examples:  "my_org/my_collection" - target my_collection in my_org namespace. '
        '"my_org/my_team/my_collection" - target my_collection in my_org/my_team namespace. '
        '"my_org/my_team/*" - target all collections in my_org/my_team namespace. '
        '"my_org/my_collection*" - target collections starting with my_collection in my_org namespace. '
    )
    columns_dict = CollectionOutput.PROPERTY_HEADER_MAPPING
    column_default = ("name", "Name")
    columns_help = get_columns_help(columns_dict, column_default)

    @CLICommand.command(help=LIST_HELP, description=LIST_HELP)
    @CLICommand.arguments(
        "target", metavar="<target>", help=collection_list_arg_help, type=str, nargs="?", default=None
    )
    @CLICommand.arguments(
        "--column",
        metavar="<column>",
        help=columns_help,
        default=None,
        action="append",
        type=lambda value, columns_dict=columns_dict: check_valid_columns(value, columns_dict),
    )
    def list(self, args):
        """List collections"""
        self.config.validate_configuration(guest_mode_allowed=True, csv_allowed=True)

        # If target specified then need to parse and validate
        if args and args.target:
            srt = SimpleRegistryTarget(args.target, name_required=True, glob_allowed=True)
            target = args.target
            org = srt.org or args.org or self.config.org_name
            team = srt.team or args.team or self.config.team_name
        else:
            target = "*"
            org = args.org or self.config.org_name
            team = args.team or self.config.team_name

        check_add_args_columns(args.column, CollectionSubCommand.column_default)
        pages_gen = self.search_api.search_collections(org, team, target)
        self.printer.print_collection_list(pages_gen, args.column)

    UPDATE_HELP = "Update a collection."

    collection_remove_image_help = "An image to be removed from the collection."
    collection_remove_model_help = "A model to be removed from the collection."
    collection_remove_resource_help = "A resource to be removed from the collection."
    collection_remove_chart_help = "A chart to be removed from the collection."

    @CLICommand.command(help=UPDATE_HELP, description=UPDATE_HELP, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=collection_create_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=create_display_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments("--label-set", metavar="<label-set>", help=label_set_help, type=str, action="append")
    @CLICommand.arguments("--label", metavar="<label>", help=create_label_arg_help, type=str, action="append")
    @CLICommand.arguments(
        "--logo", metavar="<logo<", help=create_logo_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--overview-filename", metavar="<path>", help=create_overview_arg_help, type=str, action=ReadFile, default=None
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=create_owner_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher",
        metavar="<publisher>",
        help=create_publisher_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--short-desc", metavar="<desc>", help=create_shortdesc_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--add-image", metavar="<image>", help=create_image_arg_help, action="append", dest="images", default=[]
    )
    @CLICommand.arguments(
        "--add-model", metavar="<model>", help=create_model_arg_help, action="append", dest="models", default=[]
    )
    @CLICommand.arguments(
        "--add-resource",
        metavar="<resource>",
        help=create_resource_arg_help,
        action="append",
        dest="resources",
        default=[],
    )
    @CLICommand.arguments(
        "--add-chart", metavar="<chart>", help=create_chart_arg_help, action="append", dest="charts", default=[]
    )
    @CLICommand.arguments(
        "--category",
        metavar="<category>",
        help=create_category_arg_help,
        type=str.upper,
        action=SingleUseAction,
        choices=category_choices,
    )
    @CLICommand.arguments(
        "--remove-image",
        metavar="<image>",
        help=collection_remove_image_help,
        action="append",
        default=[],
        dest="remove_images",
    )
    @CLICommand.arguments(
        "--remove-model",
        metavar="<model>",
        help=collection_remove_model_help,
        action="append",
        default=[],
        dest="remove_models",
    )
    @CLICommand.arguments(
        "--remove-resource",
        metavar="<resource>",
        help=collection_remove_resource_help,
        action="append",
        default=[],
        dest="remove_resources",
    )
    @CLICommand.arguments(
        "--remove-chart",
        metavar="<chart>",
        help=collection_remove_chart_help,
        action="append",
        default=[],
        dest="remove_charts",
    )
    def update(self, args):
        """Update a collection"""
        self.config.validate_configuration(guest_mode_allowed=False)

        reg_target = SimpleRegistryTarget(args.target, org_required=True, name_required=True)
        collection_request = CollectionUpdateRequest(
            {
                "displayName": args.display_name,
                "labels": None,
                "labelsV2": get_label_set_labels(self.label_set_api, self.resource_type, args.label_set, args.label),
                "logo": args.logo,
                "description": args.overview_filename,  # Read from the markdown file
                "builtBy": args.built_by,
                "publisher": args.publisher,
                "shortDescription": args.short_desc,
                "category": args.category,
            }
        )
        add_artifacts_request = self._get_artifacts_request_dict(args.images, args.charts, args.models, args.resources)
        remove_artifacts_request = self._get_artifacts_request_dict(
            args.remove_images, args.remove_charts, args.remove_models, args.remove_resources
        )

        collection_response = CollectionResponse(
            self.collection_api.patch_collection(
                reg_target.name, collection_request, reg_target.org, team=reg_target.team
            )
        )
        _, add_errors = self.collection_api.make_artifacts_requests(
            add_artifacts_request, reg_target.org, reg_target.name, team=reg_target.team, verb="PUT"
        )
        _, remove_errors = self.collection_api.make_artifacts_requests(
            remove_artifacts_request, reg_target.org, reg_target.name, team=reg_target.team, verb="DELETE"
        )

        # An info call on all artifacts is necessary because adds/removes may not encompass other artifacts that exist.
        # This duplicates the collection info call but can be optimized later
        self.info(args)
        self.printer.print_artifact_put_errors(add_errors, collection_response.collection.name)
        self.printer.print_artifact_delete_errors(remove_errors, collection_response.collection.name)

        for _, error_list in chain(add_errors.items(), remove_errors.items()):
            if error_list:
                raise NgcAPIError("Update encountered errors.")

    SHARE_HELP = "Share a collection with a team or org. If a team is set, it will be shared with that team by default."

    REMOVE_HELP = "Remove a collection."
    remove_target_arg_help = f"Collection to remove. Format: {collection_metavar}"
    remove_yes_arg_help = "Automatically confirm removal to interactive prompts."

    @CLICommand.command(help=REMOVE_HELP, description=REMOVE_HELP, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=remove_target_arg_help, type=str)
    @CLICommand.arguments("-y", "--yes", help=remove_yes_arg_help, dest="default_yes", action="store_true")
    def remove(self, args):
        """Remove a collection"""
        self.config.validate_configuration(guest_mode_allowed=False)
        reg_target = SimpleRegistryTarget(args.target, org_required=True, name_required=True)
        confirm_remove(target=args.target, default=args.default_yes)
        _ = self.collection_api.remove(reg_target.org, reg_target.name, team=reg_target.team)
        self.printer.print_ok(f"Successfully removed collection '{args.target}'.")

    FIND_HELP = "Get a list of collections containing the specified artifact."
    find_artifact_choices = ["MODEL", "CHART", "RESOURCE", "IMAGE"]
    find_artifact_type = f"Type of artifact to look for.  Choices: {', '.join(find_artifact_choices)}"
    find_artifact_target = "Target artifact to look for.  Format: org/[team/]artifact_name."

    @CLICommand.command(help=FIND_HELP, description=FIND_HELP)
    @CLICommand.arguments(
        "artifact_type",
        metavar="<artifact_type>",
        help=find_artifact_type,
        type=str.upper,
        choices=find_artifact_choices,
    )
    @CLICommand.arguments("artifact_target", metavar="<artifact_target>", help=find_artifact_target)
    def find(self, args):
        """Get a list of collections containing the specified artifact."""
        self.config.validate_configuration(guest_mode_allowed=True)
        has_key = bool(self.config.app_key)
        reg_target = SimpleRegistryTarget(args.artifact_target, org_required=True, name_required=True)

        collections = []
        for page in self.collection_api.find(
            reg_target.org,
            CollectionArtifacts[args.artifact_type].value,
            reg_target.name,
            team=reg_target.team,
            has_key=has_key,
        ):
            response_list = CollectionListResponse(page)
            collections.extend(response_list.collections)
        self.printer.print_collection_list([collections])

    publish_help = "Publish a collection from the NGC model registry to catalog."
    publish_arg_help = f"The the target collection you want to publish to. Format: {collection_metavar}"
    source_help = f"The source collection you want to publish. Format: {collection_metavar}"
    allow_guest_help = "Open up permissions of the published object to be accessible by unauthenticated users."
    discoverable_help = "Open up permission of the publish object to be discoverable by searches."

    @CLICommand.command(help=publish_help, description=publish_help, feature_tag=PUBLISH_TYPE)
    @CLICommand.arguments("target", metavar=collection_metavar, help=publish_help, type=str)
    @CLICommand.arguments("--source", metavar=collection_metavar, help=source_help, type=str, default=None)
    @CLICommand.arguments("--allow-guest", help=ALLOW_GUEST_HELP, action="store_true", default=False)
    @CLICommand.arguments("--discoverable", help=DISCOVERABLE_HELP, action="store_true", default=False)
    @CLICommand.arguments("--public", help=PUBLIC_HELP, action="store_true", default=False)
    @CLICommand.arguments("--metadata-only", help=METADATA_HELP, action="store_true", default=False)
    @CLICommand.arguments("--visibility-only", help=VISIBILITY_HELP, action="store_true", default=False)
    @CLICommand.mutex(["metadata_only"], ["visibility_only"])
    def publish(self, args):
        self.config.validate_configuration(guest_mode_allowed=False)
        source = SimpleRegistryTarget(args.source)
        if args.visibility_only:
            if args.source:
                raise InvalidArgumentError(
                    "You cannot specify a `--source` argument when making a `visibility_only` publishing request"
                )
            # Use the target value as the source. They aren't used, but are needed for the Publishing object.
            source = SimpleRegistryTarget(args.target)
        else:
            if not args.source:
                raise InvalidArgumentError("You must specify a `--source` argument")
            source = SimpleRegistryTarget(args.source)
        target = SimpleRegistryTarget(args.target)
        # collection version is not yet available
        #                    |  metadata_only T      |      metadata_only F
        # visibility_only T  |     not allowed       |      call /share
        # visibility_only F  |  call /metadata/copy  |  call /metadata/copy + /share
        #
        args.version_only = False
        try:
            publisher = Publisher(source, target, self.publish_api, "collections", args)
        except InvalidArgumentError as e:
            self.printer.print_error(e)
            return
        publisher.publish()
        self.printer.print_ok(f"Successfully published collection {args.target}")
