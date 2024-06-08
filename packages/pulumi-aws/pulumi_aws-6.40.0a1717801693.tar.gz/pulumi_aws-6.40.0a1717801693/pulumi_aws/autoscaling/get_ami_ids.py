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
    'GetAmiIdsResult',
    'AwaitableGetAmiIdsResult',
    'get_ami_ids',
    'get_ami_ids_output',
]

@pulumi.output_type
class GetAmiIdsResult:
    """
    A collection of values returned by getAmiIds.
    """
    def __init__(__self__, arns=None, filters=None, id=None, names=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        List of the Autoscaling Groups Arns in the current region.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAmiIdsFilterResult']]:
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
    def names(self) -> Sequence[str]:
        """
        List of the Autoscaling Groups in the current region.
        """
        return pulumi.get(self, "names")


class AwaitableGetAmiIdsResult(GetAmiIdsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAmiIdsResult(
            arns=self.arns,
            filters=self.filters,
            id=self.id,
            names=self.names)


def get_ami_ids(filters: Optional[Sequence[pulumi.InputType['GetAmiIdsFilterArgs']]] = None,
                names: Optional[Sequence[str]] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAmiIdsResult:
    """
    The Autoscaling Groups data source allows access to the list of AWS
    ASGs within a specific region. This will allow you to pass a list of AutoScaling Groups to other resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    groups = aws.autoscaling.get_ami_ids(filters=[
        aws.autoscaling.GetAmiIdsFilterArgs(
            name="tag:Team",
            values=["Pets"],
        ),
        aws.autoscaling.GetAmiIdsFilterArgs(
            name="tag-key",
            values=["Environment"],
        ),
    ])
    slack_notifications = aws.autoscaling.Notification("slack_notifications",
        group_names=groups.names,
        notifications=[
            "autoscaling:EC2_INSTANCE_LAUNCH",
            "autoscaling:EC2_INSTANCE_TERMINATE",
            "autoscaling:EC2_INSTANCE_LAUNCH_ERROR",
            "autoscaling:EC2_INSTANCE_TERMINATE_ERROR",
        ],
        topic_arn="TOPIC ARN")
    ```


    :param Sequence[pulumi.InputType['GetAmiIdsFilterArgs']] filters: Filter used to scope the list e.g., by tags. See [related docs](http://docs.aws.amazon.com/AutoScaling/latest/APIReference/API_Filter.html).
    :param Sequence[str] names: List of autoscaling group names
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['names'] = names
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:autoscaling/getAmiIds:getAmiIds', __args__, opts=opts, typ=GetAmiIdsResult).value

    return AwaitableGetAmiIdsResult(
        arns=pulumi.get(__ret__, 'arns'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        names=pulumi.get(__ret__, 'names'))


@_utilities.lift_output_func(get_ami_ids)
def get_ami_ids_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAmiIdsFilterArgs']]]]] = None,
                       names: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAmiIdsResult]:
    """
    The Autoscaling Groups data source allows access to the list of AWS
    ASGs within a specific region. This will allow you to pass a list of AutoScaling Groups to other resources.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    groups = aws.autoscaling.get_ami_ids(filters=[
        aws.autoscaling.GetAmiIdsFilterArgs(
            name="tag:Team",
            values=["Pets"],
        ),
        aws.autoscaling.GetAmiIdsFilterArgs(
            name="tag-key",
            values=["Environment"],
        ),
    ])
    slack_notifications = aws.autoscaling.Notification("slack_notifications",
        group_names=groups.names,
        notifications=[
            "autoscaling:EC2_INSTANCE_LAUNCH",
            "autoscaling:EC2_INSTANCE_TERMINATE",
            "autoscaling:EC2_INSTANCE_LAUNCH_ERROR",
            "autoscaling:EC2_INSTANCE_TERMINATE_ERROR",
        ],
        topic_arn="TOPIC ARN")
    ```


    :param Sequence[pulumi.InputType['GetAmiIdsFilterArgs']] filters: Filter used to scope the list e.g., by tags. See [related docs](http://docs.aws.amazon.com/AutoScaling/latest/APIReference/API_Filter.html).
    :param Sequence[str] names: List of autoscaling group names
    """
    ...
