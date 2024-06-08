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
    'GetVpnGatewayResult',
    'AwaitableGetVpnGatewayResult',
    'get_vpn_gateway',
    'get_vpn_gateway_output',
]

@pulumi.output_type
class GetVpnGatewayResult:
    """
    A collection of values returned by getVpnGateway.
    """
    def __init__(__self__, amazon_side_asn=None, arn=None, attached_vpc_id=None, availability_zone=None, filters=None, id=None, state=None, tags=None):
        if amazon_side_asn and not isinstance(amazon_side_asn, str):
            raise TypeError("Expected argument 'amazon_side_asn' to be a str")
        pulumi.set(__self__, "amazon_side_asn", amazon_side_asn)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if attached_vpc_id and not isinstance(attached_vpc_id, str):
            raise TypeError("Expected argument 'attached_vpc_id' to be a str")
        pulumi.set(__self__, "attached_vpc_id", attached_vpc_id)
        if availability_zone and not isinstance(availability_zone, str):
            raise TypeError("Expected argument 'availability_zone' to be a str")
        pulumi.set(__self__, "availability_zone", availability_zone)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="amazonSideAsn")
    def amazon_side_asn(self) -> str:
        return pulumi.get(self, "amazon_side_asn")

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="attachedVpcId")
    def attached_vpc_id(self) -> str:
        return pulumi.get(self, "attached_vpc_id")

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> str:
        return pulumi.get(self, "availability_zone")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetVpnGatewayFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def state(self) -> str:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetVpnGatewayResult(GetVpnGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpnGatewayResult(
            amazon_side_asn=self.amazon_side_asn,
            arn=self.arn,
            attached_vpc_id=self.attached_vpc_id,
            availability_zone=self.availability_zone,
            filters=self.filters,
            id=self.id,
            state=self.state,
            tags=self.tags)


def get_vpn_gateway(amazon_side_asn: Optional[str] = None,
                    attached_vpc_id: Optional[str] = None,
                    availability_zone: Optional[str] = None,
                    filters: Optional[Sequence[pulumi.InputType['GetVpnGatewayFilterArgs']]] = None,
                    id: Optional[str] = None,
                    state: Optional[str] = None,
                    tags: Optional[Mapping[str, str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpnGatewayResult:
    """
    The VPN Gateway data source provides details about
    a specific VPN gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.ec2.get_vpn_gateway(filters=[aws.ec2.GetVpnGatewayFilterArgs(
        name="tag:Name",
        values=["vpn-gw"],
    )])
    pulumi.export("vpnGatewayId", selected.id)
    ```


    :param str amazon_side_asn: Autonomous System Number (ASN) for the Amazon side of the specific VPN Gateway to retrieve.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    :param str attached_vpc_id: ID of a VPC attached to the specific VPN Gateway to retrieve.
    :param str availability_zone: Availability Zone of the specific VPN Gateway to retrieve.
    :param Sequence[pulumi.InputType['GetVpnGatewayFilterArgs']] filters: Custom filter block as described below.
    :param str id: ID of the specific VPN Gateway to retrieve.
    :param str state: State of the specific VPN Gateway to retrieve.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired VPN Gateway.
    """
    __args__ = dict()
    __args__['amazonSideAsn'] = amazon_side_asn
    __args__['attachedVpcId'] = attached_vpc_id
    __args__['availabilityZone'] = availability_zone
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['state'] = state
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getVpnGateway:getVpnGateway', __args__, opts=opts, typ=GetVpnGatewayResult).value

    return AwaitableGetVpnGatewayResult(
        amazon_side_asn=pulumi.get(__ret__, 'amazon_side_asn'),
        arn=pulumi.get(__ret__, 'arn'),
        attached_vpc_id=pulumi.get(__ret__, 'attached_vpc_id'),
        availability_zone=pulumi.get(__ret__, 'availability_zone'),
        filters=pulumi.get(__ret__, 'filters'),
        id=pulumi.get(__ret__, 'id'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_vpn_gateway)
def get_vpn_gateway_output(amazon_side_asn: Optional[pulumi.Input[Optional[str]]] = None,
                           attached_vpc_id: Optional[pulumi.Input[Optional[str]]] = None,
                           availability_zone: Optional[pulumi.Input[Optional[str]]] = None,
                           filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetVpnGatewayFilterArgs']]]]] = None,
                           id: Optional[pulumi.Input[Optional[str]]] = None,
                           state: Optional[pulumi.Input[Optional[str]]] = None,
                           tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpnGatewayResult]:
    """
    The VPN Gateway data source provides details about
    a specific VPN gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.ec2.get_vpn_gateway(filters=[aws.ec2.GetVpnGatewayFilterArgs(
        name="tag:Name",
        values=["vpn-gw"],
    )])
    pulumi.export("vpnGatewayId", selected.id)
    ```


    :param str amazon_side_asn: Autonomous System Number (ASN) for the Amazon side of the specific VPN Gateway to retrieve.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    :param str attached_vpc_id: ID of a VPC attached to the specific VPN Gateway to retrieve.
    :param str availability_zone: Availability Zone of the specific VPN Gateway to retrieve.
    :param Sequence[pulumi.InputType['GetVpnGatewayFilterArgs']] filters: Custom filter block as described below.
    :param str id: ID of the specific VPN Gateway to retrieve.
    :param str state: State of the specific VPN Gateway to retrieve.
    :param Mapping[str, str] tags: Map of tags, each pair of which must exactly match
           a pair on the desired VPN Gateway.
    """
    ...
