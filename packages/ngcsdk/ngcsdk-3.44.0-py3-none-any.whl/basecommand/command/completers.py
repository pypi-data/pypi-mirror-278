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
from basecommand.constants import WORKSPACE_LIST_PAGE_SIZE
from ngcbpc.api.configuration import Configuration
from ngcbpc.command.completers import NGCCompleter
from ngccli.modules.client import Client

# TODO make this faster
config = Configuration()
job_id_completer = NGCCompleter(
    lambda: [
        str(elem.id)
        for elem in Client().basecommand.jobs.get_jobs(config.org_name, user_id=Client().users.user_who().user.id)
    ]
)  # noqa: E501
dataset_id_completer = NGCCompleter(
    lambda: [str(elem.id) for elem in Client().basecommand.dataset.list_dataset(config.org_name)]
)

workspace_id_completer = NGCCompleter(
    lambda: [
        elem.id
        for elem in Client().basecommand.workspace.list_workspace(
            org_name=config.org_name,
            team_name=config.team_name,
            ace_name=config.ace_name,
            exclude_shared=False,
            page_size=WORKSPACE_LIST_PAGE_SIZE,
        )
    ]
)
