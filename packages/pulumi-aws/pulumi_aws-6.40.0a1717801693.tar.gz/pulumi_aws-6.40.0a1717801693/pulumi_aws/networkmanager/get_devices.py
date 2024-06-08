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
    'GetDevicesResult',
    'AwaitableGetDevicesResult',
    'get_devices',
    'get_devices_output',
]

@pulumi.output_type
class GetDevicesResult:
    """
    A collection of values returned by getDevices.
    """
    def __init__(__self__, global_network_id=None, id=None, ids=None, site_id=None, tags=None):
        if global_network_id and not isinstance(global_network_id, str):
            raise TypeError("Expected argument 'global_network_id' to be a str")
        pulumi.set(__self__, "global_network_id", global_network_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if site_id and not isinstance(site_id, str):
            raise TypeError("Expected argument 'site_id' to be a str")
        pulumi.set(__self__, "site_id", site_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="globalNetworkId")
    def global_network_id(self) -> str:
        return pulumi.get(self, "global_network_id")

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
        IDs of the devices.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="siteId")
    def site_id(self) -> Optional[str]:
        return pulumi.get(self, "site_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "tags")


class AwaitableGetDevicesResult(GetDevicesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDevicesResult(
            global_network_id=self.global_network_id,
            id=self.id,
            ids=self.ids,
            site_id=self.site_id,
            tags=self.tags)


def get_devices(global_network_id: Optional[str] = None,
                site_id: Optional[str] = None,
                tags: Optional[Mapping[str, str]] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDevicesResult:
    """
    Retrieve information about devices.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkmanager.get_devices(global_network_id=global_network_id,
        tags={
            "Env": "test",
        })
    ```


    :param str global_network_id: ID of the Global Network of the devices to retrieve.
    :param str site_id: ID of the site of the devices to retrieve.
    :param Mapping[str, str] tags: Restricts the list to the devices with these tags.
    """
    __args__ = dict()
    __args__['globalNetworkId'] = global_network_id
    __args__['siteId'] = site_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:networkmanager/getDevices:getDevices', __args__, opts=opts, typ=GetDevicesResult).value

    return AwaitableGetDevicesResult(
        global_network_id=pulumi.get(__ret__, 'global_network_id'),
        id=pulumi.get(__ret__, 'id'),
        ids=pulumi.get(__ret__, 'ids'),
        site_id=pulumi.get(__ret__, 'site_id'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_devices)
def get_devices_output(global_network_id: Optional[pulumi.Input[str]] = None,
                       site_id: Optional[pulumi.Input[Optional[str]]] = None,
                       tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDevicesResult]:
    """
    Retrieve information about devices.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.networkmanager.get_devices(global_network_id=global_network_id,
        tags={
            "Env": "test",
        })
    ```


    :param str global_network_id: ID of the Global Network of the devices to retrieve.
    :param str site_id: ID of the site of the devices to retrieve.
    :param Mapping[str, str] tags: Restricts the list to the devices with these tags.
    """
    ...
