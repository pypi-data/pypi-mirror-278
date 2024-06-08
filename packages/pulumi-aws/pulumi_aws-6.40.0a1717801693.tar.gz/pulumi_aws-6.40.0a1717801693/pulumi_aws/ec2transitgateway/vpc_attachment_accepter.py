# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VpcAttachmentAccepterArgs', 'VpcAttachmentAccepter']

@pulumi.input_type
class VpcAttachmentAccepterArgs:
    def __init__(__self__, *,
                 transit_gateway_attachment_id: pulumi.Input[str],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transit_gateway_default_route_table_association: Optional[pulumi.Input[bool]] = None,
                 transit_gateway_default_route_table_propagation: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a VpcAttachmentAccepter resource.
        :param pulumi.Input[str] transit_gateway_attachment_id: The ID of the EC2 Transit Gateway Attachment to manage.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value tags for the EC2 Transit Gateway VPC Attachment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[bool] transit_gateway_default_route_table_association: Boolean whether the VPC Attachment should be associated with the EC2 Transit Gateway association default route table. Default value: `true`.
        :param pulumi.Input[bool] transit_gateway_default_route_table_propagation: Boolean whether the VPC Attachment should propagate routes with the EC2 Transit Gateway propagation default route table. Default value: `true`.
        """
        pulumi.set(__self__, "transit_gateway_attachment_id", transit_gateway_attachment_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if transit_gateway_default_route_table_association is not None:
            pulumi.set(__self__, "transit_gateway_default_route_table_association", transit_gateway_default_route_table_association)
        if transit_gateway_default_route_table_propagation is not None:
            pulumi.set(__self__, "transit_gateway_default_route_table_propagation", transit_gateway_default_route_table_propagation)

    @property
    @pulumi.getter(name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> pulumi.Input[str]:
        """
        The ID of the EC2 Transit Gateway Attachment to manage.
        """
        return pulumi.get(self, "transit_gateway_attachment_id")

    @transit_gateway_attachment_id.setter
    def transit_gateway_attachment_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "transit_gateway_attachment_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value tags for the EC2 Transit Gateway VPC Attachment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="transitGatewayDefaultRouteTableAssociation")
    def transit_gateway_default_route_table_association(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean whether the VPC Attachment should be associated with the EC2 Transit Gateway association default route table. Default value: `true`.
        """
        return pulumi.get(self, "transit_gateway_default_route_table_association")

    @transit_gateway_default_route_table_association.setter
    def transit_gateway_default_route_table_association(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "transit_gateway_default_route_table_association", value)

    @property
    @pulumi.getter(name="transitGatewayDefaultRouteTablePropagation")
    def transit_gateway_default_route_table_propagation(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean whether the VPC Attachment should propagate routes with the EC2 Transit Gateway propagation default route table. Default value: `true`.
        """
        return pulumi.get(self, "transit_gateway_default_route_table_propagation")

    @transit_gateway_default_route_table_propagation.setter
    def transit_gateway_default_route_table_propagation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "transit_gateway_default_route_table_propagation", value)


@pulumi.input_type
class _VpcAttachmentAccepterState:
    def __init__(__self__, *,
                 appliance_mode_support: Optional[pulumi.Input[str]] = None,
                 dns_support: Optional[pulumi.Input[str]] = None,
                 ipv6_support: Optional[pulumi.Input[str]] = None,
                 subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transit_gateway_attachment_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_default_route_table_association: Optional[pulumi.Input[bool]] = None,
                 transit_gateway_default_route_table_propagation: Optional[pulumi.Input[bool]] = None,
                 transit_gateway_id: Optional[pulumi.Input[str]] = None,
                 vpc_id: Optional[pulumi.Input[str]] = None,
                 vpc_owner_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering VpcAttachmentAccepter resources.
        :param pulumi.Input[str] appliance_mode_support: Whether Appliance Mode support is enabled. Valid values: `disable`, `enable`.
        :param pulumi.Input[str] dns_support: Whether DNS support is enabled. Valid values: `disable`, `enable`.
        :param pulumi.Input[str] ipv6_support: Whether IPv6 support is enabled. Valid values: `disable`, `enable`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: Identifiers of EC2 Subnets.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value tags for the EC2 Transit Gateway VPC Attachment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] transit_gateway_attachment_id: The ID of the EC2 Transit Gateway Attachment to manage.
        :param pulumi.Input[bool] transit_gateway_default_route_table_association: Boolean whether the VPC Attachment should be associated with the EC2 Transit Gateway association default route table. Default value: `true`.
        :param pulumi.Input[bool] transit_gateway_default_route_table_propagation: Boolean whether the VPC Attachment should propagate routes with the EC2 Transit Gateway propagation default route table. Default value: `true`.
        :param pulumi.Input[str] transit_gateway_id: Identifier of EC2 Transit Gateway.
        :param pulumi.Input[str] vpc_id: Identifier of EC2 VPC.
        :param pulumi.Input[str] vpc_owner_id: Identifier of the AWS account that owns the EC2 VPC.
        """
        if appliance_mode_support is not None:
            pulumi.set(__self__, "appliance_mode_support", appliance_mode_support)
        if dns_support is not None:
            pulumi.set(__self__, "dns_support", dns_support)
        if ipv6_support is not None:
            pulumi.set(__self__, "ipv6_support", ipv6_support)
        if subnet_ids is not None:
            pulumi.set(__self__, "subnet_ids", subnet_ids)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if transit_gateway_attachment_id is not None:
            pulumi.set(__self__, "transit_gateway_attachment_id", transit_gateway_attachment_id)
        if transit_gateway_default_route_table_association is not None:
            pulumi.set(__self__, "transit_gateway_default_route_table_association", transit_gateway_default_route_table_association)
        if transit_gateway_default_route_table_propagation is not None:
            pulumi.set(__self__, "transit_gateway_default_route_table_propagation", transit_gateway_default_route_table_propagation)
        if transit_gateway_id is not None:
            pulumi.set(__self__, "transit_gateway_id", transit_gateway_id)
        if vpc_id is not None:
            pulumi.set(__self__, "vpc_id", vpc_id)
        if vpc_owner_id is not None:
            pulumi.set(__self__, "vpc_owner_id", vpc_owner_id)

    @property
    @pulumi.getter(name="applianceModeSupport")
    def appliance_mode_support(self) -> Optional[pulumi.Input[str]]:
        """
        Whether Appliance Mode support is enabled. Valid values: `disable`, `enable`.
        """
        return pulumi.get(self, "appliance_mode_support")

    @appliance_mode_support.setter
    def appliance_mode_support(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "appliance_mode_support", value)

    @property
    @pulumi.getter(name="dnsSupport")
    def dns_support(self) -> Optional[pulumi.Input[str]]:
        """
        Whether DNS support is enabled. Valid values: `disable`, `enable`.
        """
        return pulumi.get(self, "dns_support")

    @dns_support.setter
    def dns_support(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_support", value)

    @property
    @pulumi.getter(name="ipv6Support")
    def ipv6_support(self) -> Optional[pulumi.Input[str]]:
        """
        Whether IPv6 support is enabled. Valid values: `disable`, `enable`.
        """
        return pulumi.get(self, "ipv6_support")

    @ipv6_support.setter
    def ipv6_support(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipv6_support", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Identifiers of EC2 Subnets.
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value tags for the EC2 Transit Gateway VPC Attachment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)

    @property
    @pulumi.getter(name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the EC2 Transit Gateway Attachment to manage.
        """
        return pulumi.get(self, "transit_gateway_attachment_id")

    @transit_gateway_attachment_id.setter
    def transit_gateway_attachment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transit_gateway_attachment_id", value)

    @property
    @pulumi.getter(name="transitGatewayDefaultRouteTableAssociation")
    def transit_gateway_default_route_table_association(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean whether the VPC Attachment should be associated with the EC2 Transit Gateway association default route table. Default value: `true`.
        """
        return pulumi.get(self, "transit_gateway_default_route_table_association")

    @transit_gateway_default_route_table_association.setter
    def transit_gateway_default_route_table_association(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "transit_gateway_default_route_table_association", value)

    @property
    @pulumi.getter(name="transitGatewayDefaultRouteTablePropagation")
    def transit_gateway_default_route_table_propagation(self) -> Optional[pulumi.Input[bool]]:
        """
        Boolean whether the VPC Attachment should propagate routes with the EC2 Transit Gateway propagation default route table. Default value: `true`.
        """
        return pulumi.get(self, "transit_gateway_default_route_table_propagation")

    @transit_gateway_default_route_table_propagation.setter
    def transit_gateway_default_route_table_propagation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "transit_gateway_default_route_table_propagation", value)

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of EC2 Transit Gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @transit_gateway_id.setter
    def transit_gateway_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transit_gateway_id", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of EC2 VPC.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="vpcOwnerId")
    def vpc_owner_id(self) -> Optional[pulumi.Input[str]]:
        """
        Identifier of the AWS account that owns the EC2 VPC.
        """
        return pulumi.get(self, "vpc_owner_id")

    @vpc_owner_id.setter
    def vpc_owner_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vpc_owner_id", value)


class VpcAttachmentAccepter(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transit_gateway_attachment_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_default_route_table_association: Optional[pulumi.Input[bool]] = None,
                 transit_gateway_default_route_table_propagation: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Manages the accepter's side of an EC2 Transit Gateway VPC Attachment.

        When a cross-account (requester's AWS account differs from the accepter's AWS account) EC2 Transit Gateway VPC Attachment
        is created, an EC2 Transit Gateway VPC Attachment resource is automatically created in the accepter's account.
        The requester can use the `ec2transitgateway.VpcAttachment` resource to manage its side of the connection
        and the accepter can use the `ec2transitgateway.VpcAttachmentAccepter` resource to "adopt" its side of the
        connection into management.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2transitgateway.VpcAttachmentAccepter("example",
            transit_gateway_attachment_id=example_aws_ec2_transit_gateway_vpc_attachment["id"],
            tags={
                "Name": "Example cross-account attachment",
            })
        ```

        ## Import

        Using `pulumi import`, import `aws_ec2_transit_gateway_vpc_attachment_accepter` using the EC2 Transit Gateway Attachment identifier. For example:

        ```sh
        $ pulumi import aws:ec2transitgateway/vpcAttachmentAccepter:VpcAttachmentAccepter example tgw-attach-12345678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value tags for the EC2 Transit Gateway VPC Attachment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] transit_gateway_attachment_id: The ID of the EC2 Transit Gateway Attachment to manage.
        :param pulumi.Input[bool] transit_gateway_default_route_table_association: Boolean whether the VPC Attachment should be associated with the EC2 Transit Gateway association default route table. Default value: `true`.
        :param pulumi.Input[bool] transit_gateway_default_route_table_propagation: Boolean whether the VPC Attachment should propagate routes with the EC2 Transit Gateway propagation default route table. Default value: `true`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VpcAttachmentAccepterArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages the accepter's side of an EC2 Transit Gateway VPC Attachment.

        When a cross-account (requester's AWS account differs from the accepter's AWS account) EC2 Transit Gateway VPC Attachment
        is created, an EC2 Transit Gateway VPC Attachment resource is automatically created in the accepter's account.
        The requester can use the `ec2transitgateway.VpcAttachment` resource to manage its side of the connection
        and the accepter can use the `ec2transitgateway.VpcAttachmentAccepter` resource to "adopt" its side of the
        connection into management.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2transitgateway.VpcAttachmentAccepter("example",
            transit_gateway_attachment_id=example_aws_ec2_transit_gateway_vpc_attachment["id"],
            tags={
                "Name": "Example cross-account attachment",
            })
        ```

        ## Import

        Using `pulumi import`, import `aws_ec2_transit_gateway_vpc_attachment_accepter` using the EC2 Transit Gateway Attachment identifier. For example:

        ```sh
        $ pulumi import aws:ec2transitgateway/vpcAttachmentAccepter:VpcAttachmentAccepter example tgw-attach-12345678
        ```

        :param str resource_name: The name of the resource.
        :param VpcAttachmentAccepterArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VpcAttachmentAccepterArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 transit_gateway_attachment_id: Optional[pulumi.Input[str]] = None,
                 transit_gateway_default_route_table_association: Optional[pulumi.Input[bool]] = None,
                 transit_gateway_default_route_table_propagation: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VpcAttachmentAccepterArgs.__new__(VpcAttachmentAccepterArgs)

            __props__.__dict__["tags"] = tags
            if transit_gateway_attachment_id is None and not opts.urn:
                raise TypeError("Missing required property 'transit_gateway_attachment_id'")
            __props__.__dict__["transit_gateway_attachment_id"] = transit_gateway_attachment_id
            __props__.__dict__["transit_gateway_default_route_table_association"] = transit_gateway_default_route_table_association
            __props__.__dict__["transit_gateway_default_route_table_propagation"] = transit_gateway_default_route_table_propagation
            __props__.__dict__["appliance_mode_support"] = None
            __props__.__dict__["dns_support"] = None
            __props__.__dict__["ipv6_support"] = None
            __props__.__dict__["subnet_ids"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["transit_gateway_id"] = None
            __props__.__dict__["vpc_id"] = None
            __props__.__dict__["vpc_owner_id"] = None
        super(VpcAttachmentAccepter, __self__).__init__(
            'aws:ec2transitgateway/vpcAttachmentAccepter:VpcAttachmentAccepter',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            appliance_mode_support: Optional[pulumi.Input[str]] = None,
            dns_support: Optional[pulumi.Input[str]] = None,
            ipv6_support: Optional[pulumi.Input[str]] = None,
            subnet_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            transit_gateway_attachment_id: Optional[pulumi.Input[str]] = None,
            transit_gateway_default_route_table_association: Optional[pulumi.Input[bool]] = None,
            transit_gateway_default_route_table_propagation: Optional[pulumi.Input[bool]] = None,
            transit_gateway_id: Optional[pulumi.Input[str]] = None,
            vpc_id: Optional[pulumi.Input[str]] = None,
            vpc_owner_id: Optional[pulumi.Input[str]] = None) -> 'VpcAttachmentAccepter':
        """
        Get an existing VpcAttachmentAccepter resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] appliance_mode_support: Whether Appliance Mode support is enabled. Valid values: `disable`, `enable`.
        :param pulumi.Input[str] dns_support: Whether DNS support is enabled. Valid values: `disable`, `enable`.
        :param pulumi.Input[str] ipv6_support: Whether IPv6 support is enabled. Valid values: `disable`, `enable`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: Identifiers of EC2 Subnets.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value tags for the EC2 Transit Gateway VPC Attachment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] transit_gateway_attachment_id: The ID of the EC2 Transit Gateway Attachment to manage.
        :param pulumi.Input[bool] transit_gateway_default_route_table_association: Boolean whether the VPC Attachment should be associated with the EC2 Transit Gateway association default route table. Default value: `true`.
        :param pulumi.Input[bool] transit_gateway_default_route_table_propagation: Boolean whether the VPC Attachment should propagate routes with the EC2 Transit Gateway propagation default route table. Default value: `true`.
        :param pulumi.Input[str] transit_gateway_id: Identifier of EC2 Transit Gateway.
        :param pulumi.Input[str] vpc_id: Identifier of EC2 VPC.
        :param pulumi.Input[str] vpc_owner_id: Identifier of the AWS account that owns the EC2 VPC.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VpcAttachmentAccepterState.__new__(_VpcAttachmentAccepterState)

        __props__.__dict__["appliance_mode_support"] = appliance_mode_support
        __props__.__dict__["dns_support"] = dns_support
        __props__.__dict__["ipv6_support"] = ipv6_support
        __props__.__dict__["subnet_ids"] = subnet_ids
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["transit_gateway_attachment_id"] = transit_gateway_attachment_id
        __props__.__dict__["transit_gateway_default_route_table_association"] = transit_gateway_default_route_table_association
        __props__.__dict__["transit_gateway_default_route_table_propagation"] = transit_gateway_default_route_table_propagation
        __props__.__dict__["transit_gateway_id"] = transit_gateway_id
        __props__.__dict__["vpc_id"] = vpc_id
        __props__.__dict__["vpc_owner_id"] = vpc_owner_id
        return VpcAttachmentAccepter(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applianceModeSupport")
    def appliance_mode_support(self) -> pulumi.Output[str]:
        """
        Whether Appliance Mode support is enabled. Valid values: `disable`, `enable`.
        """
        return pulumi.get(self, "appliance_mode_support")

    @property
    @pulumi.getter(name="dnsSupport")
    def dns_support(self) -> pulumi.Output[str]:
        """
        Whether DNS support is enabled. Valid values: `disable`, `enable`.
        """
        return pulumi.get(self, "dns_support")

    @property
    @pulumi.getter(name="ipv6Support")
    def ipv6_support(self) -> pulumi.Output[str]:
        """
        Whether IPv6 support is enabled. Valid values: `disable`, `enable`.
        """
        return pulumi.get(self, "ipv6_support")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Output[Sequence[str]]:
        """
        Identifiers of EC2 Subnets.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value tags for the EC2 Transit Gateway VPC Attachment. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
        pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")

        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> pulumi.Output[str]:
        """
        The ID of the EC2 Transit Gateway Attachment to manage.
        """
        return pulumi.get(self, "transit_gateway_attachment_id")

    @property
    @pulumi.getter(name="transitGatewayDefaultRouteTableAssociation")
    def transit_gateway_default_route_table_association(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean whether the VPC Attachment should be associated with the EC2 Transit Gateway association default route table. Default value: `true`.
        """
        return pulumi.get(self, "transit_gateway_default_route_table_association")

    @property
    @pulumi.getter(name="transitGatewayDefaultRouteTablePropagation")
    def transit_gateway_default_route_table_propagation(self) -> pulumi.Output[Optional[bool]]:
        """
        Boolean whether the VPC Attachment should propagate routes with the EC2 Transit Gateway propagation default route table. Default value: `true`.
        """
        return pulumi.get(self, "transit_gateway_default_route_table_propagation")

    @property
    @pulumi.getter(name="transitGatewayId")
    def transit_gateway_id(self) -> pulumi.Output[str]:
        """
        Identifier of EC2 Transit Gateway.
        """
        return pulumi.get(self, "transit_gateway_id")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Output[str]:
        """
        Identifier of EC2 VPC.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vpcOwnerId")
    def vpc_owner_id(self) -> pulumi.Output[str]:
        """
        Identifier of the AWS account that owns the EC2 VPC.
        """
        return pulumi.get(self, "vpc_owner_id")

