# Copyright (c) 2019-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from forge.command.forge import ForgeCommand
from forge.printer.provider import ProviderPrinter
from ngcbpc.api.configuration import Configuration
from ngcbpc.command.clicommand import CLICommand
from ngccli.modules.client import Client


class ProviderCommand(ForgeCommand):

    CMD_NAME = "provider"
    HELP = "Infrastructure Provider Commands"
    DESC = "Infrastructure Provider Commands"

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = Configuration()
        client = Client(api_key=self.config.app_key, base_url=self.config.base_url)
        self.api = client.forge.provider
        self.printer = ProviderPrinter()

    INFO_HELP = "Current infrastructure provider."

    @CLICommand.arguments(
        "--statistics", help="Show statistics for current infrastructure provider.", action="store_true", default=False
    )
    @CLICommand.command(help=INFO_HELP, description=INFO_HELP)
    def info(self, args):
        """Infrastructure provider info."""
        resp, stats = self.api.info(args.org, args.team, args.statistics)
        self.printer.print_info(resp, stats)
