# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetQueuesResult',
    'AwaitableGetQueuesResult',
    'get_queues',
    'get_queues_output',
]

@pulumi.output_type
class GetQueuesResult:
    """
    A collection of values returned by getQueues.
    """
    def __init__(__self__, id=None, queue_name_prefix=None, queue_urls=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if queue_name_prefix and not isinstance(queue_name_prefix, str):
            raise TypeError("Expected argument 'queue_name_prefix' to be a str")
        pulumi.set(__self__, "queue_name_prefix", queue_name_prefix)
        if queue_urls and not isinstance(queue_urls, list):
            raise TypeError("Expected argument 'queue_urls' to be a list")
        pulumi.set(__self__, "queue_urls", queue_urls)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="queueNamePrefix")
    def queue_name_prefix(self) -> Optional[str]:
        return pulumi.get(self, "queue_name_prefix")

    @property
    @pulumi.getter(name="queueUrls")
    def queue_urls(self) -> Sequence[str]:
        """
        A list of queue URLs.
        """
        return pulumi.get(self, "queue_urls")


class AwaitableGetQueuesResult(GetQueuesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetQueuesResult(
            id=self.id,
            queue_name_prefix=self.queue_name_prefix,
            queue_urls=self.queue_urls)


def get_queues(queue_name_prefix: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetQueuesResult:
    """
    Data source for managing an AWS SQS (Simple Queue) Queues.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.sqs.get_queues(queue_name_prefix="example")
    ```


    :param str queue_name_prefix: A string to use for filtering the list results. Only those queues whose name begins with the specified string are returned. Queue URLs and names are case-sensitive.
    """
    __args__ = dict()
    __args__['queueNamePrefix'] = queue_name_prefix
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:sqs/getQueues:getQueues', __args__, opts=opts, typ=GetQueuesResult).value

    return AwaitableGetQueuesResult(
        id=pulumi.get(__ret__, 'id'),
        queue_name_prefix=pulumi.get(__ret__, 'queue_name_prefix'),
        queue_urls=pulumi.get(__ret__, 'queue_urls'))


@_utilities.lift_output_func(get_queues)
def get_queues_output(queue_name_prefix: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetQueuesResult]:
    """
    Data source for managing an AWS SQS (Simple Queue) Queues.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.sqs.get_queues(queue_name_prefix="example")
    ```


    :param str queue_name_prefix: A string to use for filtering the list results. Only those queues whose name begins with the specified string are returned. Queue URLs and names are case-sensitive.
    """
    ...
