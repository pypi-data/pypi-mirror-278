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

__all__ = [
    'GetInputResult',
    'AwaitableGetInputResult',
    'get_input',
    'get_input_output',
]

@pulumi.output_type
class GetInputResult:
    """
    A collection of values returned by getInput.
    """
    def __init__(__self__, arn=None, attached_channels=None, destinations=None, id=None, input_class=None, input_devices=None, input_partner_ids=None, input_source_type=None, media_connect_flows=None, name=None, role_arn=None, security_groups=None, sources=None, state=None, tags=None, type=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if attached_channels and not isinstance(attached_channels, list):
            raise TypeError("Expected argument 'attached_channels' to be a list")
        pulumi.set(__self__, "attached_channels", attached_channels)
        if destinations and not isinstance(destinations, list):
            raise TypeError("Expected argument 'destinations' to be a list")
        pulumi.set(__self__, "destinations", destinations)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if input_class and not isinstance(input_class, str):
            raise TypeError("Expected argument 'input_class' to be a str")
        pulumi.set(__self__, "input_class", input_class)
        if input_devices and not isinstance(input_devices, list):
            raise TypeError("Expected argument 'input_devices' to be a list")
        pulumi.set(__self__, "input_devices", input_devices)
        if input_partner_ids and not isinstance(input_partner_ids, list):
            raise TypeError("Expected argument 'input_partner_ids' to be a list")
        pulumi.set(__self__, "input_partner_ids", input_partner_ids)
        if input_source_type and not isinstance(input_source_type, str):
            raise TypeError("Expected argument 'input_source_type' to be a str")
        pulumi.set(__self__, "input_source_type", input_source_type)
        if media_connect_flows and not isinstance(media_connect_flows, list):
            raise TypeError("Expected argument 'media_connect_flows' to be a list")
        pulumi.set(__self__, "media_connect_flows", media_connect_flows)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if role_arn and not isinstance(role_arn, str):
            raise TypeError("Expected argument 'role_arn' to be a str")
        pulumi.set(__self__, "role_arn", role_arn)
        if security_groups and not isinstance(security_groups, list):
            raise TypeError("Expected argument 'security_groups' to be a list")
        pulumi.set(__self__, "security_groups", security_groups)
        if sources and not isinstance(sources, list):
            raise TypeError("Expected argument 'sources' to be a list")
        pulumi.set(__self__, "sources", sources)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Input.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="attachedChannels")
    def attached_channels(self) -> Sequence[str]:
        """
        Channels attached to Input.
        """
        return pulumi.get(self, "attached_channels")

    @property
    @pulumi.getter
    def destinations(self) -> Sequence['outputs.GetInputDestinationResult']:
        return pulumi.get(self, "destinations")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="inputClass")
    def input_class(self) -> str:
        """
        The input class.
        """
        return pulumi.get(self, "input_class")

    @property
    @pulumi.getter(name="inputDevices")
    def input_devices(self) -> Sequence['outputs.GetInputInputDeviceResult']:
        """
        Settings for the devices.
        """
        return pulumi.get(self, "input_devices")

    @property
    @pulumi.getter(name="inputPartnerIds")
    def input_partner_ids(self) -> Sequence[str]:
        """
        A list of IDs for all Inputs which are partners of this one.
        """
        return pulumi.get(self, "input_partner_ids")

    @property
    @pulumi.getter(name="inputSourceType")
    def input_source_type(self) -> str:
        """
        Source type of the input.
        """
        return pulumi.get(self, "input_source_type")

    @property
    @pulumi.getter(name="mediaConnectFlows")
    def media_connect_flows(self) -> Sequence['outputs.GetInputMediaConnectFlowResult']:
        """
        A list of the MediaConnect Flows.
        """
        return pulumi.get(self, "media_connect_flows")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the input.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> str:
        """
        The ARN of the role this input assumes during and after creation.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> Sequence[str]:
        """
        List of input security groups.
        """
        return pulumi.get(self, "security_groups")

    @property
    @pulumi.getter
    def sources(self) -> Sequence['outputs.GetInputSourceResult']:
        """
        The source URLs for a PULL-type input.
        """
        return pulumi.get(self, "sources")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        The state of the input.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A map of tags assigned to the Input.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the input.
        """
        return pulumi.get(self, "type")


class AwaitableGetInputResult(GetInputResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetInputResult(
            arn=self.arn,
            attached_channels=self.attached_channels,
            destinations=self.destinations,
            id=self.id,
            input_class=self.input_class,
            input_devices=self.input_devices,
            input_partner_ids=self.input_partner_ids,
            input_source_type=self.input_source_type,
            media_connect_flows=self.media_connect_flows,
            name=self.name,
            role_arn=self.role_arn,
            security_groups=self.security_groups,
            sources=self.sources,
            state=self.state,
            tags=self.tags,
            type=self.type)


def get_input(id: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetInputResult:
    """
    Data source for managing an AWS Elemental MediaLive Input.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.medialive.get_input(id=example_aws_medialive_input["id"])
    ```


    :param str id: The ID of the Input.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:medialive/getInput:getInput', __args__, opts=opts, typ=GetInputResult).value

    return AwaitableGetInputResult(
        arn=pulumi.get(__ret__, 'arn'),
        attached_channels=pulumi.get(__ret__, 'attached_channels'),
        destinations=pulumi.get(__ret__, 'destinations'),
        id=pulumi.get(__ret__, 'id'),
        input_class=pulumi.get(__ret__, 'input_class'),
        input_devices=pulumi.get(__ret__, 'input_devices'),
        input_partner_ids=pulumi.get(__ret__, 'input_partner_ids'),
        input_source_type=pulumi.get(__ret__, 'input_source_type'),
        media_connect_flows=pulumi.get(__ret__, 'media_connect_flows'),
        name=pulumi.get(__ret__, 'name'),
        role_arn=pulumi.get(__ret__, 'role_arn'),
        security_groups=pulumi.get(__ret__, 'security_groups'),
        sources=pulumi.get(__ret__, 'sources'),
        state=pulumi.get(__ret__, 'state'),
        tags=pulumi.get(__ret__, 'tags'),
        type=pulumi.get(__ret__, 'type'))


@_utilities.lift_output_func(get_input)
def get_input_output(id: Optional[pulumi.Input[str]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetInputResult]:
    """
    Data source for managing an AWS Elemental MediaLive Input.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.medialive.get_input(id=example_aws_medialive_input["id"])
    ```


    :param str id: The ID of the Input.
    """
    ...
