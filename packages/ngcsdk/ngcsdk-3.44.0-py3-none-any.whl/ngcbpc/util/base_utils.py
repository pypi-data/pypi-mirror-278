#
# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import logging

logger = logging.getLogger(__name__)


def get_nvPrettyPrint():
    from ngcbpc.printer.nvPrettyPrint import (  # pylint: disable=import-outside-toplevel
        NVPrettyPrint,
    )

    return NVPrettyPrint()


def get_connection(base_url=None):
    from ngcbpc.api.configuration import (  # pylint: disable=import-outside-toplevel
        Configuration,
    )
    from ngcbpc.api.connection import (  # pylint: disable=import-outside-toplevel
        Connection,
    )

    if base_url is None:
        base_url = Configuration().base_url
    return Connection(base_url)


def get_configuration():
    from ngcbpc.api.configuration import (  # pylint: disable=import-outside-toplevel
        Configuration,
    )

    return Configuration
