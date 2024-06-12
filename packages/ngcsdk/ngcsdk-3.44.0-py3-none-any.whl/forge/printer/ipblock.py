# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from ngcbpc.printer.nvPrettyPrint import NVPrettyPrint


class IpblockPrinter(NVPrettyPrint):
    """Forge Ipblock Printer"""

    def print_list(self, ipblock_list, columns=None):

        if self.config.format_type == "json":
            output = ipblock_list
        else:
            output = []
            if not columns:
                columns = [
                    ("id", "Id"),
                    ("name", "Name"),
                    ("siteName", "Site Name"),
                    ("routingType", "Routing Type"),
                    ("prefix", "Prefix"),
                    ("prefixLength", "Prefix Length"),
                    ("protocolVersion", "Protocol Version"),
                    ("status", "Status"),
                    ("updated", "Updated"),
                ]
            cols, disp = zip(*columns)
            output = [list(disp)]
            for ipblock in ipblock_list:
                out = IpblockOutput(ipblock, self.config)
                output.append([getattr(out, col, None) for col in cols])
        self.print_data(output, True)

    def print_info(self, ipblock, status_history=False):

        if self.config.format_type == "json":
            self.print_data(ipblock)
        else:
            output = IpblockOutput(ipblock)
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            tbl.set_title("Ipblock Information")
            tbl.add_label_line("Id", output.id)
            tbl.add_label_line("Name", output.name)
            tbl.add_label_line("Description", output.description)
            tbl.add_label_line("Site Id", output.siteId)
            tbl.add_label_line("Site Name", output.siteName)
            tbl.add_label_line("Infrastructure Provider Id", output.infrastructureProviderId)
            tbl.add_label_line("Infrastructure Provider Name", output.infrastructureProviderName)
            tbl.add_label_line("Tenant Id", output.tenantId)
            tbl.add_label_line("Tenant Name", output.tenantName)
            tbl.add_label_line("Routing Type", output.routingType)
            tbl.add_label_line("Prefix", output.prefix)
            tbl.add_label_line("Prefix Length", output.prefixLength)
            tbl.add_label_line("Protocol Version", output.protocolVersion)
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


class IpblockOutput:
    def __init__(self, ipblock, config=None):
        self.ipblock = ipblock
        self.config = config

    @property
    def id(self):
        return self.ipblock.get("id", "")

    @property
    def name(self):
        return self.ipblock.get("name", "")

    @property
    def description(self):
        return self.ipblock.get("description", "")

    @property
    def siteId(self):
        return self.ipblock.get("siteId", "")

    @property
    def infrastructureProviderId(self):
        return self.ipblock.get("infrastructureProviderId", "")

    @property
    def tenantId(self):
        return self.ipblock.get("tenantId", "")

    @property
    def routingType(self):
        return self.ipblock.get("routingType", "")

    @property
    def prefix(self):
        return self.ipblock.get("prefix", "")

    @property
    def prefixLength(self):
        return self.ipblock.get("prefixLength", "")

    @property
    def protocolVersion(self):
        return self.ipblock.get("protocolVersion", "")

    @property
    def status(self):
        return self.ipblock.get("status", "")

    @property
    def statusHistory(self):
        return self.ipblock.get("statusHistory", "")

    @property
    def created(self):
        return self.ipblock.get("created", "")

    @property
    def updated(self):
        return self.ipblock.get("updated", "")

    @property
    def siteName(self):
        return self.ipblock.get("site", {}).get("name", "")

    @property
    def infrastructureProviderName(self):
        return self.ipblock.get("infrastructureProvider", {}).get("orgDisplayName", "")

    @property
    def tenantName(self):
        return self.ipblock.get("tenant", {}).get("orgDisplayName", "")


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
