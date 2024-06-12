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

#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from basecommand.api.quickstart_cluster import (
    GuestQuickStartClusterAPI,
    QuickStartClusterAPI,
)
from basecommand.api.quickstart_project import (
    GuestQuickStartProjectAPI,
    QuickStartProjectAPI,
)
from ngcbpc.api.configuration import Configuration


class BaseQuickStartAPI:
    def __init__(self, connection):
        self._connection = connection

    @property
    def cluster(self) -> QuickStartClusterAPI:
        if Configuration().app_key:
            return QuickStartClusterAPI(connection=self._connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestQuickStartClusterAPI(connection=self._connection)

    @property
    def project(self) -> QuickStartProjectAPI:
        if Configuration().app_key:
            return QuickStartProjectAPI(connection=self._connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestQuickStartProjectAPI(connection=self._connection)
