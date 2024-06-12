#
# Copyright (c) 2018-2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from builtins import int
import logging

from ngcbpc.api.configuration import Configuration
from ngcbpc.command.args_validation import (
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
from ngcbpc.data.model.SortOrderEnum import SortOrderEnum
from ngcbpc.data.registry.AccessTypeEnum import AccessTypeEnum
from ngcbpc.errors import InvalidArgumentError, NgcException, ResourceNotFoundException
from ngcbpc.printer.transfer import TransferPrinter
from ngcbpc.util.utils import find_case_insensitive, get_columns_help, get_environ_tag
from ngccli.modules.client import Client
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
from registry.printer.model import ModelPrinter

logger = logging.getLogger(__name__)

# TODO: As of 2020-02-25, these are hard-coded in the UI and CLI. If they become part of the schema,
# reference that and remove this class.
LINK_TYPE_VALUES = ["NGC", "Github", "Other"]
PUBLISH_TYPE = ENABLE_TYPE if (get_environ_tag() <= CANARY_ENV) else DISABLE_TYPE


def verify_link_type(args):
    """If a link_type has been specified, make sure it is valid, and if so, convert to the canonical capitalization"""
    if args.link_type:
        args.link_type = find_case_insensitive(args.link_type, LINK_TYPE_VALUES, "link_type")


class ModelSubCommand(RegistryCommand):
    CMD_NAME = "model"
    HELP = "Model Commands"
    DESC = "Model Commands"
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser

        self.model_printer = ModelPrinter()
        self.transfer_printer = TransferPrinter()
        self.config = Configuration()
        self.client = Client(api_key=self.config.app_key, base_url=self.config.base_url)
        self.model_api = self.client.registry.model
        self.search_api = self.client.registry.search
        self.label_set_api = self.client.registry.label_set
        self.publish_api = self.client.registry.publish
        self.resource_type = "MODEL"

    if bool(Configuration().product_names):
        product_names = Configuration().product_names
    else:
        product_names = PRODUCT_NAMES

    # Model specific
    model_target_arg_help = "Model.  Format: org/[team/]model_name."

    # Model version specific
    download_version_target_arg_help = (
        "Model version. Format: org/[team/]model_name[:version].  "
        "If no version specified, the latest version will be targeted."
    )

    upload_version_target_arg_help = "Model version. Format: org/[team/]model_name:version."

    # Model or Model version specific
    model_version_target_arg_help = (
        "Model or model version.  Format: org/[team/]model_name[:version]. "
        'To target a model version, use "org/[team/]model_name:version".  '
        'To target a model, use "org/[team/]model_name".'
    )

    default_version_sort = "SEMVER_DESC"
    model_version_sort_arg_help = "Sort model versions.  Allowed values: {}.  Default: {}.".format(
        ", ".join(SortOrderEnum), default_version_sort
    )

    # list specific
    list_target_arg_help = (
        "Filter the search by allowing wildcards for "
        "Model(s) or model version(s). Format: org/[team/]name[:version]. To target model version(s), "
        'use "org/[team/]name:version". To target model(s), use "org/[team/]name". Name and version also supports '
        'the wildcards "*" and "?". Examples: '
        '"my_org/my_model" - target my_model in my_org namespace. '
        '"my_org/my_team/my_model" - target my_model in my_org/my_team namespace. '
        '"my_org/my_team/*" - target all models in my_org/my_team namespace. '
        '"my_org/my_model*" - target models starting with my_model in my_org namespace. '
    )
    list_help = "List model(s) or model version(s)."

    columns_dict = {
        "name": "Name",
        "org": "Org",
        "team": "Team",
        "description": "Description",
        "updated": "Last Modified",
        "created": "Created Date",
        "shared": "Shared",
        "size": "File Size",
        "repository": "Repository",
        "version": "Latest Version",
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
    columns_default_model = ("repository", "Repository")
    columns_default_version = ("version", "Version")
    columns_help = get_columns_help(columns_dict, [columns_default_model, columns_default_version])
    ACCESS_TYPE_LIST_HELP = "Filter the list of resources to only resources that have specified access type."
    PRODUCT_NAME_LIST_HELP = (
        "Filter the list of resources to only resources that are under the product name. Multiple product-name"
        f" arguments are allowed. Choose from: {', '.join(product_names)}"
    )

    @CLICommand.arguments("target", metavar="<target>", help=list_target_arg_help, type=str, nargs="?", default=None)
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
        "--sort",
        metavar="<order>",
        help=model_version_sort_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
        choices=SortOrderEnum,
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
    @CLICommand.command(help=list_help, description=list_help)
    def list(self, args):
        """Lists models."""
        mrt = ModelRegistryTarget(args.target, glob_allowed=True)
        product_names_args = args.product_name if args.product_name else []
        product_names_args = [name.replace("-", "_") for name in product_names_args]

        model_list = self.model_api.list(
            args.target, mrt.org, mrt.team, args.sort, args.access_type, product_names_args
        )
        if mrt.version is None:
            self.model_printer.print_model_list(model_list, args.column)
        else:
            self.model_printer.print_model_version_list(model_list, columns=args.column)

    info_help = "Retrieve metadata for a model or model version."
    credentials_help = "List model credentials in addition to details for a version."
    metrics_help = f"{credentials_help} DEPRECATED; will be removed after May 2021. Please use '--credentials' instead."

    @CLICommand.command(help=info_help, description=info_help)
    @CLICommand.arguments("target", metavar="<target>", help=model_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--files", help="List files in addition to details for a version.", dest="list_files", action="store_true"
    )
    @CLICommand.arguments("--credentials", help=credentials_help, action="store_true")
    @CLICommand.arguments("--metrics", help=metrics_help, action="store_true")
    @CLICommand.mutex(["credentials"], ["metrics"])
    def info(self, args):
        """Retrieve metadata for a model or version."""
        mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)
        if args.metrics:
            self.model_printer.print_metrics_deprecation_warning("--metrics")
        if not mrt.version:
            arg_name = ""
            if args.credentials:
                arg_name = "credentials"
            elif args.metrics:
                arg_name = "metrics"
            if args.list_files:
                arg_name = "files"
            if arg_name:
                raise InvalidArgumentError(
                    f"--{arg_name} argument is not valid for a model target; please specify a version"
                )

        model = self.model_api.info(target=args.target)

        if mrt.version:
            # TODO: Collapse List Files into Info API function
            credentials = args.credentials or args.metrics
            file_list = self.get_version_files(args.target, mrt.org, mrt.team) if args.list_files else None
            self.model_printer.print_model_version(
                version=model.modelVersion, model=model.model, file_list=file_list, credentials=credentials
            )
        else:
            self.model_printer.print_model(model.model)

    def get_version_files(self, target, org_name, team_name):
        try:
            file_list = self.model_api.list_files(target=target, org=org_name, team=team_name)
        except ResourceNotFoundException:
            mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
            raise ResourceNotFoundException(
                f"Files could not be found for target '{mrt.name}:{mrt.version}'."
            ) from None
        return file_list

    # TODO group by model/version in help output
    # model specific
    application_arg_help = "Model application."
    framework_arg_help = "Framework used to train the model."
    format_arg_help = "Format of the model."
    precision_arg_help = "Precision the model was trained with."
    short_desc_arg_help = "Short description of the model."
    display_name_arg_help = "Display name for the model."
    label_set_help = (
        "Name of the label set. Format: org/[team/]name. "
        "Labels from the label set will be combined with the label argument. Can be used multiple times. "
    )
    labels_arg_help = (
        "Label for the model. To specify more than one label, use multiple --label arguments. "
        "Labels from the given label sets will be combined with the label argument."
    )
    logo_arg_help = "URL for the model logo image."
    public_dataset_name_help = "Name of public dataset used in the model."
    public_dataset_link_help = "Link to public dataset used in the model."
    public_dataset_license_help = "License for public dataset used in the model."
    built_by_help = "Builder of the model."
    publisher_help = "Publisher of the model."
    # Note: model level overview attribute is stored in description in the schema.
    # UI diverged and we need to quickly match them now.
    overview_arg_help = "Overview. Provide the path to a file that contains the overview for the model."
    bias_arg_help = "Bias. Provide the path to a file that contains the bias in the model."
    explainability_arg_help = (
        "Explainability.  Provide the path to a file that contains the explainability for this model."
    )
    privacy_arg_help = "Privacy. Provide the path to a file that contains the privacy for this model."
    safety_arg_help = (
        "Safety and Security. Provide the path to a file that contains the safety and security in the model."
    )

    # version specific
    gpu_model_arg_help = "The GPU used to train the model version."
    desc_arg_help = "Description for the model version."
    mem_footprint_arg_help = "The memory footprint of the model version."
    num_epochs_arg_help = "The number of epochs for the model version."
    batch_size_arg_help = "The batch size of the model version."
    accuracy_reached_arg_help = "Accuracy reached with model version."
    link_type_help = "Type of link to a resource or other toolsets for the model. Choices: {}.".format(
        ", ".join(LINK_TYPE_VALUES)
    )
    credentials_file_help = (
        "A JSON file containing a single object with 'name' and 'attributes' fields. Attributes are a list of "
        "key-value pairs. A maximum of twelve attributes may be used per file, and up to three files may be specified."
    )
    metrics_file_help = (
        f"{credentials_file_help} DEPRECATED; will be removed after May 2021. Please use --credentials-file instead."
    )

    create_help = "Create a model."

    @CLICommand.command(help=create_help, description=create_help, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=model_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--application",
        metavar="<app>",
        help=application_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--framework",
        metavar="<fwk>",
        help=framework_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--format",
        metavar="<fmt>",
        help=format_arg_help,
        dest="model_format",
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--precision",
        metavar="<prec>",
        help=precision_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--short-desc",
        metavar="<desc>",
        help=short_desc_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--overview-filename", metavar="<path>", help=overview_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--bias-filename",
        metavar="<path>",
        help=bias_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--explainability-filename",
        metavar="<path>",
        help=explainability_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--privacy-filename",
        metavar="<path>",
        help=privacy_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--safety-security-filename",
        metavar="<path>",
        help=safety_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=display_name_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments("--label", metavar="<label>", help=labels_arg_help, action="append", type=str, default=None)
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=label_set_help, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--logo", metavar="<url>", help=logo_arg_help, type=check_url, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--public-dataset-name",
        metavar="<name>",
        help=public_dataset_name_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-link",
        metavar="<link>",
        help=public_dataset_link_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-license",
        metavar="<lcs>",
        help=public_dataset_license_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=built_by_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher", metavar="<name>", help=publisher_help, type=str, default=None, action=SingleUseAction
    )
    def create(self, args):
        """Create a model."""
        created_model = self.model_api.create(
            target=args.target,
            application=args.application,
            framework=args.framework,
            model_format=args.model_format,
            precision=args.precision,
            short_description=args.short_desc,
            overview_filename=args.overview_filename,
            bias_filename=args.bias_filename,
            explainability_filename=args.explainability_filename,
            privacy_filename=args.privacy_filename,
            safety_security_filename=args.safety_security_filename,
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
        self.model_printer.print_head(f"Successfully created model '{args.target}'.")
        self.model_printer.print_model(created_model)

    update_help = "Update a model or model version."

    # These lists are used for argument validate.
    model_only_args = [
        ("application", "--application"),
        ("framework", "--framework"),
        ("model_format", "--format"),
        ("precision", "--precision"),
        ("short_desc", "--short-desc"),
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
        ("mem_footprint", "--memory-footprint"),
        ("num_epoch", "--num-epochs"),
        ("batch_size", "--batch-size"),
        ("accuracy_reached", "--accuracy-reached"),
        ("desc", "--description"),
        ("set_latest", "--set-latest"),
    ]

    # FIXME - we are suppressing metavar for optional args to match help output of globals
    @CLICommand.command(help=update_help, description=update_help, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=model_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--application", metavar="<app>", help=application_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--framework", metavar="<fwk>", help=framework_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--format",
        metavar="<fmt>",
        help=format_arg_help,
        dest="model_format",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--precision", metavar="<prec>", help=precision_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--short-desc", metavar="<desc>", help=short_desc_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--desc", metavar="<desc>", help=desc_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--overview-filename", metavar="<path>", help=overview_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--bias-filename",
        metavar="<path>",
        help=bias_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--explainability-filename",
        metavar="<path>",
        help=explainability_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--privacy-filename",
        metavar="<path>",
        help=privacy_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--safety-security-filename",
        metavar="<path>",
        help=safety_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=display_name_arg_help, type=str, default=None, action=SingleUseAction
    )
    # TODO - do we need to be able to update/delete a label without updating others?
    @CLICommand.arguments("--label", metavar="<label>", help=labels_arg_help, action="append", type=str, default=None)
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=label_set_help, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--logo", metavar="<url>", help=logo_arg_help, type=check_url, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--public-dataset-name",
        metavar="<name>",
        help=public_dataset_name_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-link",
        metavar="<url>",
        help=public_dataset_link_help,
        type=check_url,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-license",
        metavar="<lcs>",
        help=public_dataset_license_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=built_by_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher", metavar="<name>", help=publisher_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--gpu-model",
        metavar="<model>",
        dest="gpu_model",
        help=gpu_model_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--memory-footprint",
        dest="mem_footprint",
        metavar="<footprint>",
        help=mem_footprint_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--num-epochs",
        metavar="<num>",
        dest="num_epoch",
        help=num_epochs_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--batch-size",
        metavar="<size>",
        dest="batch_size",
        help=batch_size_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--accuracy-reached",
        metavar="<accuracy>",
        dest="accuracy_reached",
        help=accuracy_reached_arg_help,
        type=float,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--set-latest", help="Set this version to be the latest version.", default=None, action="store_true"
    )
    def update(self, args):
        """Update a model or version."""
        _mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)

        model = self.model_api.update(
            target=args.target,
            application=args.application,
            framework=args.framework,
            model_format=args.model_format,
            precision=args.precision,
            short_description=args.short_desc,
            overview_filename=args.overview_filename,
            bias_filename=args.bias_filename,
            explainability_filename=args.explainability_filename,
            privacy_filename=args.privacy_filename,
            safety_security_filename=args.safety_security_filename,
            display_name=args.display_name,
            label=args.label,
            label_set=args.label_set,
            logo=args.logo,
            public_dataset_name=args.public_dataset_name,
            public_dataset_license=args.public_dataset_license,
            public_dataset_link=args.public_dataset_link,
            built_by=args.built_by,
            publisher=args.publisher,
            num_epochs=args.num_epoch,
            batch_size=args.batch_size,
            accuracy_reached=args.accuracy_reached,
            set_latest=args.set_latest,
            gpu_model=args.gpu_model,
            memory_footprint=args.mem_footprint,
        )

        if _mrt.version is None:
            self.model_printer.print_head("Successfully updated model '{}'.".format(args.target))
            self.model_printer.print_model(model)
        else:
            self.model_printer.print_head(f"Successfully updated model version '{args.target}'.")
            self.model_printer.print_model_version(model.modelVersion)

    delete_help = "Remove a model or model version."

    # TODO - don't allow model removal if versions still exist.
    @CLICommand.command(help=delete_help, description=delete_help, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=model_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "-y",
        "--yes",
        help="Automatically say yes to all interactive questions.",
        dest="default_yes",
        action="store_true",
    )
    def remove(self, args):
        """Delete a model."""
        self.config.validate_configuration()
        mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)
        self.model_api.remove(target=args.target, default_yes=args.default_yes)
        if mrt.version:
            self.model_printer.print_ok(f"Successfully removed model version '{args.target}'.")
        else:
            self.model_printer.print_ok(f"Successfully removed model '{args.target}'.")

    download_version_help = "Download a model version."

    @CLICommand.command(name="download-version", help=download_version_help, description=download_version_help)
    @CLICommand.arguments("target", metavar="<target>", help=download_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--dest",
        metavar="<path>",
        help="Destination to download the current model.  Default: .",
        type=str,
        default="",
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--file",
        metavar="<wildcard>",
        action="append",
        help=(
            "Specify individual files to download from the model.\n"
            "Supports standard Unix shell-style wildcards like (?, [abc], [!a-z], etc..) "
            "May be used multiple times in the same command."
        ),
    )
    @CLICommand.arguments(
        "--exclude",
        metavar="<wildcard>",
        action="append",
        help=(
            "Exclude files or directories from the downloaded model.\n"
            "Supports standard Unix shell-style wildcards like (?, [abc], [!a-z], etc..). "
            "May be used multiple times in the same command."
        ),
    )
    def download_version(self, args):
        """Download the specified model version"""
        self.model_api.download_version(
            target=args.target, destination=args.dest, file_patterns=args.file, exclude_patterns=args.exclude
        )

    def _get_latest_version(self, target):
        try:
            model_resp = self.model_api.get(target.org, target.team, target.name)
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
        if not model_resp.model.latestVersionIdStr:
            raise NgcException("Target '{}' has no version available for download.".format(target))

        return model_resp.model.latestVersionIdStr

    upload_version_help = "Upload a model version."

    @CLICommand.command(
        name="upload-version", help=upload_version_help, description=upload_version_help, feature_tag=CONFIG_TYPE
    )
    @CLICommand.arguments("target", metavar="<target>", help=upload_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--source",
        metavar="<path>",
        help="Provide source directory of the model or path of single file to be uploaded.  Default: .",
        type=str,
        default=".",
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--gpu-model",
        metavar="<model>",
        dest="gpu_model",
        help=gpu_model_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--memory-footprint",
        dest="mem_footprint",
        metavar="<footprint>",
        help=mem_footprint_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--num-epochs",
        metavar="<num>",
        dest="num_epoch",
        help=num_epochs_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--batch-size",
        metavar="<size>",
        dest="batch_size",
        help=batch_size_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--accuracy-reached",
        metavar="<accuracy>",
        dest="accuracy_reached",
        help=accuracy_reached_arg_help,
        type=float,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments("--desc", metavar="<desc>", help=desc_arg_help, type=str, default="", action=SingleUseAction)
    @CLICommand.arguments(
        "--dry-run",
        help="List file paths, total upload size and file count without performing the upload.",
        action="store_true",
        default=False,
        dest="dry_run",
    )
    @CLICommand.arguments(
        "--link-type", metavar="<type>", default=None, help=link_type_help, type=str, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--link",
        metavar="<url>",
        help="Link to resource or other toolsets for the model",
        action=SingleUseAction,
        type=check_url,
    )
    @CLICommand.arguments(
        "--credentials-file", metavar="<file>", help=credentials_file_help, action="append", default=None
    )
    @CLICommand.arguments("--metrics-file", metavar="<file>", help=metrics_file_help, action="append", default=None)
    @CLICommand.mutex(["credentials_file"], ["metrics_file"])
    def upload_version(self, args):
        """Upload a model version."""
        if args.metrics_file:
            self.model_printer.print_metrics_deprecation_warning("--metrics_file")

        self.model_api.upload_version(
            target=args.target,
            source=args.source,
            gpu_model=args.gpu_model,
            memory_footprint=args.mem_footprint,
            num_epochs=args.num_epoch,
            batch_size=args.batch_size,
            accuracy_reached=args.accuracy_reached,
            description=args.desc,
            link=args.link,
            link_type=args.link_type,
            dry_run=args.dry_run,
            credential_files=args.credentials_file,
            metric_files=args.metrics_file,
        )

    model_metavar = "org/[team/]model_name[:version]"
    publish_help = (
        "Publish a model from the NGC model registry to catalog.  If no version is provided, 'latest' is assumed."
    )
    publish_arg_help = f"The the target model and version you want to publish to.  Format: {model_metavar}"
    source_help = f"The source model and version you want to publish.  Format: {model_metavar}"
    product_help = PRODUCT_HELP + ", ".join(product_names)

    @CLICommand.command(help=publish_help, description=publish_help, feature_tag=PUBLISH_TYPE)
    @CLICommand.arguments("target", metavar=model_metavar, help=publish_help, type=str)
    @CLICommand.arguments("--source", metavar=model_metavar, help=source_help, type=str, default=None)
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
        self.config.validate_configuration(guest_mode_allowed=False)
        if (args.product_name and not args.access_type) or (args.access_type and not args.product_name):
            raise InvalidArgumentError(
                "If specify one of '--product-name' or '--access-type', you must specify the other."
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
                self.model_printer.print_ok(f"No version specified; using latest version: {source.version}.")
        target = ModelRegistryTarget(args.target)
        if not target.version:
            target.version = source.version
        try:
            publisher = Publisher(source, target, self.publish_api, "models", args)
        except InvalidArgumentError as e:
            self.model_printer.print_error(e)
            return
        publisher = Publisher(source, target, self.publish_api, "models", args)
        publisher.publish()
        self.model_printer.print_ok(f"Successfully published {args.target}")
