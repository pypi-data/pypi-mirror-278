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

#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from ngcbpc.printer.nvPrettyPrint import NVPrettyPrint


class FunctionPrinter(NVPrettyPrint):
    """NVCF Function Printer"""

    def print_list(self, function_list, columns=None):
        if self.config.format_type == "json":
            output = function_list
        else:
            columns = [
                ("name", "Name"),
                ("id", "Id"),
                ("version", "Version"),
                ("containerImage", "Container"),
                ("helmChart", "Helm Chart"),
                ("status", "Status"),
            ]
            cols, disp = zip(*columns)
            output = [list(disp)]
            for function in function_list:
                out = FunctionOutput(function)
                output.append([getattr(out, col, "") for col in cols])
        self.print_data(output, True)

    def print_info(self, function):
        if self.config.format_type == "json":
            self.print_data(function)
        else:
            output = FunctionOutput(function)
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            tbl.set_title("Function Information")
            tbl.add_label_line("Name", output.name)
            tbl.add_label_line("Version", output.version)
            tbl.add_label_line("ID", output.id)
            tbl.add_label_line("Status", output.status)
            tbl.add_label_line("Inference URL", output.inferenceUrl)

            if output.helmChart:
                tbl.add_label_line("Helm Chart", output.helmChart)
                tbl.add_label_line("Helm Chart Service Name", output.helmChartServiceName)

            if output.containerImage:
                tbl.add_label_line("Container Image", output.containerImage)
            if output.models:
                model_output = ", ".join([f"{model.get('name')}/{model.get('version')}" for model in output.models])
                tbl.add_label_line("Models", model_output)

            tbl.add_separator_line()
            tbl.print()


class FunctionOutput:
    def __init__(self, function):
        self.function = function

    @property
    def activeInstances(self):
        return self.function.get("activeInstances", None)

    @property
    def containerImage(self):
        return self.function.get("containerImage", "")

    @property
    def helmChart(self):
        return self.function.get("helmChart", "")

    @property
    def helmChartServiceName(self):
        return self.function.get("helmChartServiceName", "")

    @property
    def gpus(self):
        return self.function.get("gpus", "")

    @property
    def id(self):
        return self.function.get("id", "")

    @property
    def inferenceUrl(self):
        return self.function.get("inferenceUrl", "")

    @property
    def maxInstances(self):
        return self.function.get("maxInstances", "")

    @property
    def minInstances(self):
        return self.function.get("minInstances", "")

    @property
    def models(self):
        return self.function.get("models", None)

    @property
    def name(self):
        return self.function.get("name", "")

    @property
    def status(self):
        return self.function.get("status", "")

    @property
    def version(self):
        return self.function.get("versionId", "")
