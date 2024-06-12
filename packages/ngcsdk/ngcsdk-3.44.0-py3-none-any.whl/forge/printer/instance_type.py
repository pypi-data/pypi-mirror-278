# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from ngcbpc.printer.nvPrettyPrint import NVPrettyPrint


class InstanceTypePrinter(NVPrettyPrint):
    """Forge InstanceType Printer"""

    def print_list(self, instance_type_list, columns=None):

        if self.config.format_type == "json":
            output = instance_type_list
        else:
            output = []
            if not columns:
                columns = [
                    ("id", "Id"),
                    ("name", "Name"),
                    ("displayName", "Display Name"),
                    ("controllerMachineType", "Controller Machine Type"),
                    ("status", "Status"),
                    ("created", "Created"),
                    ("updated", "Updated"),
                ]
            cols, disp = zip(*columns)
            output = [list(disp)]
            for instance_type in instance_type_list:
                out = InstanceTypeOutput(instance_type, self.config)
                output.append([getattr(out, col, "") for col in cols])
        self.print_data(output, True)

    def print_info(self, instance_type, status_history=False):

        if self.config.format_type == "json":
            self.print_data(instance_type)
        else:
            output = InstanceTypeOutput(instance_type)
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            tbl.set_title("Instance Type Information")
            tbl.add_label_line("Id", output.id)
            tbl.add_label_line("Name", output.name)
            tbl.add_label_line("Display Name", output.displayName)
            tbl.add_label_line("Description", output.description)
            tbl.add_label_line("Controller Machine Type", output.controllerMachineType)
            tbl.add_label_line("Infrastructure Provider Id", output.infrastructureProviderId)
            tbl.add_label_line("Infrastructure Provider Name", output.infrastructureProviderName)
            tbl.add_label_line("Site Id", output.siteId)
            tbl.add_label_line("Site Name", output.siteName)
            tbl.add_label_line("Status", output.status)
            tbl.add_label_line("Created", output.created)
            tbl.add_label_line("Updated", output.updated)
            tbl.add_separator_line()
            if output.allocationStats:
                as_tbl = self.add_sub_table(parent_table=tbl, outline=True, level=1)
                as_tbl.set_title("Allocation Stats")
                as_tbl.add_label_line("Total", output.allocationStatsTotal)
                as_tbl.add_label_line("Used", output.allocationStatsUsed)
                tbl.add_separator_line()
            for mc in output.machineCapabilities:
                mco = MachineCapabilityOutput(mc)
                mc_tbl = self.add_sub_table(parent_table=tbl, outline=True, level=1)
                mc_tbl.set_title("Machine Capability")
                mc_tbl.add_label_line("Type", mco.type)
                mc_tbl.add_label_line("Name", mco.name)
                mc_tbl.add_label_line("Frequency", mco.frequency)
                mc_tbl.add_label_line("Cores", mco.cores)
                mc_tbl.add_label_line("Threads", mco.threads)
                mc_tbl.add_label_line("Capacity", mco.capacity)
                mc_tbl.add_label_line("Count", mco.count)
                tbl.add_separator_line()
            if status_history:
                for sh in output.status_history:
                    sho = StatusHistoryOutput(sh)
                    st_tbl = self.add_sub_table(parent_table=tbl, outline=True, level=1)
                    st_tbl.add_label_line("Status", sho.status)
                    st_tbl.add_label_line("Message", sho.message)
                    st_tbl.add_label_line("Created", sho.created)
                    st_tbl.add_label_line("Updated", sho.updated)
                    tbl.add_separator_line()
            tbl.print()

    def print_list_machine(self, itm_list):

        if self.config.format_type == "json":
            output = itm_list
        else:
            output = []
            columns = [
                ("id", "Association Id"),
                ("machineId", "Machine Id"),
                ("instanceTypeId", "Instance Type Id"),
                ("created", "Created"),
                ("updated", "Updated"),
            ]
            cols, disp = zip(*columns)
            output = [list(disp)]
            for itm in itm_list:
                out = InstanceTypeMachineOutput(itm)
                output.append([getattr(out, col, None) for col in cols])
        self.print_data(output, True)

    def print_info_machine(self, itm_list):

        if self.config.format_type == "json":
            self.print_data(itm_list)
        else:
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            for itm in itm_list:
                itmo = InstanceTypeMachineOutput(itm)
                itm_tbl = self.add_sub_table(parent_table=tbl, outline=True, level=1)
                itm_tbl.set_title("Instance Type Machine")
                itm_tbl.add_label_line("Association Id", itmo.id)
                itm_tbl.add_label_line("Machine Id", itmo.machineId)
                itm_tbl.add_label_line("Instance Type Id", itmo.instanceTypeId)
                itm_tbl.add_label_line("Created", itmo.created)
                itm_tbl.add_label_line("Updated", itmo.updated)
                tbl.add_separator_line()


class InstanceTypeOutput:
    def __init__(self, instance_type, config=None):
        self.instance_type = instance_type
        self.config = config

    @property
    def id(self):
        return self.instance_type.get("id", "")

    @property
    def name(self):
        return self.instance_type.get("name", "")

    @property
    def displayName(self):
        return self.instance_type.get("displayName", "")

    @property
    def description(self):
        return self.instance_type.get("description", "")

    @property
    def controllerMachineType(self):
        return self.instance_type.get("controllerMachineType", "")

    @property
    def infrastructureProviderId(self):
        return self.instance_type.get("infrastructureProviderId", "")

    @property
    def siteId(self):
        return self.instance_type.get("siteId", "")

    @property
    def machineCapabilities(self):
        return self.instance_type.get("machineCapabilities", "")

    @property
    def status(self):
        return self.instance_type.get("status", "")

    @property
    def status_history(self):
        return self.instance_type.get("statusHistory", "")

    @property
    def created(self):
        return self.instance_type.get("created", "")

    @property
    def updated(self):
        return self.instance_type.get("updated", "")

    @property
    def siteName(self):
        return self.instance_type.get("site", {}).get("name", "")

    @property
    def infrastructureProviderName(self):
        return self.instance_type.get("infrastructureProvider", {}).get("orgDisplayName", "")

    @property
    def allocationStats(self):
        return self.instance_type.get("allocationStats", {})

    @property
    def allocationStatsTotal(self):
        return self.instance_type.get("allocationStats", {}).get("total", "")

    @property
    def allocationStatsUsed(self):
        return self.instance_type.get("allocationStats", {}).get("used", "")


class MachineCapabilityOutput:
    def __init__(self, machine_capability):
        self.machine_capability = machine_capability

    @property
    def type(self):
        return self.machine_capability.get("type", "")

    @property
    def name(self):
        return self.machine_capability.get("name", "")

    @property
    def frequency(self):
        return self.machine_capability.get("frequency", "")

    @property
    def cores(self):
        return self.machine_capability.get("cores", "")

    @property
    def threads(self):
        return self.machine_capability.get("threads", "")

    @property
    def capacity(self):
        return self.machine_capability.get("capacity", "")

    @property
    def count(self):
        return self.machine_capability.get("count", "")


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


class InstanceTypeMachineOutput:
    def __init__(self, itm_out):
        self.itm_out = itm_out

    @property
    def id(self):
        return self.itm_out.get("id", "")

    @property
    def machineId(self):
        return self.itm_out.get("machineId", "")

    @property
    def instanceTypeId(self):
        return self.itm_out.get("instanceTypeId", "")

    @property
    def created(self):
        return self.itm_out.get("created", "")

    @property
    def updated(self):
        return self.itm_out.get("updated", "")
