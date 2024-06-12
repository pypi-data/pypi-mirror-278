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

from organization.api.alert import AlertAPI
from organization.api.audit import AuditAPI
from organization.api.orgs import OrgAPI
from organization.api.secrets import SecretsAPI
from organization.api.storage import StorageAPI
from organization.api.subscription import SubscriptionAPI
from organization.api.teams import TeamAPI
from organization.api.users import UsersAPI


class API:
    def __init__(self, connection, api_client):
        self.connection = connection
        self.api_client = api_client

    @property
    def alert(self):
        return AlertAPI(connection=self.connection)

    @property
    def audit(self):
        return AuditAPI(connection=self.connection)

    @property
    def organization(self):
        return OrgAPI(connection=self.connection)

    @property
    def secrets(self):
        return SecretsAPI(connection=self.connection)

    @property
    def storage(self):
        return StorageAPI(connection=self.connection)

    @property
    def subscription(self):
        return SubscriptionAPI(connection=self.connection)

    @property
    def team(self):
        return TeamAPI(connection=self.connection)

    @property
    def user(self):
        return UsersAPI(connection=self.connection, api_client=self.api_client)
