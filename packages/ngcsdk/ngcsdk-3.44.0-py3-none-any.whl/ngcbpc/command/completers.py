#
# Copyright (c) 2018-2020, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from ngcbpc.api.configuration import Configuration
from ngcbpc.constants import FORMAT_TYPES


class NGCCompleter:
    """To be used with argcomplete"""

    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        result = self.fn(*self.args, **self.kwargs)
        return result


config = Configuration()
org_completer = NGCCompleter(config.get_org_names)
ace_completer = NGCCompleter(lambda: [elem.name for elem in config.get_ace_list(config.org_name)])
team_completer = NGCCompleter(config.get_team_list)
format_completer = NGCCompleter(lambda: FORMAT_TYPES)
_valid_configuration_options = (
    [config.get("key_name", "") for config in config.configurations.values()] if config.configurations else []
)
config_profile_completer = NGCCompleter(lambda: _valid_configuration_options)

__all__ = [
    "org_completer",
    "ace_completer",
    "team_completer",
    "format_completer",
    "config_profile_completer",
]
