# Copyright (c) 2019-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from forge.command.forge import ForgeCommand
from forge.printer.user import UserPrinter
from ngcbpc.api.configuration import Configuration
from ngcbpc.command.clicommand import CLICommand
from ngccli.modules.client import Client


class UserCommand(ForgeCommand):

    CMD_NAME = "user"
    HELP = "User Commands"
    DESC = "User Commands"

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = Configuration()
        client = Client(api_key=self.config.app_key, base_url=self.config.base_url)
        self.api = client.forge.user
        self.printer = UserPrinter()

    INFO_HELP = "Current user information."

    @CLICommand.command(help=INFO_HELP, description=INFO_HELP)
    def info(self, args):
        """User info."""
        self.config.validate_configuration()
        org_name = args.org or self.config.org_name
        team_name = args.team or self.config.team_name
        resp = self.api.info(org_name, team_name)
        self.printer.print_info(resp)
