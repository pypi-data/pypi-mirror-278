from forge.api.allocation import AllocationAPI, GuestAllocationAPI
from forge.api.constraint import ConstraintAPI, GuestConstraintAPI
from forge.api.infiniband import GuestInfiniBandPartitionAPI, InfiniBandPartitionAPI
from forge.api.instance import GuestInstanceAPI, InstanceAPI
from forge.api.instance_type import GuestInstanceTypeAPI, InstanceTypeAPI
from forge.api.ipblock import GuestIpblockAPI, IpblockAPI
from forge.api.machine import GuestMachineAPI, MachineAPI
from forge.api.operating_system import GuestOperatingSystemAPI, OperatingSystemAPI
from forge.api.provider import GuestProviderAPI, ProviderAPI
from forge.api.rule import GuestRuleAPI, RuleAPI
from forge.api.site import GuestSiteAPI, SiteAPI
from forge.api.ssh_key import GuestSSHKeyAPI, SSHKeyAPI
from forge.api.ssh_key_group import GuestSSHKeyGroupAPI, SSHKeyGroupAPI
from forge.api.subnet import GuestSubnetAPI, SubnetAPI
from forge.api.tenant import GuestTenantAPI, TenantAPI
from forge.api.tenant_account import GuestTenantAccountAPI, TenantAccountAPI
from forge.api.user import GuestUserAPI, UserAPI
from forge.api.vpc import GuestVpcAPI, VpcAPI
from ngcbpc.api.configuration import Configuration


class ForgeAPI:
    def __init__(self, connection, api_client):
        self.connection = connection
        self.api_client = api_client

    @property
    def provider(self):
        if Configuration().app_key:
            return ProviderAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestProviderAPI(connection=self.connection)

    @property
    def tenant(self):
        if Configuration().app_key:
            return TenantAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestTenantAPI(connection=self.connection)

    @property
    def tenant_account(self):
        if Configuration().app_key:
            return TenantAccountAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestTenantAccountAPI(connection=self.connection)

    @property
    def site(self):
        if Configuration().app_key:
            return SiteAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestSiteAPI(connection=self.connection)

    @property
    def allocation(self):
        if Configuration().app_key:
            return AllocationAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestAllocationAPI(connection=self.connection)

    @property
    def constraint(self):
        if Configuration().app_key:
            return ConstraintAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestConstraintAPI(connection=self.connection)

    @property
    def ipblock(self):
        if Configuration().app_key:
            return IpblockAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestIpblockAPI(connection=self.connection)

    @property
    def vpc(self):
        if Configuration().app_key:
            return VpcAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestVpcAPI(connection=self.connection)

    @property
    def subnet(self):
        if Configuration().app_key:
            return SubnetAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestSubnetAPI(connection=self.connection)

    @property
    def instance(self):
        if Configuration().app_key:
            return InstanceAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestInstanceAPI(connection=self.connection)

    @property
    def instance_type(self):
        if Configuration().app_key:
            return InstanceTypeAPI(connection=self.connection, api_client=self.api_client)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestInstanceTypeAPI(connection=self.connection)

    @property
    def machine(self):
        if Configuration().app_key:
            return MachineAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestMachineAPI(connection=self.connection)

    @property
    def operating_system(self):
        if Configuration().app_key:
            return OperatingSystemAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestOperatingSystemAPI(connection=self.connection)

    @property
    def rule(self):
        if Configuration().app_key:
            return RuleAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestRuleAPI(connection=self.connection)

    @property
    def user(self):
        if Configuration().app_key:
            return UserAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestUserAPI(connection=self.connection)

    @property
    def ssh_key(self):
        if Configuration().app_key:
            return SSHKeyAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestSSHKeyAPI(connection=self.connection)

    @property
    def ssh_key_group(self):
        if Configuration().app_key:
            return SSHKeyGroupAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestSSHKeyGroupAPI(connection=self.connection)

    @property
    def infiniband_partition(self):
        if Configuration().app_key:
            return InfiniBandPartitionAPI(connection=self.connection)
        # guest is wide open and can access w/o api key
        # internally this is a different api endpoint
        return GuestInfiniBandPartitionAPI(connection=self.connection)
