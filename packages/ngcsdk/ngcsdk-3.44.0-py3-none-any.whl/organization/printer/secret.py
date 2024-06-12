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

from ngcbpc.printer.nvPrettyPrint import NVPrettyPrint, str_


class SecretPrinter(NVPrettyPrint):
    """Printer for Secrets module"""

    def print_secret_list(self, secrets):
        """Prints Secrets Similar to WebUI"""
        output = []
        if self.config.format_type == "json":
            output = secrets or []
        else:
            columns = [
                ("name", "Name"),
                ("description", "Description"),
                ("number_of_keypairs", "# of Keypairs"),
                ("enabled", "enabled"),
            ]
            output = self.generate_secret_list([secrets.secrets] or [], columns)

        self.print_data(output, is_table=True)

    def print_secret_info(self, secret_info):
        if self.config.format_type == "json":
            self.print_data(secret_info)
            return
        tbl = self.create_output(header=False, outline=True)
        tbl.set_title("Secret Details")
        tbl.add_separator_line()
        tbl.add_label_line("Description", secret_info.description)
        tbl.add_label_line("Enabled", secret_info.enabled)
        content_tbl = self.add_sub_table(outline=True, detail_style=False)
        content_tbl.set_title("Secret Pairs")
        for kv in secret_info.kv or []:
            content_tbl.add_label_line(kv.key, kv.value)
        tbl.add_separator_line()
        tbl.print()

    @staticmethod
    def generate_secret_list(secrets_list, columns):
        cols, disp = zip(*columns)
        yield list(disp)

        for secrets in secrets_list or []:
            for secret in secrets or []:
                out = SecretOutput(secret)
                yield [getattr(out, col, None) for col in cols]


class SecretOutput:
    def __init__(self, secret):
        self.secret = secret

    @property
    def name(self):
        return str_(self.secret.name)

    @property
    def description(self):
        return str_(self.secret.description)

    @property
    def number_of_keypairs(self):
        return len(self.secret.kv) or 0

    @property
    def enabled(self):
        return self.secret.enabled
