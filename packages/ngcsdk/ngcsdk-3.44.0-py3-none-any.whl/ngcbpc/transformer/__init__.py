#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from ngcbpc.data.search.SearchResponseResultResource import SearchResponseResultResource


class BaseSearchTransformer(SearchResponseResultResource):

    SEARCH_RESOURCE_KEY_MAPPING = {}
    SEARCH_RESOURCE_TOP_KEY_MAPPING = {}

    def __init__(self, search_response):
        self._resources = search_response.toDict()
        # handle top level keys
        for from_key, to_key in self.SEARCH_RESOURCE_TOP_KEY_MAPPING.items():
            self._resources.update({to_key: self._resources.get(from_key, None)})
        for attr in search_response.attributes or []:
            self._resources.update({self.SEARCH_RESOURCE_KEY_MAPPING.get(attr.key, attr.key): attr.value})
        for label in search_response.labels or []:
            self._resources.update({self.SEARCH_RESOURCE_KEY_MAPPING.get(label.key, label.key): " ".join(label.values)})
        super().__init__(self._resources)
