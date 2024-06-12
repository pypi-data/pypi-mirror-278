# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from ngcbpc.printer.nvPrettyPrint import NVPrettyPrint


class VpcPrinter(NVPrettyPrint):
    """Forge Vpc Printer"""

    def print_list(self, vpc_list, columns=None):

        if self.config.format_type == "json":
            output = vpc_list
        else:
            output = []
            if not columns:
                columns = [
                    ("id", "Id"),
                    ("name", "Name"),
                    ("siteName", "Site Name"),
                    ("infrastructureProviderName", "Infrastructure Provider Name"),
                    ("status", "Status"),
                    ("updated", "Updated"),
                ]
            cols, disp = zip(*columns)
            output = [list(disp)]
            for vpc in vpc_list:
                out = VpcOutput(vpc, self.config)
                output.append([getattr(out, col, None) for col in cols])
        self.print_data(output, True)

    def print_info(self, vpc, status_history=False):

        if self.config.format_type == "json":
            self.print_data(vpc)
        else:
            output = VpcOutput(vpc)
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            tbl.set_title("VPC Information")
            tbl.add_label_line("Id", output.id)
            tbl.add_label_line("Name", output.name)
            tbl.add_label_line("Description", output.description)
            tbl.add_label_line("Org", output.org)
            tbl.add_label_line("Tenant Id", output.tenantId)
            tbl.add_label_line("Tenant Name", output.tenantName)
            tbl.add_label_line("Site Id", output.siteId)
            tbl.add_label_line("Site Name", output.siteName)
            tbl.add_label_line("Infrastructure Provider Id", output.infrastructureProviderId)
            tbl.add_label_line("Infrastructure Provider Name", output.infrastructureProviderName)
            tbl.add_label_line("Status", output.status)
            tbl.add_label_line("Created", output.created)
            tbl.add_label_line("Updated", output.updated)
            tbl.add_separator_line()
            if status_history:
                for sh in output.statusHistory:
                    sho = StatusHistoryOutput(sh)
                    st_tbl = self.add_sub_table(parent_table=tbl, outline=True, level=1)
                    st_tbl.add_label_line("Status", sho.status)
                    st_tbl.add_label_line("Message", sho.message)
                    st_tbl.add_label_line("Created", sho.created)
                    st_tbl.add_label_line("Updated", sho.updated)
                    tbl.add_separator_line()
            tbl.print()


class VpcOutput:
    def __init__(self, vpc, config=None):
        self.vpc = vpc
        self.config = config

    @property
    def id(self):
        return self.vpc.get("id", "")

    @property
    def name(self):
        return self.vpc.get("name", "")

    @property
    def description(self):
        return self.vpc.get("description", "")

    @property
    def org(self):
        return self.vpc.get("org", "")

    @property
    def tenantId(self):
        return self.vpc.get("tenantId", "")

    @property
    def siteId(self):
        return self.vpc.get("siteId", "")

    @property
    def status(self):
        return self.vpc.get("status", "")

    @property
    def statusHistory(self):
        return self.vpc.get("statusHistory", "")

    @property
    def created(self):
        return self.vpc.get("created", "")

    @property
    def updated(self):
        return self.vpc.get("updated", "")

    @property
    def siteName(self):
        return self.vpc.get("site", {}).get("name", "")

    @property
    def tenantName(self):
        return self.vpc.get("tenant", {}).get("orgDisplayName", "")

    @property
    def infrastructureProviderId(self):
        return self.vpc.get("infrastructureProvider", {}).get("id", "")

    @property
    def infrastructureProviderName(self):
        return self.vpc.get("infrastructureProvider", {}).get("orgDisplayName", "")


class StatusHistoryOutput:
    def __init__(self, status_out):
        self.status_out = status_out

    @property
    def status(self):
        return self.status_out.get("status", "")

    @property
    def message(self):
        return self.status_out.get("message", "")

    @property
    def created(self):
        return self.status_out.get("created", "")

    @property
    def updated(self):
        return self.status_out.get("updated", "")
