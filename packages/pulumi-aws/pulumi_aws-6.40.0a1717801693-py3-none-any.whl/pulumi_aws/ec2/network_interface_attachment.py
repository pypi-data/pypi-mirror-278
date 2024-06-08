# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NetworkInterfaceAttachmentInitArgs', 'NetworkInterfaceAttachment']

@pulumi.input_type
class NetworkInterfaceAttachmentInitArgs:
    def __init__(__self__, *,
                 device_index: pulumi.Input[int],
                 instance_id: pulumi.Input[str],
                 network_interface_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a NetworkInterfaceAttachment resource.
        :param pulumi.Input[int] device_index: Network interface index (int).
        :param pulumi.Input[str] instance_id: Instance ID to attach.
        :param pulumi.Input[str] network_interface_id: ENI ID to attach.
        """
        pulumi.set(__self__, "device_index", device_index)
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "network_interface_id", network_interface_id)

    @property
    @pulumi.getter(name="deviceIndex")
    def device_index(self) -> pulumi.Input[int]:
        """
        Network interface index (int).
        """
        return pulumi.get(self, "device_index")

    @device_index.setter
    def device_index(self, value: pulumi.Input[int]):
        pulumi.set(self, "device_index", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        Instance ID to attach.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Input[str]:
        """
        ENI ID to attach.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_interface_id", value)


@pulumi.input_type
class _NetworkInterfaceAttachmentState:
    def __init__(__self__, *,
                 attachment_id: Optional[pulumi.Input[str]] = None,
                 device_index: Optional[pulumi.Input[int]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkInterfaceAttachment resources.
        :param pulumi.Input[str] attachment_id: The ENI Attachment ID.
        :param pulumi.Input[int] device_index: Network interface index (int).
        :param pulumi.Input[str] instance_id: Instance ID to attach.
        :param pulumi.Input[str] network_interface_id: ENI ID to attach.
        :param pulumi.Input[str] status: The status of the Network Interface Attachment.
        """
        if attachment_id is not None:
            pulumi.set(__self__, "attachment_id", attachment_id)
        if device_index is not None:
            pulumi.set(__self__, "device_index", device_index)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="attachmentId")
    def attachment_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ENI Attachment ID.
        """
        return pulumi.get(self, "attachment_id")

    @attachment_id.setter
    def attachment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attachment_id", value)

    @property
    @pulumi.getter(name="deviceIndex")
    def device_index(self) -> Optional[pulumi.Input[int]]:
        """
        Network interface index (int).
        """
        return pulumi.get(self, "device_index")

    @device_index.setter
    def device_index(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "device_index", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        Instance ID to attach.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        ENI ID to attach.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_interface_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The status of the Network Interface Attachment.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class NetworkInterfaceAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_index: Optional[pulumi.Input[int]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attach an Elastic network interface (ENI) resource with EC2 instance.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ec2.NetworkInterfaceAttachment("test",
            instance_id=test_aws_instance["id"],
            network_interface_id=test_aws_network_interface["id"],
            device_index=0)
        ```

        ## Import

        Using `pulumi import`, import Elastic network interface (ENI) Attachments using its Attachment ID. For example:

        ```sh
        $ pulumi import aws:ec2/networkInterfaceAttachment:NetworkInterfaceAttachment secondary_nic eni-attach-0a33842b4ec347c4c
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] device_index: Network interface index (int).
        :param pulumi.Input[str] instance_id: Instance ID to attach.
        :param pulumi.Input[str] network_interface_id: ENI ID to attach.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkInterfaceAttachmentInitArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attach an Elastic network interface (ENI) resource with EC2 instance.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ec2.NetworkInterfaceAttachment("test",
            instance_id=test_aws_instance["id"],
            network_interface_id=test_aws_network_interface["id"],
            device_index=0)
        ```

        ## Import

        Using `pulumi import`, import Elastic network interface (ENI) Attachments using its Attachment ID. For example:

        ```sh
        $ pulumi import aws:ec2/networkInterfaceAttachment:NetworkInterfaceAttachment secondary_nic eni-attach-0a33842b4ec347c4c
        ```

        :param str resource_name: The name of the resource.
        :param NetworkInterfaceAttachmentInitArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkInterfaceAttachmentInitArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 device_index: Optional[pulumi.Input[int]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkInterfaceAttachmentInitArgs.__new__(NetworkInterfaceAttachmentInitArgs)

            if device_index is None and not opts.urn:
                raise TypeError("Missing required property 'device_index'")
            __props__.__dict__["device_index"] = device_index
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if network_interface_id is None and not opts.urn:
                raise TypeError("Missing required property 'network_interface_id'")
            __props__.__dict__["network_interface_id"] = network_interface_id
            __props__.__dict__["attachment_id"] = None
            __props__.__dict__["status"] = None
        super(NetworkInterfaceAttachment, __self__).__init__(
            'aws:ec2/networkInterfaceAttachment:NetworkInterfaceAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attachment_id: Optional[pulumi.Input[str]] = None,
            device_index: Optional[pulumi.Input[int]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            network_interface_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'NetworkInterfaceAttachment':
        """
        Get an existing NetworkInterfaceAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attachment_id: The ENI Attachment ID.
        :param pulumi.Input[int] device_index: Network interface index (int).
        :param pulumi.Input[str] instance_id: Instance ID to attach.
        :param pulumi.Input[str] network_interface_id: ENI ID to attach.
        :param pulumi.Input[str] status: The status of the Network Interface Attachment.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkInterfaceAttachmentState.__new__(_NetworkInterfaceAttachmentState)

        __props__.__dict__["attachment_id"] = attachment_id
        __props__.__dict__["device_index"] = device_index
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["network_interface_id"] = network_interface_id
        __props__.__dict__["status"] = status
        return NetworkInterfaceAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attachmentId")
    def attachment_id(self) -> pulumi.Output[str]:
        """
        The ENI Attachment ID.
        """
        return pulumi.get(self, "attachment_id")

    @property
    @pulumi.getter(name="deviceIndex")
    def device_index(self) -> pulumi.Output[int]:
        """
        Network interface index (int).
        """
        return pulumi.get(self, "device_index")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        Instance ID to attach.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[str]:
        """
        ENI ID to attach.
        """
        return pulumi.get(self, "network_interface_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Network Interface Attachment.
        """
        return pulumi.get(self, "status")

