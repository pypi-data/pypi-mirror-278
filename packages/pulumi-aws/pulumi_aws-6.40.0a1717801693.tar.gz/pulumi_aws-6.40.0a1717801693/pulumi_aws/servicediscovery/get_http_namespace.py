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
    'GetHttpNamespaceResult',
    'AwaitableGetHttpNamespaceResult',
    'get_http_namespace',
    'get_http_namespace_output',
]

@pulumi.output_type
class GetHttpNamespaceResult:
    """
    A collection of values returned by getHttpNamespace.
    """
    def __init__(__self__, arn=None, description=None, http_name=None, id=None, name=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if http_name and not isinstance(http_name, str):
            raise TypeError("Expected argument 'http_name' to be a str")
        pulumi.set(__self__, "http_name", http_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN that Amazon Route 53 assigns to the namespace when you create it.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description that you specify for the namespace when you create it.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="httpName")
    def http_name(self) -> str:
        """
        Name of an HTTP namespace.
        """
        return pulumi.get(self, "http_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags for the resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetHttpNamespaceResult(GetHttpNamespaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHttpNamespaceResult(
            arn=self.arn,
            description=self.description,
            http_name=self.http_name,
            id=self.id,
            name=self.name,
            tags=self.tags)


def get_http_namespace(name: Optional[str] = None,
                       tags: Optional[Mapping[str, str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHttpNamespaceResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicediscovery.get_http_namespace(name="development")
    ```


    :param str name: Name of the http namespace.
    :param Mapping[str, str] tags: Map of tags for the resource.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:servicediscovery/getHttpNamespace:getHttpNamespace', __args__, opts=opts, typ=GetHttpNamespaceResult).value

    return AwaitableGetHttpNamespaceResult(
        arn=pulumi.get(__ret__, 'arn'),
        description=pulumi.get(__ret__, 'description'),
        http_name=pulumi.get(__ret__, 'http_name'),
        id=pulumi.get(__ret__, 'id'),
        name=pulumi.get(__ret__, 'name'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_http_namespace)
def get_http_namespace_output(name: Optional[pulumi.Input[str]] = None,
                              tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHttpNamespaceResult]:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicediscovery.get_http_namespace(name="development")
    ```


    :param str name: Name of the http namespace.
    :param Mapping[str, str] tags: Map of tags for the resource.
    """
    ...
