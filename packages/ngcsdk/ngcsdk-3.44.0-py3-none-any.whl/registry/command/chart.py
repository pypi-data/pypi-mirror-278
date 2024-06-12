#
# Copyright (c) 2020-2021, NVIDIA CORPORATION. All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto. Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import argparse
import logging
import time

from ngcbpc.api.configuration import Configuration
from ngcbpc.command.args_validation import (
    check_add_args_columns,
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
from ngcbpc.data.registry.AccessTypeEnum import AccessTypeEnum
from ngcbpc.errors import InvalidArgumentError, NgcException, ResourceNotFoundException
from ngcbpc.util.utils import confirm_remove, get_columns_help, get_environ_tag
from ngccli.modules.client import Client
from registry.api.utils import ChartRegistryTarget
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
from registry.errors import ChartNotFoundException
from registry.printer.chart import ChartPrinter

logger = logging.getLogger(__name__)

PUBLISH_TYPE = ENABLE_TYPE if (get_environ_tag() <= CANARY_ENV) else DISABLE_TYPE


class ChartSubCommand(RegistryCommand):
    CMD_NAME = "chart"
    HELP = "Helm Chart Commands"
    DESC = "Helm Chart Commands"
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = Configuration()
        api_key = self.config.app_key
        base_url = self.config.base_url
        client = Client(api_key=api_key, base_url=base_url)
        self.api = client.registry.chart
        self.resource_type = "HELM_CHART"
        self.publish_api = client.registry.publish
        self.printer = ChartPrinter()

    if bool(Configuration().product_names):
        product_names = Configuration().product_names
    else:
        product_names = PRODUCT_NAMES

    TARGET_HELP = "Chart or chart version. Format: org/[team/]chart_name[:version]."
    TARGET_VERSION_HELP = "Chart with version. Format: org/[team/]chart_name:version."

    LIST_HELP = "List charts."
    CREATE_TARGET_HELP = "Name of the chart to create. Format: org/[team/]chart_name."
    UPLOAD_TARGET_VERSION_HELP = (
        "Chart version. Format: org/[team/]chart_name:version. "
        "Alternative format using file name: org/[team/]chart_name-1.2.3.tgz"
    )
    # common chart and chart version attributes
    OVERVIEW_HELP = "Overview. Provide the path to a file that contains the overview for the chart."
    REMOVE_HELP = "Remove a chart from the repository."
    CREATE_VER_HELP = "Create a chart's metadata."
    LABEL_SET_HELP = (
        "Name of the label set. Format: org/[team/]name. "
        "Labels from the label set will be combined with the label argument. Can be used multiple times. "
    )
    LABEL_HELP = (
        "Label for the chart. To specify more than one label, use multiple --label arguments. "
        "Labels from the given label sets will be combined with the label argument."
    )
    LIST_TARGET_HELP = (
        "Filter the search by allowing wildcards for charts. "
        "Format: org/[team/]chart_name[:version]. "
        "To target charts use 'org/[team/]chart_name'. "
        "Both name and version support the wildcards '*' and '?'.  "
        "Version also supports character expressions ([a-z], [!ab], etc.). "
        "Examples:  'my_org/my_chart' - target my_chart in my_org repository. "
        "'my_org/my_team/my_chart' - target my_chart in my_org/my_team repository. "
        "'my_org/my_team/*' - target all charts in my_org/my_team repository. "
        "'my_org/my_chart*' "
        "- target all chart versions for my_chart in my_org namespace. "
        "'my_org/my_chart:[1-5]' "
        "- target versions 1-5 for my_chart in my_org namespace."
    )
    columns_dict = {
        "created": "Created",
        "createdBy": "Created By",
        "description": "Description",
        "displayName": "Display Name",
        "guestAccess": "Guest Access",
        "labels": "Labels",
        "name": "Name",
        "org": "Org",
        "public": "Public",
        "size": "Size",
        "team": "Team",
        "updated": "Last Modified",
        "version": "Version",
    }
    columns_default_chart = ("repository", "Repository")
    columns_default_version = ("artifactVersion", "Version")
    columns_help = get_columns_help(columns_dict, [columns_default_chart, columns_default_version])
    ACCESS_TYPE_LIST_HELP = "Filter the list of resources to only resources that have specified access type."
    PRODUCT_NAME_LIST_HELP = (
        "Filter the list of resources to only resources that are under the product name. Multiple product-name"
        f" arguments are allowed. Choose from: {', '.join(product_names)}"
    )

    # These are used for validating update arguments.
    chart_update_args = (
        "short_desc",
        "overview_filename",
        "built_by",
        "display_name",
        "label",
        "logo",
        "publisher",
        "label_set",
    )

    @CLICommand.arguments(
        "target",
        metavar="<target>",
        help=LIST_TARGET_HELP,
        type=str,
        nargs="?",
        default=None,
    )
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
    @CLICommand.command(name="list", help=LIST_HELP, description=LIST_HELP)
    def list(self, args) -> None:
        """List charts/versions. Depending if version is provided."""

        crt = ChartRegistryTarget(args.target, glob_allowed=True)
        arg_cols = args.column if hasattr(args, "column") else None
        columns = self._col_translate(arg_cols) if arg_cols else None
        product_names_args = args.product_name if args.product_name else []
        product_names_args = [name.replace("-", "_") for name in product_names_args]

        if crt.version is None:
            check_add_args_columns(columns, ChartSubCommand.columns_default_chart)
            chart_list = self.api.list_charts(
                args.target, access_type=args.access_type, product_names=product_names_args
            )
            self.printer.print_chart_list(chart_list, columns=columns)

        else:
            # drew from legacy logic d31d2242e3256579dcdd706bc4cd1c41ec3a2f2d
            # has version_list | has main_chart | print output
            #     F            |        T/F     | empty
            #     T            |        F       | version_list
            #     T            |        T       | version_list + main_chart

            check_add_args_columns(columns, ChartSubCommand.columns_default_version)
            try:
                # unpack to esculate exceptions
                version_list = list(self.api.list_versions(args.target))
            except (ResourceNotFoundException, ChartNotFoundException):
                logger.debug("version list is empty")
                self.printer.print_chart_version_list([], columns=columns, main_chart=None)
                return None
            # should not merge these two because we still print version if main_chart is None
            try:
                main_chart_resp = self.api.list_charts(args.target)
                main_chart = list(main_chart_resp)[0][0]  # possible IndexError
            except IndexError:
                main_chart = None
                logger.debug("main chart index error, resp: %s", main_chart_resp)
            self.printer.print_chart_version_list(version_list, columns=columns, main_chart=main_chart)
        return None

    @staticmethod
    def _col_translate(columns):
        translate_table = {
            "org": "orgName",
            "team": "teamName",
            "created": "dateCreated",
            "updated": "dateModified",
            "public": "isPublic",
        }
        return [(translate_table.get(col, col), disp) for col, disp in columns]

    INFO_HELP = "Retrieve metadata for a chart or chart version."

    @CLICommand.command(name="info", help=INFO_HELP, description=INFO_HELP)
    @CLICommand.arguments("target", metavar="<target>", help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--files",
        help="List files in addition to details for a version.",
        dest="list_files",
        action="store_true",
        default=False,
    )
    def info(self, args) -> None:
        """Retrieve metadata for a chart"""
        self.config.validate_configuration(guest_mode_allowed=True)
        crt = ChartRegistryTarget(args.target, org_required=True, name_required=True)

        # args.list_files:          True    |   False
        # name+ver:         chart+ver+files |   chart+ver
        # name:           ArgumentTypeError |   chart

        if crt.version is None and args.list_files:
            raise argparse.ArgumentTypeError(
                "--files argument is not valid for a chart target, please specify a version."
            )

        chart = self.api.info_chart(args.target)
        if crt.version is None:
            self.printer.print_chart(chart)
        else:
            version = self.api.info_chart_version(args.target)
            files = self.api.list_files(args.target) if args.list_files else None
            self.printer.print_chart_version(version=version, chart=chart, file_list=files)

    UPDATE_HELP = "Update a chart or chart version."

    @CLICommand.command(
        name="update",
        help=UPDATE_HELP,
        description=UPDATE_HELP,
        feature_tag=CONFIG_TYPE,
    )
    @CLICommand.arguments("target", metavar="<target>", help=CREATE_TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--overview-filename",
        metavar="<path>",
        help=OVERVIEW_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--display-name",
        metavar="<dispName>",
        help="The name to display for the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--label",
        metavar="<label>",
        help=LABEL_HELP,
        type=str,
        default=None,
        action="append",
    )
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=LABEL_SET_HELP, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--short-desc",
        metavar="<shortDesc>",
        help="A brief description of the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by",
        metavar="<builtBy>",
        help="The entity responsible for building the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--publisher",
        metavar="<publisher>",
        help="The entity responsible for creating the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--logo",
        metavar="<logo>",
        help="The URL of the image to set as the logo for the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    def update(self, args):
        """Update a resource"""

        updated_chart = self.api.update(
            target=args.target,
            overview_filepath=args.overview_filename,
            display_name=args.display_name,
            labels=args.label,
            label_sets=args.label_set,
            logo=args.logo,
            publisher=args.publisher,
            built_by=args.built_by,
            short_description=args.short_desc,
        )
        self.printer.print_head(f"Successfully updated chart '{args.target}'")
        self.printer.print_chart(updated_chart)

    @CLICommand.command(
        name="remove",
        help=REMOVE_HELP,
        description=REMOVE_HELP,
        feature_tag=CONFIG_TYPE,
    )
    @CLICommand.arguments("target", metavar="<target>", help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "-y",
        "--yes",
        help="Automatically say yes to all interactive questions.",
        dest="default_yes",
        action="store_true",
    )
    def remove(self, args):
        """Delete a chart from the repository"""

        self.config.validate_configuration()
        crt = ChartRegistryTarget(args.target, org_required=True, name_required=True)

        confirm_remove(target=args.target, default=args.default_yes)

        if crt.version is None:
            for version in self.api.list_versions(args.target):
                # we have to print on command layer and print for each version deleted
                # so exposing the version deletion logic here,
                # sdk user can call api.remove() directly
                # and in api layer, it follows the same removal logic
                versioned_target = args.target + ":" + version.id
                self.api.remove_chart_version(versioned_target)
                self.printer.print_ok("Successfully removed chart version '{}'.".format(versioned_target))

            self.api.remove_chart(args.target)
            self.printer.print_ok("Successfully removed chart '{}'.".format(args.target))
        else:
            self.api.remove_chart_version(args.target)
            self.printer.print_ok("Successfully removed chart version '{}'.".format(args.target))

    PULL_HELP = "Download a chart version."
    DL_TARGET_HELP = (
        "Chart version. Format: org/[team/]chart[:version]. "
        "If no version specified, the latest version will be targeted."
    )

    @CLICommand.command(name="pull", help=PULL_HELP, description=PULL_HELP)
    @CLICommand.arguments("target", metavar="<target>", help=DL_TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--dest",
        metavar="<path>",
        help="Provide a destination to download the chart. Default: . (current directory)",
        type=str,
        default="",
        action=SingleUseAction,
    )
    def pull(self, args):
        """Download the specified chart"""
        crt = ChartRegistryTarget(args.target, org_required=True, name_required=True, version_required=False)
        if not crt.version:
            crt.version = self.api.get_latest_chart_version(args.target)
            args.target += f":{crt.version}"
            self.printer.print_ok(f"No version specified; downloading latest version: {crt.version}.")

        output_path = self.api.pull(args.target, args.dest)
        self.printer.print_ok(f"Successfully pulled chart version '{output_path}'.")

    def _get_latest_version(self, obj) -> str:
        target = "/".join(i for i in [obj.org, obj.team, obj.name] if i)
        try:
            chart = self.api.info_chart(target)
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
        if not chart.latestVersionId:
            raise NgcException("Target '{}' has no version available.".format(target))
        return chart.latestVersionId

    @CLICommand.command(
        name="create",
        help=CREATE_VER_HELP,
        description=CREATE_VER_HELP,
        feature_tag=CONFIG_TYPE,
    )
    @CLICommand.arguments(
        "target",
        metavar="<target>",
        help=CREATE_TARGET_HELP,
        type=str,
        default=None,
    )
    @CLICommand.arguments(
        "--overview-filename",
        metavar="<path>",
        help=OVERVIEW_HELP,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--display-name",
        metavar="<dispName>",
        help="The name to display for the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments("--label", metavar="<label>", help=LABEL_HELP, type=str, default=None, action="append")
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=LABEL_SET_HELP, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--short-desc",
        metavar="<shortDesc>",
        help="A brief description of the chart",
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by",
        metavar="<builtBy>",
        help="The entity responsible for building the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--publisher",
        metavar="<publisher>",
        help="The entity responsible for creating the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--logo",
        metavar="<logo>",
        help="The URL of the image to set as the logo for the chart",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    def create(self, args):
        """Create a chart's metadata"""

        created_chart = self.api.create(
            target=args.target,
            short_description=args.short_desc,
            overview_filepath=args.overview_filename,
            display_name=args.display_name,
            labels=args.label,
            label_sets=args.label_set,
            logo=args.logo,
            publisher=args.publisher,
            built_by=args.built_by,
        )
        self.printer.print_head("Successfully created chart '{}'.".format(args.target))
        self.printer.print_chart(created_chart)

    UL_VER_HELP = "Push (upload) a chart."
    SOURCE_HELP = (
        "The path to the directory containing the packaged chart. "
        "If not specified, the chart will be uploaded from the current directory."
    )

    @CLICommand.command(
        name="push",
        help=UL_VER_HELP,
        description=UL_VER_HELP,
        feature_tag=CONFIG_TYPE,
    )
    @CLICommand.arguments(
        "target",
        metavar="<target>",
        help=UPLOAD_TARGET_VERSION_HELP,
        type=str,
        default=None,
    )
    @CLICommand.arguments(
        "--source",
        metavar="<path>",
        help=SOURCE_HELP,
        type=str,
        default=".",
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--dry-run",
        help="List file paths, total upload size and file count without performing the upload.",
        action="store_true",
        default=False,
        dest="dry_run",
    )
    def push(self, args):
        """Upload a chart"""
        msgs = []
        self.api.push(args.target, args.source, is_dry_run=args.dry_run, cli_messages=msgs)
        for msg in msgs:
            self.printer.print_ok(msg)

        if not args.dry_run:
            retry = 1
            while retry <= 3:
                # push returns http code 201 without the artifact version, we need to poll with some delays/retries
                # to get the updated version
                try:
                    chart_version = self.api.info_chart_version(args.target)
                    self.printer.print_chart_version(chart_version)
                    return
                except ChartNotFoundException:
                    if retry == 3:
                        raise
                    time.sleep(1)
                    retry += 1

    chart_metavar = "org/[team/]chart[:version]"
    publish_help = (
        "Publish a chart from the NGC chart registry to catalog.  If no version is provided, the latest is assumed."
    )
    publish_arg_help = f"The the target image and tag you want to publish to.  Format: {chart_metavar}"
    source_help = f"The source image and tag you want to publish.  Format: {chart_metavar}"
    metadata_help = "Only perform a shallow copy of the metadata instead of a deep copy of the objects referenced."
    allow_guest_help = "Open up permissions of the published object to be accessible by unauthenticated users."
    discoverable_help = "Open up permission of the publish object to be discoverable by searches."
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
        self.config.validate_configuration(guest_mode_allowed=False)
        if (args.product_name and not args.access_type) or (args.access_type and not args.product_name):
            raise InvalidArgumentError(
                "If specify one of '--product-name' or '--access-type', you must specify the other."
            ) from None
        source = ChartRegistryTarget(args.source)
        if args.visibility_only:
            if args.source:
                raise InvalidArgumentError(
                    "You cannot specify a `--source` argument when making a `visibility_only` publishing request"
                )
            # Use the target value as the source. They aren't used, but are needed for the Publishing object.
            source = ChartRegistryTarget(args.target)
        else:
            if not args.source:
                raise InvalidArgumentError("You must specify a `--source` argument")
            source = ChartRegistryTarget(args.source)
            if not source.version:
                # Need a version to publish; try getting the latest version. If there is no version available for the
                # source, the `_get_latest_tag()` method will raise an exception.
                source.version = self._get_latest_version(source)
                self.printer.print_ok(f"No version specified; using latest version: {source.version}.")
        target = ChartRegistryTarget(args.target)
        if not target.version:
            target.version = source.version
        try:
            publisher = Publisher(source, target, self.publish_api, "helm-charts", args)
        except InvalidArgumentError as e:
            self.printer.print_error(e)
            return
        publisher.publish()
        self.printer.print_ok(f"Successfully published {args.target}")
