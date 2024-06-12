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
from typing import Optional, Type, TypeVar

from ngcbpc.errors import NgcException

T = TypeVar("T", bound="DeploymentSpecification")


class DeploymentSpecification:
    """This class represents a deployment specification for NVCF"""

    @classmethod
    def from_str(cls: Type[T], in_str: str) -> T:
        """Assumes a colon separated string of the form
        backend:gpu:instanceType:minInstances:maxInstances"""
        values = in_str.split(":")
        backend = values[0]
        gpu = values[1]
        instance_type = values[2]
        min_instances = int(values[3])
        max_instances = int(values[4])
        return cls(
            backend=backend,
            gpu=gpu,
            instance_type=instance_type,
            min_instances=min_instances,
            max_instances=max_instances,
        )

    @classmethod
    def from_dict(cls: Type[T], in_dict: dict) -> T:
        backend = in_dict["backend"]
        gpu = in_dict["gpu"]
        min_instances = int(in_dict["minInstances"])
        max_instances = int(in_dict["maxInstances"])
        instance_type = in_dict.get("instanceType", None)
        availability_zones = in_dict.get("availabilityZones", None)
        max_request_concurrency = in_dict.get("maxRequestConcurrency", None)
        configuration = in_dict.get("configuration", None)
        return cls(
            gpu=gpu,
            backend=backend,
            max_instances=max_instances,
            min_instances=min_instances,
            instance_type=instance_type,
            availability_zones=availability_zones,
            max_request_concurrency=max_request_concurrency,
            configuration=configuration,
        )

    def __init__(
        self,
        backend: str,
        gpu: str,
        min_instances: int,
        max_instances: int,
        instance_type: Optional[str] = None,
        availability_zones: Optional[list[str]] = None,
        max_request_concurrency: Optional[int] = None,
        configuration: Optional[dict] = None,
    ):
        """
        Matches the deployment specification object.
        """
        self.gpu = gpu
        self.backend = backend
        self.minInstances = min_instances
        self.maxInstances = max_instances
        self.instanceType = instance_type
        self.availabilityZones = availability_zones
        self.maxRequestConcurrency = max_request_concurrency
        self.configuration = configuration

        if self.minInstances <= 0:
            raise NgcException("MinimumInstances cannot be negative")

        if self.maxInstances < self.minInstances:
            raise NgcException("Max Instances must be more than or equal to MinimumInstances")


class GPUObject:
    def __init__(self, name, instances, backend):
        self.name = name
        self.instances = instances
        self.backend = backend


def get_available_gpus_from_cluster_groups(cluster_groups: list) -> list[GPUObject]:
    """Returns a list of GPUs from the cluster_groups endpoint"""
    gpus = []
    for cluster_group in cluster_groups:
        backend = cluster_group.get("name")
        for gpu in cluster_group.get("gpus", []):
            gpu_name = gpu.get("name")
            instance_types = gpu.get("instanceTypes", [])
            instance_names = [instance_type.get("name") for instance_type in instance_types]
            gpus.append(GPUObject(gpu_name, instance_names, backend))
    return gpus
