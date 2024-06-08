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
    'GetContactFlowModuleResult',
    'AwaitableGetContactFlowModuleResult',
    'get_contact_flow_module',
    'get_contact_flow_module_output',
]

@pulumi.output_type
class GetContactFlowModuleResult:
    """
    A collection of values returned by getContactFlowModule.
    """
    def __init__(__self__, arn=None, contact_flow_module_id=None, content=None, description=None, id=None, instance_id=None, name=None, state=None, status=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if contact_flow_module_id and not isinstance(contact_flow_module_id, str):
            raise TypeError("Expected argument 'contact_flow_module_id' to be a str")
        pulumi.set(__self__, "contact_flow_module_id", contact_flow_module_id)
        if content and not isinstance(content, str):
            raise TypeError("Expected argument 'content' to be a str")
        pulumi.set(__self__, "content", content)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Contact Flow Module.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="contactFlowModuleId")
    def contact_flow_module_id(self) -> str:
        return pulumi.get(self, "contact_flow_module_id")

    @property
    @pulumi.getter
    def content(self) -> str:
        """
        Logic of the Contact Flow Module.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the Contact Flow Module.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> str:
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        Type of Contact Flow Module Module. Values are either `ACTIVE` or `ARCHIVED`.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Contact Flow Module Module. Values are either `PUBLISHED` or `SAVED`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags to assign to the Contact Flow Module.
        """
        return pulumi.get(self, "tags")


class AwaitableGetContactFlowModuleResult(GetContactFlowModuleResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetContactFlowModuleResult(
            arn=self.arn,
            contact_flow_module_id=self.contact_flow_module_id,
            content=self.content,
            description=self.description,
            id=self.id,
            instance_id=self.instance_id,
            name=self.name,
            state=self.state,
            status=self.status,
            tags=self.tags)


def get_contact_flow_module(contact_flow_module_id: Optional[str] = None,
                            instance_id: Optional[str] = None,
                            name: Optional[str] = None,
                            tags: Optional[Mapping[str, str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetContactFlowModuleResult:
    """
    Provides details about a specific Amazon Connect Contact Flow Module.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_contact_flow_module(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="example")
    ```

    By `contact_flow_module_id`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_contact_flow_module(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        contact_flow_module_id="cccccccc-bbbb-cccc-dddd-111111111111")
    ```


    :param str contact_flow_module_id: Returns information on a specific Contact Flow Module by contact flow module id
    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Contact Flow Module by name
    :param Mapping[str, str] tags: Map of tags to assign to the Contact Flow Module.
    """
    __args__ = dict()
    __args__['contactFlowModuleId'] = contact_flow_module_id
    __args__['instanceId'] = instance_id
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:connect/getContactFlowModule:getContactFlowModule', __args__, opts=opts, typ=GetContactFlowModuleResult).value

    return AwaitableGetContactFlowModuleResult(
        arn=pulumi.get(__ret__, 'arn'),
        contact_flow_module_id=pulumi.get(__ret__, 'contact_flow_module_id'),
        content=pulumi.get(__ret__, 'content'),
        description=pulumi.get(__ret__, 'description'),
        id=pulumi.get(__ret__, 'id'),
        instance_id=pulumi.get(__ret__, 'instance_id'),
        name=pulumi.get(__ret__, 'name'),
        state=pulumi.get(__ret__, 'state'),
        status=pulumi.get(__ret__, 'status'),
        tags=pulumi.get(__ret__, 'tags'))


@_utilities.lift_output_func(get_contact_flow_module)
def get_contact_flow_module_output(contact_flow_module_id: Optional[pulumi.Input[Optional[str]]] = None,
                                   instance_id: Optional[pulumi.Input[str]] = None,
                                   name: Optional[pulumi.Input[Optional[str]]] = None,
                                   tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                   opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetContactFlowModuleResult]:
    """
    Provides details about a specific Amazon Connect Contact Flow Module.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_contact_flow_module(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="example")
    ```

    By `contact_flow_module_id`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_contact_flow_module(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        contact_flow_module_id="cccccccc-bbbb-cccc-dddd-111111111111")
    ```


    :param str contact_flow_module_id: Returns information on a specific Contact Flow Module by contact flow module id
    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Contact Flow Module by name
    :param Mapping[str, str] tags: Map of tags to assign to the Contact Flow Module.
    """
    ...
