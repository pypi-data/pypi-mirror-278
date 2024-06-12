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

from basecommand.api.aces import AceAPI
from basecommand.api.datamover import DataMoverAPI
from basecommand.api.dataset import DatasetAPI
from basecommand.api.jobs import JobsAPI
from basecommand.api.measurements import MeasurementsAPI
from basecommand.api.quickstart import BaseQuickStartAPI
from basecommand.api.resource import ResourceAPI
from basecommand.api.resultset import ResultsetAPI
from basecommand.api.search import BaseCommandSearchAPI
from basecommand.api.utils import get_data_mover_service_url, get_dataset_service_url
from basecommand.api.workspace import WorkspaceAPI
from ngcbpc.api.connection import Connection
from ngcbpc.environ import NGC_CLI_SEARCH_SERVICE_URL


class BasecommandAPI:
    def __init__(self, connection, api_client):
        self.connection = connection
        self.api_client = api_client
        self.data_mover_connection = Connection(base_url=get_data_mover_service_url())
        self.dataset_service_connection = Connection(base_url=get_dataset_service_url())

    @property
    def jobs(self):
        return JobsAPI(connection=self.connection, api_client=self.api_client)

    @property
    def measurements(self):
        return MeasurementsAPI(connection=self.connection)

    @property
    def aces(self):
        return AceAPI(connection=self.connection)

    @property
    def dataset(self):
        return DatasetAPI(
            connection=self.connection,
            api_client=self.api_client,
            dataset_service_connection=self.dataset_service_connection,
        )

    @property
    def resultset(self):
        return ResultsetAPI(
            connection=self.connection,
            api_client=self.api_client,
            dataset_service_connection=self.dataset_service_connection,
        )

    @property
    def workspace(self):
        return WorkspaceAPI(
            connection=self.connection,
            api_client=self.api_client,
            dataset_service_connection=self.dataset_service_connection,
        )

    @property
    def quickstart(self) -> BaseQuickStartAPI:
        return BaseQuickStartAPI(connection=self.connection)

    @property
    def data_mover(self):
        return DataMoverAPI(connection=self.data_mover_connection)

    @property
    def search(self):
        connection = Connection(base_url=NGC_CLI_SEARCH_SERVICE_URL) if NGC_CLI_SEARCH_SERVICE_URL else self.connection
        return BaseCommandSearchAPI(connection=connection)

    @property
    def resource(self):
        return ResourceAPI(connection=self.connection)
