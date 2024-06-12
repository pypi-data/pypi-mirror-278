# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from itertools import chain
import json
from typing import Optional

from ngcbpc.api.configuration import Configuration
from ngcbpc.api.pagination import pagination_helper_header_page_reference
from ngcbpc.util.utils import format_org_team, has_org_role

PAGE_SIZE = 100


class TenantAccountAPI:
    def __init__(self, connection, api_client=None):
        self.config = Configuration()
        self.connection = connection
        self.client = api_client

    @staticmethod
    def _get_tenant_account_endpoint(org_name=None, team_name=None):
        org_team = format_org_team(org_name, team_name, plural_form=False)
        return "/".join(["v2", org_team, "forge", "tenant", "account"])

    def list(
        self,
        org: Optional[str] = None,
        team: Optional[str] = None,
        provider: Optional[str] = None,
        tenant: Optional[str] = None,
    ):
        self.config.validate_configuration()
        org_name = org or self.config.org_name
        team_name = team or self.config.team_name
        if not (provider or tenant):
            user_resp = self.client.users.user_who(org_name)
            if has_org_role(user_resp, org_name, ["FORGE_PROVIDER_ADMIN"]):
                provider_info, _ = self.client.forge.provider.info(org_name, team_name)
                provider = provider_info.get("id", "")
            elif has_org_role(user_resp, org_name, ["FORGE_TENANT_ADMIN"]):
                tenant_info, _ = self.client.forge.tenant.info(org_name, team_name)
                tenant = tenant_info.get("id", "")
        ep = self._get_tenant_account_endpoint(org_name, team_name)
        params = []
        if provider:
            params.append(f"infrastructureProviderId={provider}")
        if tenant:
            params.append(f"tenantId={tenant}")
        params.append("includeRelation=InfrastructureProvider")
        params.append("includeRelation=Tenant")
        params.append("orderBy=UPDATED_DESC")
        params.append(f"pageSize={PAGE_SIZE}")
        query = "?".join([ep, "&".join(params)])
        return chain(
            *[
                res
                for res in pagination_helper_header_page_reference(
                    self.connection, query, org_name=org_name, team_name=team_name, operation_name="list_test_account"
                )
                if res
            ]
        )

    def info(
        self,
        tenant_account: str,
        org: Optional[str] = None,
        team: Optional[str] = None,
        provider: Optional[str] = None,
        tenant: Optional[str] = None,
    ):
        self.config.validate_configuration()
        org_name = org or self.config.org_name
        team_name = team or self.config.team_name
        if not (provider or tenant):
            user_resp = self.client.users.user_who(org_name)
            if has_org_role(user_resp, org_name, ["FORGE_PROVIDER_ADMIN"]):
                provider_info, _ = self.client.forge.provider.info(org_name, team_name)
                provider = provider_info.get("id", "")
            elif has_org_role(user_resp, org_name, ["FORGE_TENANT_ADMIN"]):
                tenant_info, _ = self.client.forge.tenant.info(org_name, team_name)
                tenant = tenant_info.get("id", "")
        ep = self._get_tenant_account_endpoint(org_name, team_name)
        url = f"{ep}/{tenant_account}"
        params = []
        if provider:
            params.append(f"infrastructureProviderId={provider}")
        if tenant:
            params.append(f"tenantId={tenant}")
        params.append("includeRelation=InfrastructureProvider")
        params.append("includeRelation=Tenant")
        query = "?".join([url, "&".join(params)])
        resp = self.connection.make_api_request(
            "GET", query, auth_org=org_name, auth_team=team_name, operation_name="info_tenant_account"
        )
        return resp

    def create(
        self,
        tenant_org: str,
        org: Optional[str] = None,
        team: Optional[str] = None,
        provider: Optional[str] = None,
    ):
        self.config.validate_configuration()
        org_name = org or self.config.org_name
        team_name = team or self.config.team_name
        if not provider:
            provider_info, _ = self.client.forge.provider.info(org_name, team_name)
            provider = provider_info.get("id", "")
        url = self._get_tenant_account_endpoint(org_name, team_name)
        create_obj = {
            "infrastructureProviderId": provider,
            "tenantOrg": tenant_org,
        }
        resp = self.connection.make_api_request(
            "POST",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(create_obj),
            operation_name="create_tenant_account",
        )
        return resp

    def update(
        self,
        tenant_account: str,
        org: Optional[str] = None,
        team: Optional[str] = None,
        tenant_contact: Optional[str] = None,
    ):
        self.config.validate_configuration()
        org_name = org or self.config.org_name
        team_name = team or self.config.team_name
        ep = self._get_tenant_account_endpoint(org_name, team_name)
        url = f"{ep}/{tenant_account}"
        update_obj = {
            "tenantContactId": tenant_contact,
        }
        resp = self.connection.make_api_request(
            "PATCH",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(update_obj),
            operation_name="update_tenant_account",
        )
        return resp

    def remove(
        self,
        tenant_account: str,
        org: Optional[str] = None,
        team: Optional[str] = None,
    ):
        self.config.validate_configuration()
        org_name = org or self.config.org_name
        team_name = team or self.config.team_name
        ep = self._get_tenant_account_endpoint(org_name, team_name)
        url = f"{ep}/{tenant_account}"
        resp = self.connection.make_api_request(
            "DELETE",
            url,
            auth_org=org_name,
            auth_team=team_name,
            operation_name="remove_tenant_account",
            json_response=False,
        )
        return resp


class GuestTenantAccountAPI(TenantAccountAPI):
    pass
