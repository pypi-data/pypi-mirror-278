#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from itertools import chain

from ngcbpc.printer.nvPrettyPrint import (
    format_date,
    GeneralWrapper,
    NVPrettyPrint,
    str_,
)
from ngcbpc.printer.utils import format_label, format_list_view_date
from ngcbpc.util.file_utils import human_size
from registry.api.utils import format_repo


class ChartPrinter(NVPrettyPrint):
    """The printer is responsible for printing objects and lists of objects of the associated type"""

    def print_chart_list(self, chart_list, columns=None):
        """Handles the output for `ngc registry chart list`"""
        output = []
        if self.config.format_type == "json":
            output = chain(*chart_list)
        else:
            if not columns:
                columns = [
                    ("name", "Name"),
                    ("repository", "Repository"),
                    ("version", "Version"),
                    ("size", "Size"),
                    ("createdBy", "Created By"),
                    ("description", "Description"),
                    ("dateCreated", "Created Date"),
                    ("dateModified", "Last Modified"),
                    ("accessType", "Access Type"),
                    ("productNames", "Associated Products"),
                ]
            output = self.generate_chart_list(chart_list, self.config, columns)
        self.print_data(output, is_table=True)

    def print_chart_version_list(self, version_list, columns=None, main_chart=None):
        """Handles the output for `ngc registry chart list <chart:version>`"""
        output = []

        if self.config.format_type == "json":
            output = version_list or []
        else:
            if not columns:
                columns = [
                    ("artifactVersion", "Version"),
                    ("fileCount", "File Count"),
                    ("artifactSize", "File Size"),
                    ("artifactDateCreated", "Created Date"),
                ]
            output = self.generate_chart_list([version_list], self.config, columns, main_chart=main_chart)
        self.print_data(output, True)

    @staticmethod
    def generate_chart_list(gen, config, columns, main_chart=None):
        cols, disp = zip(*columns)
        yield list(disp)

        for page in gen or []:
            for chart in page or []:
                out = ChartOuput(chart, config, main_chart=main_chart)
                yield [getattr(out, col, None) for col in cols]

    def print_chart(self, chart):
        """Print information about a chart"""
        if self.config.format_type == "json":
            chart_dict = chart.toDict()
            self.print_data(GeneralWrapper.from_dict(chart_dict))
            return
        tbl = self.create_output(header=False)
        tbl.add_separator_line()
        tbl.set_title("Chart Information")
        tbl.add_label_line("Name", chart.name)
        tbl.add_label_line("Short Description", chart.shortDescription)
        tbl.add_label_line("Display Name", chart.displayName)
        team_name = str_(chart.teamName) if hasattr(chart, "teamName") else ""
        tbl.add_label_line("Team", str_(team_name))
        tbl.add_label_line("Publisher", str_(chart.publisher))
        tbl.add_label_line("Built By", str_(chart.builtBy))
        tbl.add_label_line("Labels", "")
        # pylint: disable=expression-not-assigned
        [tbl.add_label_line("", format_label(label)) for label in chart.labels or []]
        tbl.add_label_line("Logo", str_(chart.logo))
        tbl.add_label_line("Created Date", format_date(chart.createdDate))
        tbl.add_label_line("Updated Date", format_date(chart.updatedDate))
        tbl.add_label_line("Read Only", str_(chart.isReadOnly))
        tbl.add_label_line("Access Type", chart.accessType)
        tbl.add_label_line("Associated Products", chart.productNames)
        tbl.add_label_line("Latest Version ID", str_(chart.latestVersionId))
        _size = str(chart.latestVersionSizeInBytes or "")
        if chart.latestVersionId and not _size:
            _size = 0
        tbl.add_label_line("Latest Version Size (bytes)", _size)
        # Note: script level overview attribute is stored in description in the schema.
        # UI diverged and we need to quickly match them now.
        tbl.add_label_line("Overview", "")
        if chart.description:
            chart.description = str(chart.description)
            # pylint: disable=expression-not-assigned
            [tbl.add_label_line("", line, level=1) for line in chart.description.splitlines()]
        tbl.add_separator_line()
        tbl.print()

    def print_chart_version(self, version, chart=None, file_list=None):
        """Print information about a chart version"""
        if self.config.format_type == "json":
            files_dict = [_file.toDict() for _file in file_list or []]
            chart_dict = GeneralWrapper(version=version.toDict(), file_list=files_dict)
            self.print_data(chart_dict)
        else:
            tbl = self.create_output(header=False)
            tbl.add_separator_line()
            tbl.set_title("Chart Version Information")
            # administrative info
            tbl.add_label_line("Created Date", format_date(version.createdDate))
            tbl.add_label_line("Updated Date", format_date(version.updatedDate))
            tbl.add_label_line("Version ID", str_(version.id))
            tbl.add_label_line("Total File Count", str_(version.totalFileCount))
            tbl.add_label_line("Total Size", human_size(version.totalSizeInBytes))
            tbl.add_label_line("Status", version.status)
            if chart:
                tbl.add_label_line("Access Type", chart.accessType)
                tbl.add_label_line("Associated Products", chart.productNames)
            if file_list:
                tbl.add_label_line("File List", "")
                for _file in file_list or []:
                    file_line = "{} - {}".format(_file.path, human_size(_file.sizeInBytes))
                    tbl.add_label_line("", file_line)
            tbl.add_separator_line()
            tbl.print()


class ChartOuput:
    def __init__(self, chart, config=None, main_chart=None):
        self.chart = chart
        self.config = config
        self.main_chart = main_chart

    def _resolve(self, att, to_string=True):
        val = getattr(self.main_chart, att) if self.main_chart else getattr(self.chart, att)
        if to_string:
            return str_(val)
        return val

    @property
    def artifactDateCreated(self):
        return self.dateCreated

    @property
    def artifactSize(self):
        return human_size(int(self.chart.totalSizeInBytes))

    @property
    def artifactVersion(self):
        return self.version

    @property
    def createdBy(self):
        cb = self.chart.createdByUser if hasattr(self.chart, "createdByUser") else self.chart.createdBy
        return cb or ""

    @property
    def dateCreated(self):
        dt = self.chart.createdDate if hasattr(self.chart, "createdDate") else self.chart.dateCreated
        return format_list_view_date(dt) or ""

    @property
    def dateModified(self):
        return format_list_view_date(self.chart.updatedDate) or ""

    @property
    def description(self):
        return self._resolve("description")

    @property
    def displayName(self):
        return self._resolve("displayName", to_string=False)

    @property
    def fileCount(self):
        return str_(self.chart.totalFileCount) or ""

    @property
    def isPublic(self):
        return self._resolve("isPublic") or "False"

    @property
    def labels(self):
        lbls = self._resolve("labels", to_string=False)
        if not lbls:
            return ""
        lbs = [lb["values"] for lb in lbls if lb["key"] == "general"]
        if not lbs:
            return ""
        lb = lbs[0]
        return ", ".join(lb)

    @property
    def name(self):
        return self._resolve("name")

    @property
    def orgName(self):
        return self._resolve("orgName")

    @property
    def repository(self):
        return format_repo(self.chart.orgName, self.chart.teamName, self.chart.name)

    @property
    def size(self):
        if self.main_chart:
            atts = self.main_chart.attributes or []
        else:
            atts = self.chart.attributes or []
        sz = [att.value for att in atts if att.key == "latestVersionSizeInBytes"]
        if not sz:
            sz = [getattr(self.chart, "totalSizeInBytes", "")]
        return human_size(int(sz[0])) if sz[0] else ""

    @property
    def teamName(self):
        return self._resolve("teamName")

    @property
    def version(self):
        if hasattr(self.chart, "id"):
            return self.chart.id or ""
        atts = self.chart.attributes or []
        version = [att.value for att in atts if att.key == "latestVersionIdStr"]
        return version[0] if version else ""

    @property
    def productNames(self):
        labels = self.chart.labels
        if not labels:
            return ""
        products = []
        for each in labels:
            if each["key"] == "productNames":
                products.extend(each["values"])
        return ", ".join(products)

    @property
    def accessType(self):
        return str_(self.chart.accessType) if hasattr(self.chart, "accessType") else ""
