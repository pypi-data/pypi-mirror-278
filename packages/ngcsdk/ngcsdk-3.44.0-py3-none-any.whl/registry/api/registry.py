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
from ngcbpc.api.configuration import Configuration
from ngcbpc.api.connection import Connection
from ngcbpc.environ import NGC_CLI_SEARCH_SERVICE_URL
from registry.api.chart import ChartAPI, GuestChartAPI
from registry.api.collection import CollectionAPI
from registry.api.csp import CSPAPI
from registry.api.deploy import DeployAPI
from registry.api.image import GuestImageAPI, ImageAPI
from registry.api.label_set import GuestLabelSetAPI, LabelSetAPI
from registry.api.models import GuestModelAPI, ModelAPI
from registry.api.playground import GuestPlaygroundAPI, PlaygroundAPI
from registry.api.publish import PublishAPI
from registry.api.resources import GuestResourceAPI, ResourceAPI
from registry.api.search import RegistryGuestSearchAPI, RegistrySearchAPI
from registry.api.utils import get_helm_repo_url, get_label_set_url


class RegistryAPI:
    def __init__(self, connection, api_client):
        self.connection = connection
        self.api_client = api_client
        self.chart_repo_connection = Connection(base_url=get_helm_repo_url())
        self.label_set_connection = Connection(base_url=get_label_set_url())

    @property
    def model(self):
        if Configuration().app_key:
            return ModelAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestModelAPI(connection=self.connection, api_client=self.api_client)

    @property
    def chart(self):
        if Configuration().app_key:
            return ChartAPI(
                connection=self.connection, api_client=self.api_client, repo_connection=self.chart_repo_connection
            )
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestChartAPI(
            connection=self.connection, api_client=self.api_client, repo_connection=self.chart_repo_connection
        )

    @property
    def image(self):
        if Configuration().app_key:
            return ImageAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        ret = GuestImageAPI(connection=self.connection, api_client=self.api_client)
        return ret

    @property
    def resource(self):
        if Configuration().app_key:
            return ResourceAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestResourceAPI(connection=self.connection, api_client=self.api_client)

    @property
    def label_set(self):
        if Configuration().app_key:
            return LabelSetAPI(connection=self.connection, label_set_connection=self.label_set_connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestLabelSetAPI(connection=self.connection)

    @property
    def collection(self):
        return CollectionAPI(connection=self.connection)

    @property
    def publish(self):
        return PublishAPI(connection=self.connection)

    @property
    def csp(self):
        return CSPAPI(connection=self.connection)

    @property
    def deploy(self):
        return DeployAPI(connection=self.connection)

    @property
    def search(self):
        connection = Connection(base_url=NGC_CLI_SEARCH_SERVICE_URL) if NGC_CLI_SEARCH_SERVICE_URL else self.connection
        if Configuration().app_key:
            return RegistrySearchAPI(connection=connection)
            # guest is wide open and can access w/o api key
            # internally this is a different api endpoint
        return RegistryGuestSearchAPI(connection=connection)

    @property
    def playground(self):
        if Configuration().app_key:
            return PlaygroundAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestPlaygroundAPI(connection=self.connection, api_client=self.api_client)
