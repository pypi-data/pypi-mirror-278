#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from ngcbpc.data.registry.Repository import Repository
from ngcbpc.transformer import BaseSearchTransformer


class ChartSearchTransformer(Repository, BaseSearchTransformer):
    SEARCH_RESOURCE_KEY_MAPPING = {}
    SEARCH_RESOURCE_TOP_KEY_MAPPING = {
        "canGuestPull": "canGuestDownload",
        "dateCreated": "createdDate",
        "dateModified": "updatedDate",
    }

    def __init__(self, search_response):
        BaseSearchTransformer.__init__(self, search_response)
        Repository.__init__(self, self._resources)

    def __getitem__(self, k):
        return self
