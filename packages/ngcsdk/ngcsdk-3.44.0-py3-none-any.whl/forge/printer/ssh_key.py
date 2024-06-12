# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from ngcbpc.printer.nvPrettyPrint import NVPrettyPrint


class SSHKeyPrinter(NVPrettyPrint):
    """Forge Ssh Key Printer"""

    def print_list(self, ssh_key_list, columns=None):

        if self.config.format_type == "json":
            output = ssh_key_list
        else:
            output = []
            if not columns:
                columns = [
                    ("id", "Id"),
                    ("name", "Name"),
                    ("org", "Org"),
                    ("tenantName", "Tenant Name"),
                    ("fingerprint", "Fingerprint"),
                    ("isGlobal", "Global"),
                    ("expires", "Expiration"),
                    ("created", "Created"),
                    ("updated", "Updated"),
                ]
            cols, disp = zip(*columns)
            output = [list(disp)]
            for ssh_key in ssh_key_list:
                out = SSHKeyOutput(ssh_key, self.config)
                output.append([getattr(out, col, None) for col in cols])
        self.print_data(output, True)

    def print_info(self, ssh_key):

        if self.config.format_type == "json":
            self.print_data(ssh_key)
        else:
            output = SSHKeyOutput(ssh_key)
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            tbl.set_title("Ssh Key Information")
            tbl.add_label_line("Id", output.id)
            tbl.add_label_line("Name", output.name)
            tbl.add_label_line("Org", output.org)
            tbl.add_label_line("Tenant Id", output.tenantId)
            tbl.add_label_line("Fingerprint", output.fingerprint)
            tbl.add_label_line("Global", output.isGlobal)
            tbl.add_label_line("Expiration", output.expires)
            tbl.add_label_line("Created", output.created)
            tbl.add_label_line("Updated", output.updated)
            tbl.add_separator_line()
            for ea in output.entityAssociations or []:
                eao = EntityAssociationOutput(ea)
                st_tbl = self.add_sub_table(parent_table=tbl, outline=True, level=1)
                st_tbl.add_label_line("Id", eao.id)
                st_tbl.add_label_line("Ssh Key Id", eao.sshKeyId)
                st_tbl.add_label_line("Entity Type", eao.entityType)
                st_tbl.add_label_line("Entity Id", eao.entityId)
                st_tbl.add_label_line("Created", eao.created)
                st_tbl.add_label_line("Updated", eao.updated)
                tbl.add_separator_line()
            tbl.print()


class SSHKeyOutput:
    def __init__(self, ssh_key, config=None):
        self.ssh_key = ssh_key
        self.config = config

    @property
    def id(self):
        return self.ssh_key.get("id", "")

    @property
    def name(self):
        return self.ssh_key.get("name", "")

    @property
    def org(self):
        return self.ssh_key.get("org", "")

    @property
    def tenantId(self):
        return self.ssh_key.get("tenantId", "")

    @property
    def fingerprint(self):
        return self.ssh_key.get("fingerprint", "")

    @property
    def isGlobal(self):
        return self.ssh_key.get("isGlobal", "")

    @property
    def entityAssociations(self):
        return self.ssh_key.get("entityAssociations", [])

    @property
    def expires(self):
        return self.ssh_key.get("expires", "")

    @property
    def created(self):
        return self.ssh_key.get("created", "")

    @property
    def updated(self):
        return self.ssh_key.get("updated", "")

    @property
    def tenantName(self):
        return self.ssh_key.get("tenant", {}).get("orgDisplayName", "")


class EntityAssociationOutput:
    def __init__(self, entity_out):
        self.entity_out = entity_out

    @property
    def id(self):
        return self.entity_out.get("id", "")

    @property
    def sshKeyId(self):
        return self.entity_out.get("sshKeyId", "")

    @property
    def entityType(self):
        return self.entity_out.get("entityType", "")

    @property
    def entityId(self):
        return self.entity_out.get("entityId", "")

    @property
    def created(self):
        return self.entity_out.get("created", "")

    @property
    def updated(self):
        return self.entity_out.get("updated", "")
