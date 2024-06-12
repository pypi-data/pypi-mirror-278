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

from nvcf.api.nvcf import CloudFunctionAPI
from nvcf.printer.deploy_printer import DeploymentPrinter

from ngcbpc.command.clicommand import CLICommand
from ngcbpc.constants import ENABLE_TYPE


class CloudFunctionCommand(CLICommand):
    CMD_NAME = "cloud-function"
    HELP = "Cloud Function Commands"
    DESC = "Cloud Function Commands"
    CMD_ALIAS = ["cf", "picasso"]
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.make_bottom_commands(parser)
        self.client = CloudFunctionAPI()
        self.printer = DeploymentPrinter()

    @CLICommand.command(
        name="available-gpus",
        help="List available GPUs in your Org, Admin Only",
        description="List available GPUs in your Org, Admin Only",
    )
    def available_gpus(self, _):
        resp = self.client.deployments.list_cluster_groups()
        self.printer.print_gpus(resp.get("clusterGroups", {}))
