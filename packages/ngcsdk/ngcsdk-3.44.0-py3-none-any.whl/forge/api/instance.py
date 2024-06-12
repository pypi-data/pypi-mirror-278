# Copyright (c) 2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from itertools import chain
import json

from ngcbpc.api.pagination import pagination_helper_header_page_reference
from ngcbpc.util.utils import format_org_team

PAGE_SIZE = 100


class InstanceAPI:
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _get_instance_endpoint(org_name=None, team_name=None):
        org_team = format_org_team(org_name, team_name, plural_form=False)
        return "/".join(["v2", org_team, "forge", "instance"])

    def list(self, org_name, team_name, site, vpc, provider, tenant, target, status):
        ep = self._get_instance_endpoint(org_name, team_name)
        params = []
        if provider:
            params.append(f"infrastructureProviderId={provider}")
        if tenant:
            params.append(f"tenantId={tenant}")
        if site:
            params.append(f"siteId={site}")
        if vpc:
            params.append(f"vpcId={vpc}")
        if target:
            params.append(f"query={target}")
        if status:
            params.append(f"status={status}")
        params.append("includeRelation=InfrastructureProvider")
        params.append("includeRelation=Tenant")
        params.append("includeRelation=Site")
        params.append("includeRelation=InstanceType")
        params.append("includeRelation=Allocation")
        params.append("includeRelation=Vpc")
        params.append("includeRelation=Machine")
        params.append("includeRelation=OperatingSystem")
        params.append("orderBy=UPDATED_DESC")
        params.append(f"pageSize={PAGE_SIZE}")
        query = "?".join([ep, "&".join(params)])
        return chain(
            *[
                res
                for res in pagination_helper_header_page_reference(
                    self.connection, query, org_name=org_name, team_name=team_name, operation_name="list_instance"
                )
                if res
            ]
        )

    def info(self, org_name, team_name, instance):
        ep = self._get_instance_endpoint(org_name, team_name)
        url = f"{ep}/{instance}"
        params = []
        params.append("includeRelation=InfrastructureProvider")
        params.append("includeRelation=Tenant")
        params.append("includeRelation=Site")
        params.append("includeRelation=InstanceType")
        params.append("includeRelation=Allocation")
        params.append("includeRelation=Vpc")
        params.append("includeRelation=Machine")
        params.append("includeRelation=OperatingSystem")
        query = "?".join([url, "&".join(params)])
        resp = self.connection.make_api_request(
            "GET", query, auth_org=org_name, auth_team=team_name, operation_name="info_instance"
        )
        return resp

    def create(
        self,
        org_name,
        team_name,
        name,
        tenant,
        instance_type,
        vpc,
        operating_system,
        user_data,
        ipxe_script,
        always_boot_custom_ipxe,
        interfaces,
        infiniband_interfaces,
        ssh_key_group,
        labels,
    ):
        url = self._get_instance_endpoint(org_name, team_name)
        create_obj = {
            "name": name,
            "tenantId": tenant,
            "instanceTypeId": instance_type,
            "vpcId": vpc,
            "operatingSystemId": operating_system,
            "userdata": user_data,
            "ipxeScript": ipxe_script,
            "alwaysBootWithCustomIpxe": always_boot_custom_ipxe,
            "interfaces": interfaces,
            "infinibandInterfaces": infiniband_interfaces,
            "sshKeyGroupsIds": ssh_key_group,
            "labels": labels,
        }
        resp = self.connection.make_api_request(
            "POST",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(create_obj),
            operation_name="create_instance",
        )
        return resp

    def update(self, org_name, team_name, instance, name, reboot, reboot_custom_ipxe):
        ep = self._get_instance_endpoint(org_name, team_name)
        url = f"{ep}/{instance}"
        update_obj = {
            "name": name,
            "triggerReboot": reboot,
            "rebootWithCustomIpxe": reboot_custom_ipxe,
        }
        resp = self.connection.make_api_request(
            "PATCH",
            url,
            auth_org=org_name,
            auth_team=team_name,
            payload=json.dumps(update_obj),
            operation_name="update_instance",
        )
        return resp

    def remove(self, org_name, team_name, instance):
        ep = self._get_instance_endpoint(org_name, team_name)
        url = f"{ep}/{instance}"
        resp = self.connection.make_api_request(
            "DELETE",
            url,
            auth_org=org_name,
            auth_team=team_name,
            operation_name="remove_instance",
            json_response=False,
        )
        return resp

    def list_interface(self, org_name, team_name, instance):
        ep = self._get_instance_endpoint(org_name, team_name)
        url = f"{ep}/{instance}/interface"
        return chain(
            *[
                res
                for res in pagination_helper_header_page_reference(
                    self.connection,
                    url,
                    org_name=org_name,
                    team_name=team_name,
                    operation_name="list_instance_interface",
                )
                if res
            ]
        )


class GuestInstanceAPI(InstanceAPI):
    pass
