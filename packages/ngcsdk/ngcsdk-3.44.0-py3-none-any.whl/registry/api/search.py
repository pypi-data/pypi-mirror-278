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
import itertools

from ngcbpc.api.search import SearchAPI
from ngcbpc.data.search.SearchParamFilter import SearchParamFilter
from registry.transformer.chart import ChartSearchTransformer
from registry.transformer.collection import CollectionSearchTransformer
from registry.transformer.image import RepositorySearchTransformer
from registry.transformer.model import ModelSearchTransformer
from registry.transformer.model_script import ModelScriptSearchTransformer


# pylint: disable=super-init-not-called
class RegistrySearchAPI(SearchAPI):
    def __init__(self, connection):
        self.connection = connection

    def search_repo(self, org, team, resource_matcher, signed=False, access_type=None, product_names=None):
        """Get a list of images."""
        priv_result = []
        filter_list = [SearchParamFilter({"field": "signedImages", "value": True})] if signed else []
        filter_list.extend(
            [SearchParamFilter({"field": "accessType", "value": f'"{access_type}"'})] if access_type else []
        )
        if product_names:
            for product in product_names:
                filter_list.extend([SearchParamFilter({"field": "productNames", "value": f"{product.lower()}"})])

        if org or team:
            priv_result = self._run_search_query(
                "CONTAINER", resource_matcher, org=org, team=team, filter_list=filter_list
            )
        pub_result = self._run_search_query("CONTAINER", resource_matcher, org=None, team=None, filter_list=filter_list)
        all_result = list(set(itertools.chain(priv_result, pub_result)))
        yield [RepositorySearchTransformer(res) for res in all_result]

    def search_model(self, org, team, resource_matcher, access_type=None, product_names=None):
        """Get a list of models."""
        priv_result = []
        filter_list = [SearchParamFilter({"field": "accessType", "value": access_type})] if access_type else []
        if product_names:
            for product in product_names:
                filter_list.extend([SearchParamFilter({"field": "productNames", "value": f"{product.lower()}"})])
        if org or team:
            priv_result = self._run_search_query("MODEL", resource_matcher, org=org, team=team, filter_list=filter_list)
        pub_result = self._run_search_query("MODEL", resource_matcher, org=None, team=None, filter_list=filter_list)
        all_result = list(set(itertools.chain(priv_result, pub_result)))
        yield [ModelSearchTransformer(res) for res in all_result]

    def search_resource(self, org, team, resource_matcher, access_type=None, product_names=None):
        """Get a list of resources."""
        priv_result = []
        filter_list = [SearchParamFilter({"field": "accessType", "value": access_type})] if access_type else []
        if product_names:
            for product in product_names:
                filter_list.extend([SearchParamFilter({"field": "productNames", "value": f"{product.lower()}"})])
        if org or team:
            priv_result = self._run_search_query(
                "RECIPE", resource_matcher, org=org, team=team, filter_list=filter_list
            )
        pub_result = self._run_search_query("RECIPE", resource_matcher, org=None, team=None, filter_list=filter_list)
        all_result = list(set(itertools.chain(priv_result, pub_result)))
        yield [ModelScriptSearchTransformer(res) for res in all_result]

    def search_charts(self, org, team, resource_matcher, access_type=None, product_names=None):
        """Get a list of charts."""
        priv_result = []
        filter_list = [SearchParamFilter({"field": "accessType", "value": access_type})] if access_type else []
        if product_names:
            for product in product_names:
                filter_list.extend([SearchParamFilter({"field": "productNames", "value": f"{product.lower()}"})])
        if org or team:
            priv_result = self._run_search_query(
                "HELM_CHART", resource_matcher, org=org, team=team, filter_list=filter_list
            )
        pub_result = self._run_search_query(
            "HELM_CHART", resource_matcher, org=None, team=None, filter_list=filter_list
        )
        all_result = list(set(itertools.chain(priv_result, pub_result)))
        yield [ChartSearchTransformer(res) for res in all_result]

    def search_collections(self, org, team, resource_matcher):
        """Get a list of collections."""
        priv_result = []
        if org or team:
            priv_result = self._run_search_query("COLLECTION", resource_matcher, org=org, team=team)
        pub_result = self._run_search_query("COLLECTION", resource_matcher, org=None, team=None)
        all_result = list(set(itertools.chain(priv_result, pub_result)))
        yield [CollectionSearchTransformer(res) for res in all_result]


class RegistryGuestSearchAPI(RegistrySearchAPI):
    @staticmethod
    def _get_search_endpoint(resource_name, org=None, team=None):
        return "v2/search/catalog/resources/{}".format(resource_name)
