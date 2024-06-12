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

from nvcf.api.deployment_spec import DeploymentSpecification
from nvcf.command.function import FunctionCommand
from nvcf.command.utils import FunctionTarget
from nvcf.printer.deploy_printer import DeploymentPrinter

from ngcbpc.command.args_validation import check_ymd_hms_datetime
from ngcbpc.command.clicommand import CLICommand
from ngcbpc.command.config import Configuration
from ngcbpc.constants import ENABLE_TYPE
from ngccli.modules.client import Client


class DeployCommand(FunctionCommand):

    CMD_NAME = "deploy"
    DESC = "Description of the deployment command"
    HELP = "Get information about deployed functions"
    CMD_ALIAS = []

    FUNCTION_ID_HELP = "Function ID"
    FUNCTION_VERSION_OPTIONAL_METAVAR = "function-id:[<function-id>]"
    TARGET_HELP = "Function. Format: function-id:function-version"
    FUNCTION_METAVAR = "<function-id>:<function-version-id>"
    DEPLOYMENT_SPECIFICATION_HELP = "Deployment specs with GPU and Backend details, can specify multiple times."
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.client = Client()
        self.config = Configuration()
        self.printer = DeploymentPrinter()

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(help="Info about a function deployment", description="Info about a function deployment")
    def info(self, args):
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        resp = self.client.cloud_function.deployments.info(ft.id, ft.version)
        self.printer.print_info(resp.get("deployment", {}))

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(help="Undeploy A function", description="Undeploy a function")
    def remove(self, args):
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        self.client.cloud_function.deployments.delete(ft.id, ft.version)
        print("Delete successful")

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--deployment-specification",
        metavar="<backend:gpu:instance_type:min_instances:max_instances>",
        action="append",
        help="Deployment specs with GPU and Backend details, can specify multiple times",
        default=None,
        required=True,
    )
    @CLICommand.command(help="Update an existing deployment.", description="Update an existing deployment")
    def update(self, args):
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        dep_specs = [DeploymentSpecification.from_str(dep_spec) for dep_spec in args.deployment_specification]

        resp = self.client.cloud_function.deployments.update(ft.id, ft.version, dep_specs)
        self.printer.print_info(resp.get("deployment", {}))

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--deployment-specification",
        metavar="<backend:gpu:instance_type:min_instances:max_instances>",
        action="append",
        help=DEPLOYMENT_SPECIFICATION_HELP,
        default=None,
        required=True,
    )
    @CLICommand.command(help="Create a deployment.", description="Create a deployment")
    def create(self, args):
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        dep_specs = [DeploymentSpecification.from_str(dep_spec) for dep_spec in args.deployment_specification]

        resp = self.client.cloud_function.deployments.create(ft.id, ft.version, dep_specs)
        self.printer.print_info(resp.get("deployment", {}))

    @CLICommand.arguments("target", metavar=FUNCTION_VERSION_OPTIONAL_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--start-time",
        metavar="<t>",
        help="Specifies the start time for querying logs. Format: [yyyy-MM-dd::HH:mm:ss].",
        type=str,
        action=check_ymd_hms_datetime(),
    )
    @CLICommand.arguments(
        "--end-time",
        metavar="<t>",
        help="Specifies the end time for querying logs. Format: [yyyy-MM-dd::HH:mm:ss]. Default: now",
        type=str,
        action=check_ymd_hms_datetime(),
    )
    @CLICommand.arguments(
        "--duration",
        metavar="<t>",
        help=(
            "Specifies the duration of time, either after begin-time or before end-timelogs. Format: [nD][nH][nM][nS]."
            " Default 1 day, doesn't respect decimal measurements"
        ),
        type=str,
    )
    @CLICommand.command(help="Query Logs for NVCF Deployment", description="Query Logs for Deployment")
    def log(self, args):
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=False)
        logs = self.client.cloud_function.deployments.query_logs(
            function_id=ft.id,
            duration=args.duration,
            start_time=args.start_time,
            end_time=args.end_time,
            function_version_id=ft.version,
        )
        self.printer.print_logs(logs)
