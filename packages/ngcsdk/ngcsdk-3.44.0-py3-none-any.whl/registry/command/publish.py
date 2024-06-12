#
# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from ngcbpc.data.registry.AccessTypeEnum import AccessTypeEnum
from ngcbpc.errors import InvalidArgumentError
from registry.data.publishing.Artifact import Artifact
from registry.data.publishing.PublishingRequest import PublishingRequest

METADATA_HELP = "Only perform a shallow copy of the metadata instead of a deep copy of the objects referenced"
VERSION_ONLY_HELP = "Only copy the specified version of the object without copying any metadata"
ALLOW_GUEST_HELP = "Allow anonymous users to download the published object"
DISCOVERABLE_HELP = "Allow the published object to be discoverable in searches"
PUBLIC_HELP = "Allow access to the published object by everyone instead of just those with specific roles"
PRODUCT_HELP = "Publish the object under a Product. Choose from: "
ACCESS_TYPE_HELP = f"Publish the object with a specific access type. Choose from: {', '.join(AccessTypeEnum)}"
PUBTYPE_MAPPING = {
    "models": "MODEL",
    "helm-charts": "HELM_CHART",
    "resources": "RESOURCE",
    "collections": "COLLECTION",
}
VISIBILITY_HELP = "Only change the visibility qualities of the target. Metadata and version files are not affected."


class Publisher:
    def __init__(self, source_artifact, target_artifact, publish_api, artifact_type, args):
        self.source_registry_target = source_artifact
        self.target_registry_target = target_artifact
        self.publish_api = publish_api
        self.artifact_type = artifact_type
        self.metadata_only = args.metadata_only
        self.version_only = args.version_only
        self.visibility_only = args.visibility_only
        self.public = args.public
        self.allow_guest = args.allow_guest
        self.discoverable = args.discoverable
        self.product_name = args.product_name if hasattr(args, "product_name") else None
        self.access_type = args.access_type if hasattr(args, "access_type") else None
        # This will only be present for images.
        self.sign = getattr(args, "sign", False)
        self._validate_settings()

    def _validate_settings(self):
        if self.discoverable:
            if not (self.allow_guest or self.public):
                raise InvalidArgumentError(
                    "discoverable",
                    "An item cannot be published as 'discoverable' unless either 'public' or 'allow_guest' is True",
                )
        mutex_args = [val for val in (self.metadata_only, self.version_only, self.visibility_only) if val]
        if len(mutex_args) > 1:
            args = [arg for arg in ("metadata_only", "version_only", "visibility_only") if getattr(self, arg)]
            raise InvalidArgumentError(
                ", ".join(args),
                "Cannot specify more than one of 'metadata_only', 'version_only', or 'visibility_only'  "
                "in the same publishing request",
            )
        if self.version_only and self.artifact_type == "collections":
            raise NotImplementedError("version_only option for collections is not yet implemented.")

    def publish(self):
        request = PublishingRequest()
        request.isNew = False
        request.artifactType = PUBTYPE_MAPPING.get(self.artifact_type, "")
        version_name = "version"
        request.publishToPublic = self.public
        request.publishWithGuestAccess = self.allow_guest
        request.publishAsListedToPublic = self.discoverable
        request.sign = self.sign
        if self.product_name and self.access_type:
            request.accessType = self.access_type
            request.productNames = self.product_name

        rsa = request.sourceArtifact = Artifact()
        srt = self.source_registry_target
        rsa.org = srt.org
        rsa.team = srt.team
        rsa.name = srt.name
        if hasattr(srt, version_name):
            rsa.version = getattr(srt, version_name)

        rta = request.targetArtifact = Artifact()
        trt = self.target_registry_target
        rta.org = trt.org
        rta.team = trt.team
        rta.name = trt.name
        if hasattr(trt, version_name):
            rta.version = getattr(trt, version_name)

        # Collections and images have their own methods; the rest use the artifact method.
        if self.metadata_only:
            return self.publish_api.copy_metadata_artifact(request, self.artifact_type)
        if self.version_only:
            return self.publish_api.copy_version_artifact(request, self.artifact_type)
        if self.visibility_only:
            return self.publish_api.update_visibility(request, self.artifact_type)
        mthd_name = {"collections": "publish_collection"}.get(self.artifact_type, "publish_artifact")
        mthd = getattr(self.publish_api, mthd_name)
        return mthd(request, self.artifact_type)
