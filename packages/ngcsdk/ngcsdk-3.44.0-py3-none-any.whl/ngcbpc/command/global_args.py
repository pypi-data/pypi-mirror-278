#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from ngcbpc.api.configuration import Configuration
from ngcbpc.command.args_validation import check_team_name_pattern
from ngcbpc.command.completers import (
    ace_completer,
    config_profile_completer,
    format_completer,
    org_completer,
    team_completer,
)
from ngcbpc.command.parser import _CallFunction, NgcParser
from ngcbpc.constants import CANARY_ENV, CONFIG_TYPE, DISABLE_TYPE, FORMAT_TYPES
from ngcbpc.environ import NGC_CLI_ENABLE_MULTIPLE_CONFIGS
from ngcbpc.errors import InvalidArgumentError
from ngcbpc.util.utils import get_environ_tag

# Arguments added to this parser will be added to all of the parsers
config = Configuration()
parent_parser = NgcParser()
parent_parser.register("action", "call_function", _CallFunction)

MULTIPLE_CONFIGURATIONS = get_environ_tag() <= CANARY_ENV and NGC_CLI_ENABLE_MULTIPLE_CONFIGS

# When setting help strings, please follow these rules:
#
# Optional arguments: Use complete sentences, in imperative (command) form, with a period at the end and the first
#                     letter capitalized. Ex:  "Perform a function."
#
# Positional arguments: Capitalize each word, and try to limit the CLI output to a single line.
#                       Ex:  "Thing ID" or "Thing ID.  Examples: 'valid-input-example"
#
# ACE and ID should be capitalized.

parent_parser.add_argument("-h", "--help", action="help", help="Show this help message and exit.")

parent_parser.add_argument(
    "--debug",
    action="call_function",
    fn=config.set_debug_mode_global,
    exc=None,
    help="Enable debug mode.",
    const=True,
    nargs=0,
)

parent_parser.add_argument(
    "--format_type",
    action="call_function",
    fn=config.set_format_type_global,
    exc=InvalidArgumentError("format_type"),
    help=(
        "Specify the output format type. Supported formats are: %(choices)s.  "
        "Only commands that produce tabular data support csv format.  "
        "Default: ascii"
    ),
    metavar="<fmt>",
    choices=FORMAT_TYPES,
).completer = format_completer

parent_parser.add_argument(
    "--org",
    action="call_function",
    fn=config.set_org_global,
    exc=InvalidArgumentError("org"),
    help=(
        "Specify the organization name.  "
        'Use "--org no-org" to override other sources and specify no org '
        "(no-org cannot be used if API key is set). "
        "Default: current configuration"
    ),
    metavar="<name>",
    feature_type=CONFIG_TYPE,
).completer = org_completer

parent_parser.add_argument(
    "--ace",
    action="call_function",
    fn=config.set_ace_global,
    exc=InvalidArgumentError("ace"),
    help=(
        "Specify the ACE name.  "
        'Use "--ace no-ace" to override other sources and specify no ACE.  '
        "Default: current configuration"
    ),
    metavar="<name>",
    feature_type=CONFIG_TYPE,
).completer = ace_completer

parent_parser.add_argument(
    "--team",
    action="call_function",
    fn=config.set_team_global,
    exc=InvalidArgumentError("team"),
    help=(
        "Specify the team name.  "
        'Use "--team no-team" to override other sources and specify no team.  '
        "Default: current configuration"
    ),
    metavar="<name>",
    feature_type=CONFIG_TYPE,
    type=check_team_name_pattern,
).completer = team_completer

parent_parser.add_argument(
    "--config-profile",
    action="call_function",
    fn=config.set_config_global,
    exc=InvalidArgumentError("config"),
    help="Specify the configuration profile.  Default: current configuration",
    metavar="<name>",
    feature_type=CONFIG_TYPE if MULTIPLE_CONFIGURATIONS else DISABLE_TYPE,
).completer = config_profile_completer

# Parent list
PARENT_PARSERS = [parent_parser]
