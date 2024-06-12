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

from typing import Optional

from ngcbpc.api.pagination import pagination_helper
from ngcbpc.constants import API_VERSION, PAGE_SIZE
from ngcbpc.data.uis.Organization import Organization
from ngcbpc.data.uis.OrgListResponse import OrgListResponse
from ngcbpc.util.utils import extra_args


class OrgAPI:
    def __init__(self, connection):
        self.connection = connection

    def get_org_list(self):
        """List all the organizations user can access."""
        query = f"{API_VERSION}/orgs?page-size={PAGE_SIZE}"
        return self._helper_get_orgs(query)

    @extra_args
    def list(self):
        """List all the organizations user can access."""
        self.connection.configuration.validate_configuration(csv_allowed=True)
        return self.get_org_list()

    def get_org_detail(self, org_name: str):
        """List details of an organization."""
        response = self.connection.make_api_request(
            "GET",
            f"{API_VERSION}/orgs/{org_name}",
            auth_org=org_name,
            operation_name="get org details",
        )
        return Organization(response.get("organizations", {}))

    @extra_args
    def info(self, org: Optional[str] = None):
        """Get details of an organization."""
        self.connection.configuration.validate_configuration()
        org_name = org or self.connection.configuration.org_name
        return self.get_org_detail(org_name=org_name)

    def _helper_get_orgs(self, query):
        """Helper command to get list of all the orgs using pagination."""
        orgs_list_pages = pagination_helper(self.connection, query, operation_name="get orgs")
        list_of_orgs = []
        for page in orgs_list_pages:
            list_of_orgs.extend(OrgListResponse(page).organizations)
        return list_of_orgs
