# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetEbsVolumesResult',
    'AwaitableGetEbsVolumesResult',
    'get_ebs_volumes',
    'get_ebs_volumes_output',
]

@pulumi.output_type
class GetEbsVolumesResult:
    """
    A collection of values returned by getEbsVolumes.
    """
    def __init__(__self__, filters=None, id=None, ids=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetEbsVolumesFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        Set of all the EBS Volume IDs found. This data source will fail if
        no volumes match the provided criteria.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "tags")


class AwaitableGetEbsVolumesResult(GetEbsVolumesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEbsVolumesResult(
            filters=self.filters,
            id=self.id,
            ids=self.ids,
            tags=self.tags)


def get_ebs_volumes(filters: Optional[Sequence[pulumi.InputType['GetEbsVolumesFilterArgs']]] = None,
                    tags: Optional[Mapping[str, str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEbsVolumesResult:
    """
    `ebs_get_ebs_volumes` provides identifying information for EBS volumes matching given criteria.

    This data source can be useful for getting a list of volume IDs with (for example) matching tags.

    ## Example Usage

    The following demonstrates obtaining a map of availability zone to EBS volume ID for volumes with a given tag value.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ebs.get_ebs_volumes(tags={
        "VolumeSet": "TestVolumeSet",
    })
    example_get_volume = {__key: aws.ebs.get_volume(filters=[aws.ebs.GetVolumeFilterArgs(
        name="volume-id",
        values=[__value],
    )]) for __key, __value in example.ids}
    pulumi.export("availabilityZoneToVolumeId", {s.id: s.availability_zone for s in example_get_volume})
    ```


    :param Sequence[pulumi.InputType['GetEbsVolumesFilterArgs']] filters: Custom filter block as described below.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired volumes.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ebs/getEbsVolumes:getEbsVolumes', __args__, opts=opts, typ=GetEbsVolumesResult).value

    return AwaitableGetEbsVolumesResult(
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_ebs_volumes)
def get_ebs_volumes_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetEbsVolumesFilterArgs']]]]] = None,
                           tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetEbsVolumesResult]:
    """
    `ebs_get_ebs_volumes` provides identifying information for EBS volumes matching given criteria.

    This data source can be useful for getting a list of volume IDs with (for example) matching tags.

    ## Example Usage

    The following demonstrates obtaining a map of availability zone to EBS volume ID for volumes with a given tag value.

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ebs.get_ebs_volumes(tags={
        "VolumeSet": "TestVolumeSet",
    })
    example_get_volume = {__key: aws.ebs.get_volume(filters=[aws.ebs.GetVolumeFilterArgs(
        name="volume-id",
        values=[__value],
    )]) for __key, __value in example.ids}
    pulumi.export("availabilityZoneToVolumeId", {s.id: s.availability_zone for s in example_get_volume})
    ```


    :param Sequence[pulumi.InputType['GetEbsVolumesFilterArgs']] filters: Custom filter block as described below.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired volumes.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    ...
