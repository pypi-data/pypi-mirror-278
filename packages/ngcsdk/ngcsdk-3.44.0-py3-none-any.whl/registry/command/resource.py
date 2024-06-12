#
# Copyright (c) 2018-2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import logging

from ngcbpc.api.configuration import Configuration
from ngcbpc.command.args_validation import (
    check_add_args_columns,
    check_url,
    check_valid_columns,
    SingleUseAction,
)
from ngcbpc.command.clicommand import CLICommand
from ngcbpc.constants import (
    CANARY_ENV,
    CONFIG_TYPE,
    DISABLE_TYPE,
    ENABLE_TYPE,
    PRODUCT_NAMES,
)
from ngcbpc.data.model.ApplicationType import ApplicationTypeEnum
from ngcbpc.data.model.FrameworkType import FrameworkTypeEnum
from ngcbpc.data.model.PrecisionType import PrecisionTypeEnum
from ngcbpc.data.model.RecipeResponse import RecipeResponse
from ngcbpc.data.model.RecipeVersionResponse import RecipeVersionResponse
from ngcbpc.data.registry.AccessTypeEnum import AccessTypeEnum
from ngcbpc.errors import (
    InvalidArgumentError,
    NgcException,
    ResourceFilesNotFoundException,
    ResourceNotFoundException,
)
from ngcbpc.printer.transfer import TransferPrinter
from ngcbpc.util.utils import get_columns_help, get_environ_tag
from ngccli.modules.client import Client
from registry.api.resources import ResourceAPI
from registry.api.utils import ModelRegistryTarget
from registry.command.publish import (
    ACCESS_TYPE_HELP,
    ALLOW_GUEST_HELP,
    DISCOVERABLE_HELP,
    METADATA_HELP,
    PRODUCT_HELP,
    PUBLIC_HELP,
    Publisher,
    VERSION_ONLY_HELP,
    VISIBILITY_HELP,
)
from registry.command.registry import RegistryCommand
from registry.printer.resource import ResourcePrinter

logger = logging.getLogger(__name__)

NOTES_ARG = "--release-notes-filename"
PERFORMANCE_ARG = "--performance-filename"
ADVANCED_ARG = "--advanced-filename"
QUICK_START_ARG = "--quick-start-guide-filename"
SETUP_ARG = "--setup-filename"
OVERVIEW_ARG = "--overview-filename"
PUBLISH_TYPE = ENABLE_TYPE if (get_environ_tag() <= CANARY_ENV) else DISABLE_TYPE


class ResourceSubCommand(RegistryCommand):
    CMD_NAME = "resource"
    HELP = "Resource Commands"
    DESC = "Resource Commands"
    CLI_HELP = ENABLE_TYPE

    # pylint: disable=no-self-use

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = Configuration()
        self.client = Client(api_key=self.config.app_key, base_url=self.config.base_url)
        self.api: ResourceAPI = self.client.registry.resource
        self.search_api = self.client.registry.search
        self.label_set_api = self.client.registry.label_set
        self.publish_api = self.client.registry.publish
        self.printer = ResourcePrinter()
        self.transfer_printer = TransferPrinter()
        self.resource_type = "RECIPE"

    if bool(Configuration().product_names):
        product_names = Configuration().product_names
    else:
        product_names = PRODUCT_NAMES

    resource_and_version_args = [
        ("performance_filename", "--performance-filename"),
        ("quick_start_guide_filename", "--quick-start-guide-filename"),
        ("setup_filename", "--setup-filename"),
    ]

    # These lists are used for argument validate.
    resource_only_args = [
        ("application", "--application"),
        ("framework", "--framework"),
        ("model_format", "--format"),
        ("precision", "--precision"),
        ("short_desc", "--short-desc"),
        # optional
        ("display_name", "--display-name"),
        ("advanced_filename", "--advanced-filename"),
        ("label", "--label"),
        ("logo", "--logo"),
        ("overview_filename", "--overview-filename"),
        ("public_dataset_name", "--public-dataset-name"),
        ("public_dataset_link", "--public-dataset-link"),
        ("public_dataset_license", "--public-dataset-license"),
        ("built_by", "--built-by"),
        ("publisher", "--publisher"),
        ("label_set", "--label-set"),
    ]

    version_only_args = [
        ("accuracy_reached", "--accuracy-reached"),
        ("batch_size", "--batch-size"),
        ("desc", "--desc"),
        ("gpu_model", "--gpu-model"),
        ("memory_footprint", "--memory-footprint"),
        ("num_epochs", "--num-epochs"),
        ("release_notes_filename", "--release-notes-filename"),
    ]

    LIST_HELP = "List resources or resource version(s)."

    TARGET_HELP = (
        "Resource or resource version.  Format: org/[team/]resource_name[:version]. "
        'To target a resource version, use "org/[team/]name:version". '
        'To target a resource, use "org/[team/]name".'
    )

    UPLOAD_TARGET_VERSION_HELP = "Resource version. Format: org/[team/]resource_name:version."

    LIST_TARGET_HELP = (
        "Filter the search by allowing wildcards for resources "
        "or resource version(s). "
        "Format: [org/[team/]]name[:version]. "
        'To target resource version(s), use "[org/[team/]]name:version". '
        'To target resources use "[org/[team/]]name". '
        'Both name and version support the wildcards "*" and "?". '
        "Version also supports character expressions ([a-z], [!ab], etc.). "
        'Examples:  "my_org/my_resource" - target my_resource in my_org namespace. '
        '"my_org/my_team/my_resource" - target my_resource in my_org/my_team namespace. '
        '"my_org/my_team/*" - target all resources in my_org/my_team namespace. '
        '"my_org/my_resource*" '
        "- target all resource versions for my_resource in my_org namespace. "
        '"my_org/my_resource:[1-5]" '
        "- target versions 1-5 for my_resource in my_org namespace."
    )

    columns_dict = {
        "name": "Name",
        "org": "Org",
        "team": "Team",
        "description": "Description",
        "updated": "Last Modified",
        "created": "Created Date",
        "shared": "Shared",
        "size": "File Size",
        "latest_version": "Latest Version",
        "version": "Version",
        "application": "Application",
        "framework": "Framework",
        "precision": "Precision",
        "permission": "Permission",
        "accuracy": "Accuracy",
        "epochs": "Epochs",
        "batch": "Batch Size",
        "gpu": "GPU Model",
        "memory": "Memory Footprint",
        "status": "Status",
        "labels": "Labels",
    }
    columns_default_resource = ("repository", "Repository")
    columns_default_version = ("latest_version", "Latest Version")
    columns_help = get_columns_help(columns_dict, [columns_default_resource, columns_default_version])
    ACCESS_TYPE_LIST_HELP = "Filter the list of resources to only resources that have specified access type."
    PRODUCT_NAME_LIST_HELP = (
        "Filter the list of resources to only resources that are under the product name. Multiple product-name"
        f" arguments are allowed. Choose from: {', '.join(product_names)}"
    )

    @CLICommand.arguments("target", metavar="<target>", help=LIST_TARGET_HELP, type=str, nargs="?", default=None)
    # pylint:disable=undefined-variable
    @CLICommand.arguments(
        "--column",
        metavar="<column>",
        help=columns_help,
        default=None,
        action="append",
        type=lambda value, columns_dict=columns_dict: check_valid_columns(value, columns_dict),
    )
    @CLICommand.arguments(
        "--access-type",
        metavar="<access_type>",
        help=ACCESS_TYPE_LIST_HELP,
        choices=AccessTypeEnum,
        default=None,
    )
    @CLICommand.arguments(
        "--product-name",
        metavar="<product_name>",
        help=PRODUCT_NAME_LIST_HELP,
        default=None,
        action="append",
    )
    @CLICommand.command(help=LIST_HELP, description=LIST_HELP)
    def list(self, args):
        mrt = ModelRegistryTarget(args.target, glob_allowed=True)
        product_names_args = args.product_name if args.product_name else []
        product_names_args = [name.replace("-", "_") for name in product_names_args]
        resource_list = self.api.list(
            target=args.target, access_type=args.access_type, product_names=product_names_args
        )

        if mrt.version is None:
            self.printer.print_resource_list(resource_list, columns=args.column)
        else:
            check_add_args_columns(args.column, ResourceSubCommand.columns_default_version)
            self.printer.print_resource_version_list(resource_list, columns=args.column)

    INFO_HELP = "Retrieve metadata for a resource or resource version."

    @CLICommand.command(help=INFO_HELP, description=INFO_HELP)
    @CLICommand.arguments("target", metavar="<target>", help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--files", help="List files in addition to details for a version.", dest="list_files", action="store_true"
    )
    def info(self, args):
        mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)

        if mrt.version is None:
            resp: RecipeResponse = self.api.info(target=args.target, list_files=args.list_files)
            self.printer.print_resource(resp.recipe)
        else:
            resp: RecipeVersionResponse = self.api.info(target=args.target, list_files=args.list_files)
            # TODO: Collapse List Files into Info API function
            file_list = self.get_version_files(mrt.org, mrt.team, mrt.name, mrt.version) if args.list_files else None
            self.printer.print_resource_version(version=resp.recipeVersion, resource=resp.recipe, file_list=file_list)

    def get_version_files(self, org_name, team_name, name, version):
        try:
            file_list = self.api.list_files(org_name, team_name, name, version)
        except ResourceNotFoundException:
            raise ResourceFilesNotFoundException(f"Files could not be found for target '{name}:{version}'.") from None
        return file_list

    # resource attributes
    TARGET_ARG_HELP = "Resource.  Format: org/[team/]resource_name."
    RESOURCE_METAVAR_REQ_VERSION = "org/[team/]resource_name:version"
    APPLICATION_HELP = "Application of the resource. Allowed values: {}.".format(", ".join(ApplicationTypeEnum))
    FRAMEWORK_HELP = "Framework used in the resource. Allowed values: {}.".format(", ".join(FrameworkTypeEnum))
    FORMAT_HELP = "Format of the model (checkpoint) generated by the resource."
    PRECISION_HELP = "Precision supported by the resource. Allowed values: {}.".format(", ".join(PrecisionTypeEnum))
    SHORT_DESC_HELP = "Short description."
    DISPLAY_NAME_HELP = "Display name."
    LABEL_SET_HELP = (
        "Name of the label set. Format: org/[team/]name. "
        "Labels from the label set will be combined with the label argument. Can be used multiple times. "
    )
    LABEL_HELP = (
        "Label for the resource. To specify more than one label, use multiple --label arguments. "
        "Labels from the given label sets will be combined with the label argument."
    )
    LOGO_HELP = "URL for the resource logo image."
    PUBLIC_DATASET_NAME_HELP = "Name of public dataset used."
    PUBLIC_DATASET_LINK_HELP = "Link to public dataset used."
    PUBLIC_DATASET_LICENSE_HELP = "License for public dataset used."
    BUILT_BY_HELP = "Builder of the resource."
    PUBLISHER_HELP = "Publisher of the resource."
    # Note: resource-level overview attribute is stored in description in the schema.
    # UI diverged and we need to quickly match them now.
    OVERVIEW_HELP = "Overview. Provide the path to a file that contains the overview for the resource."

    # common resource and resource version attributes
    ADVANCED_HELP = 'Advanced guide. Provide the path to a file that contains the "Advanced Guide" for the resource.'
    PERFORMANCE_HELP = (
        "Performance data. Provide the path to a file that contains the performance data for the resource."
    )
    QUICK_START_HELP = (
        'Quick start information. Provide the path to a file that contains the "Quick Start Guide" '
        "information for the resource."
    )
    SETUP_HELP = "Setup instructions. Provide the path to a file that contains the setup instructions for the resource."

    # version attributes
    # Note: both script and version schema have a description.  The version level description is not
    # used anywhere and can be removed.  The script level description is displayed as Overview in UI
    DESC_HELP = "Full description of resource version."
    ACCURACY_REACHED_HELP = "Accuracy reached with resource version."
    BATCH_SIZE_HELP = "The batch size of the resource version."
    GPU_HELP = "The GPU used to train the resource version."
    MEMORY_HELP = "The memory footprint of the resource version."
    NUM_EPOCHS_HELP = "The number of epochs for the resource version."
    NOTES_HELP = "Release notes. Provide the path to a file that contains the release notes for the resource."

    # NOT RELATED TO SCRIPTS
    SOURCE_HELP = (
        "Provide source directory of the resource or path of single file to be uploaded; if omitted, current "
        "directory will be used."
    )

    CREATE_HELP = "Create a resource."

    @CLICommand.command(help=CREATE_HELP, description=CREATE_HELP, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=TARGET_ARG_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--application",
        metavar="<app>",
        required=True,
        help=APPLICATION_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--framework",
        metavar="<fwk>",
        required=True,
        help=FRAMEWORK_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--format",
        metavar="<fmt>",
        required=True,
        help=FORMAT_HELP,
        dest="model_format",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--precision",
        metavar="<prec>",
        required=True,
        help=PRECISION_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--short-desc",
        metavar="<desc>",
        required=True,
        help=SHORT_DESC_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        OVERVIEW_ARG, metavar="<path>", help=OVERVIEW_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=DISPLAY_NAME_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments("--label", metavar="<label>", help=LABEL_HELP, action="append", type=str, default=None)
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=LABEL_SET_HELP, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--logo", metavar="<url>", help=LOGO_HELP, type=check_url, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--public-dataset-name",
        metavar="<name>",
        help=PUBLIC_DATASET_NAME_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-link",
        metavar="<url>",
        help=PUBLIC_DATASET_LINK_HELP,
        type=check_url,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-license",
        metavar="<lcs>",
        help=PUBLIC_DATASET_LICENSE_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=BUILT_BY_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher", metavar="<name>", help=PUBLISHER_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        ADVANCED_ARG, metavar="<path>", help=ADVANCED_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        PERFORMANCE_ARG, metavar="<path>", help=PERFORMANCE_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        QUICK_START_ARG, metavar="<path>", help=QUICK_START_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(SETUP_ARG, metavar="<path>", help=SETUP_HELP, type=str, default=None, action=SingleUseAction)
    def create(self, args):
        """Create a new resource"""
        resource = self.api.create(
            target=args.target,
            application=args.application,
            framework=args.framework,
            model_format=args.model_format,
            precision=args.precision,
            short_description=args.short_desc,
            overview_filename=args.overview_filename,
            advanced_filename=args.advanced_filename,
            performance_filename=args.performance_filename,
            quick_start_guide_filename=args.quick_start_guide_filename,
            setup_filename=args.setup_filename,
            display_name=args.display_name,
            label=args.label,
            label_set=args.label_set,
            logo=args.logo,
            public_dataset_name=args.public_dataset_name,
            public_dataset_license=args.public_dataset_license,
            public_dataset_link=args.public_dataset_link,
            built_by=args.built_by,
            publisher=args.publisher,
        )
        self.printer.print_head("Successfully created resource '{}'.".format(args.target))
        self.printer.print_resource(resource)

    UPDATE_HELP = "Update a resource or resource version."

    @CLICommand.command(help=UPDATE_HELP, description=UPDATE_HELP, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=TARGET_HELP, type=str, default=None)
    # resource specific
    @CLICommand.arguments(
        "--application", metavar="<app>", help=APPLICATION_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--framework", metavar="<fwk>", help=FRAMEWORK_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--format",
        metavar="<fmt>",
        help=FORMAT_HELP,
        dest="model_format",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--precision", metavar="<prec>", help=PRECISION_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--short-desc", metavar="<desc>", help=SHORT_DESC_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        OVERVIEW_ARG, metavar="<path>", help=OVERVIEW_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=DISPLAY_NAME_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments("--label", metavar="<label>", help=LABEL_HELP, action="append", type=str, default=None)
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=LABEL_SET_HELP, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--logo", metavar="<url>", help=LOGO_HELP, type=check_url, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--public-dataset-name",
        metavar="<name>",
        help=PUBLIC_DATASET_NAME_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-link",
        metavar="<url>",
        help=PUBLIC_DATASET_LINK_HELP,
        type=check_url,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-license",
        metavar="<lcs>",
        help=PUBLIC_DATASET_LICENSE_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=BUILT_BY_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher", metavar="<name>", help=PUBLISHER_HELP, type=str, default=None, action=SingleUseAction
    )
    # resource version specific
    @CLICommand.arguments("--desc", metavar="<desc>", help=DESC_HELP, type=str, default=None, action=SingleUseAction)
    @CLICommand.arguments(
        "--accuracy-reached",
        metavar="<accuracy>",
        help=ACCURACY_REACHED_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--batch-size", metavar="<size>", help=BATCH_SIZE_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--gpu-model", metavar="<model>", help=GPU_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--memory-footprint", metavar="<footprint>", help=MEMORY_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--num-epochs", metavar="<num>", help=NUM_EPOCHS_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(NOTES_ARG, metavar="<path>", help=NOTES_HELP, type=str, default=None, action=SingleUseAction)
    # common
    @CLICommand.arguments(
        ADVANCED_ARG, metavar="<path>", help=ADVANCED_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        PERFORMANCE_ARG, metavar="<path>", help=PERFORMANCE_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        QUICK_START_ARG, metavar="<path>", help=QUICK_START_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(SETUP_ARG, metavar="<path>", help=SETUP_HELP, type=str, default=None, action=SingleUseAction)
    def update(self, args):
        """Update an existing resource"""
        _mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)
        resource = self.api.update(
            target=args.target,
            application=args.application,
            framework=args.framework,
            model_format=args.model_format,
            precision=args.precision,
            short_description=args.short_desc,
            overview_filename=args.overview_filename,
            advanced_filename=args.advanced_filename,
            performance_filename=args.performance_filename,
            quick_start_guide_filename=args.quick_start_guide_filename,
            setup_filename=args.setup_filename,
            release_notes_filename=args.release_notes_filename,
            display_name=args.display_name,
            label=args.label,
            label_set=args.label_set,
            logo=args.logo,
            public_dataset_name=args.public_dataset_name,
            desc=args.desc,
            public_dataset_license=args.public_dataset_license,
            public_dataset_link=args.public_dataset_link,
            built_by=args.built_by,
            publisher=args.publisher,
            num_epochs=args.num_epochs,
            batch_size=args.batch_size,
            accuracy_reached=args.accuracy_reached,
            gpu_model=args.gpu_model,
            memory_footprint=args.memory_footprint,
        )

        if _mrt.version is None:
            self.printer.print_head("Successfully updated resource'{}'.".format(args.target))
            self.printer.print_resource(resource)
        else:
            self.printer.print_head(f"Successfully updated resource version '{args.target}'.")
            self.printer.print_resource_version(version=resource.recipeVersion, resource=resource.recipe)

    REMOVE_HELP = "Remove a resource or resource version."

    @CLICommand.command(help=REMOVE_HELP, description=REMOVE_HELP, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "-y",
        "--yes",
        help="Automatically say yes to all interactive questions.",
        dest="default_yes",
        action="store_true",
    )
    def remove(self, args):
        """Delete an existing resource or resource version"""
        mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)
        self.api.remove(target=args.target, default_yes=args.default_yes)

        if mrt.version is None:
            self.printer.print_ok("Successfully removed resource '{}'.".format(args.target))
        else:
            self.printer.print_ok("Successfully removed resource version '{}'.".format(args.target))

    DL_VER_HELP = "Download a resource version."
    DL_TARGET_HELP = (
        "Resource version. Format: org/[team/]resource_name[:version].  "
        "If no version specified, the latest version will be targeted."
    )

    @CLICommand.command(name="download-version", help=DL_VER_HELP, description=DL_VER_HELP)
    @CLICommand.arguments("target", metavar="<target>", help=DL_TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--dest",
        metavar="<path>",
        help="Provide a destination to download the resource.  Default:  .",
        type=str,
        default="",
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--file",
        metavar="<wildcard>",
        action="append",
        help=(
            "Specify individual files to download from the resource.\n"
            "Supports standard Unix shell-style wildcards like (?, [abc], [!a-z], etc..) "
            "May be used multiple times in the same command."
        ),
    )
    @CLICommand.arguments(
        "--exclude",
        metavar="<wildcard>",
        action="append",
        help=(
            "Exclude files or directories from the downloaded resource.\n"
            "Supports standard Unix shell-style wildcards like (?, [abc], [!a-z], etc..). "
            "May be used multiple times in the same command."
        ),
    )
    def download_version(self, args):
        """Download a specific resource version"""
        self.api.download_version(
            target=args.target, destination=args.dest, file_patterns=args.file, exclude_patterns=args.exclude
        )

    def _get_latest_version(self, target):
        try:
            resp = self.api.get(target.org, target.team, target.name)
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
        if not resp.recipe.latestVersionIdStr:
            raise NgcException("Target '{}' has no version available for download.".format(target))
        return resp.recipe.latestVersionIdStr

    UL_VER_HELP = "Upload a resource version."

    @CLICommand.command(name="upload-version", help=UL_VER_HELP, description=UL_VER_HELP, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=UPLOAD_TARGET_VERSION_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--accuracy-reached",
        metavar="<accuracy>",
        help=ACCURACY_REACHED_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--batch-size", metavar="<size>", help=BATCH_SIZE_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--gpu-model", metavar="<model>", help=GPU_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--memory-footprint", metavar="<footprint>", help=MEMORY_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--num-epochs", metavar="<num>", help=NUM_EPOCHS_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments("--desc", metavar="<desc>", help=DESC_HELP, type=str, default=None, action=SingleUseAction)
    @CLICommand.arguments(
        PERFORMANCE_ARG, metavar="<path>", help=PERFORMANCE_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        QUICK_START_ARG, metavar="<path>", help=QUICK_START_HELP, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(SETUP_ARG, metavar="<path>", help=SETUP_HELP, type=str, default=None, action=SingleUseAction)
    @CLICommand.arguments(NOTES_ARG, metavar="<path>", help=NOTES_HELP, type=str, default=None, action=SingleUseAction)
    @CLICommand.arguments("--source", metavar="<path>", help=SOURCE_HELP, type=str, default=".", action=SingleUseAction)
    @CLICommand.arguments(
        "--dry-run",
        help="List file paths, total upload size and file count without performing the upload.",
        action="store_true",
        default=False,
        dest="dry_run",
    )
    def upload_version(self, args):
        """Upload a resource version"""
        self.api.upload_version(
            target=args.target,
            source=args.source,
            gpu_model=args.gpu_model,
            memory_footprint=args.memory_footprint,
            num_epochs=args.num_epochs,
            batch_size=args.batch_size,
            accuracy_reached=args.accuracy_reached,
            description=args.desc,
            dry_run=args.dry_run,
            release_notes_filename=args.release_notes_filename,
            performance_filename=args.performance_filename,
            quick_start_guide_filename=args.quick_start_guide_filename,
            setup_filename=args.setup_filename,
        )

    chart_metavar = "org/[team/]resource_name[:version]"
    publish_help = (
        "Publish a resource from the NGC chart registry to catalog.  If no version is provided, the latest is assumed."
    )
    source_help = f"The source resource and version you want to publish.  Format: {chart_metavar}"
    product_help = PRODUCT_HELP + ", ".join(product_names)

    @CLICommand.command(help=publish_help, description=publish_help, feature_tag=PUBLISH_TYPE)
    @CLICommand.arguments("target", metavar=chart_metavar, help=publish_help, type=str)
    @CLICommand.arguments("--source", metavar=chart_metavar, help=source_help, type=str, default=None)
    @CLICommand.arguments("--metadata-only", help=METADATA_HELP, action="store_true")
    @CLICommand.arguments("--version-only", help=VERSION_ONLY_HELP, action="store_true")
    @CLICommand.arguments("--visibility-only", help=VISIBILITY_HELP, action="store_true")
    @CLICommand.arguments("--allow-guest", help=ALLOW_GUEST_HELP, action="store_true")
    @CLICommand.arguments("--discoverable", help=DISCOVERABLE_HELP, action="store_true")
    @CLICommand.arguments("--public", help=PUBLIC_HELP, action="store_true")
    @CLICommand.arguments(
        "--product-name",
        metavar="<product_name>",
        help=product_help,
        action="append",
        default=None,
    )
    @CLICommand.arguments(
        "--access-type", metavar="<access_type>", help=ACCESS_TYPE_HELP, type=str, default=None, choices=AccessTypeEnum
    )
    @CLICommand.mutex(["metadata_only"], ["version_only"], ["visibility_only"])
    @CLICommand.mutex(["access_type", "product_name"], ["allow_guest", "discoverable", "public"])
    def publish(self, args):
        """Publish a resource across registries or orgs/teams"""
        self.config.validate_configuration(guest_mode_allowed=False)
        if (args.product_name and not args.access_type) or (args.access_type and not args.product_name):
            raise InvalidArgumentError(
                "If specify one of '--product-name' or '--access-type',you must specify the other."
            ) from None
        if args.visibility_only:
            if args.source:
                raise InvalidArgumentError(
                    "You cannot specify a `--source` argument when making a `visibility_only` publishing request"
                )
            # Use the target value as the source. They aren't used, but are needed for the Publishing object.
            source = ModelRegistryTarget(args.target)
        else:
            if not args.source:
                raise InvalidArgumentError("You must specify a `--source` argument")
            source = ModelRegistryTarget(args.source)
            if not source.version:
                # Need a version to publish; try getting the latest version. If there is no version available for the
                # source, the `_get_latest_tag()` method will raise an exception.
                source.version = self._get_latest_version(source)
                self.printer.print_ok(f"No version specified; using latest version: {source.version}.")
        target = ModelRegistryTarget(args.target)
        if not target.version:
            target.version = source.version
        try:
            publisher = Publisher(source, target, self.publish_api, "resources", args)
        except InvalidArgumentError as e:
            self.printer.print_error(e)
            return
        publisher.publish()
        self.printer.print_ok(f"Successfully published {args.target}")

    deploy_help = (
        "Create interactive deployment of a resource from the NGC catalog to a cloud service provider (CSP). "
        "Default parameters can be overwritten with the provided flag options."
    )
    csp_help = "Cloud service provider (CSP) to deploy to."
    deploy_target_help = "Model and version to use for deployment."
    cpu_help = "Number of CPUs to use."
    gpu_help = "Number of GPUs to use."
    gpu_type_help = "Type of GPUs to use."
    disk_help = "Amount of disk space to allocate in GBs."
    ram_help = "Amount of RAM to allocate in GBs."
    image_help = "Image and tag to use as base for deployment if different from default."
