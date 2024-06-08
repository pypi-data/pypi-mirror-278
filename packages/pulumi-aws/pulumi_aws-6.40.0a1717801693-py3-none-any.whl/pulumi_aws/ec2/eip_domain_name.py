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

__all__ = ['EipDomainNameArgs', 'EipDomainName']

@pulumi.input_type
class EipDomainNameArgs:
    def __init__(__self__, *,
                 allocation_id: pulumi.Input[str],
                 domain_name: pulumi.Input[str],
                 timeouts: Optional[pulumi.Input['EipDomainNameTimeoutsArgs']] = None):
        """
        The set of arguments for constructing a EipDomainName resource.
        :param pulumi.Input[str] allocation_id: The allocation ID.
        :param pulumi.Input[str] domain_name: The domain name to modify for the IP address.
        """
        pulumi.set(__self__, "allocation_id", allocation_id)
        pulumi.set(__self__, "domain_name", domain_name)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> pulumi.Input[str]:
        """
        The allocation ID.
        """
        return pulumi.get(self, "allocation_id")

    @allocation_id.setter
    def allocation_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "allocation_id", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Input[str]:
        """
        The domain name to modify for the IP address.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['EipDomainNameTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['EipDomainNameTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


@pulumi.input_type
class _EipDomainNameState:
    def __init__(__self__, *,
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 ptr_record: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input['EipDomainNameTimeoutsArgs']] = None):
        """
        Input properties used for looking up and filtering EipDomainName resources.
        :param pulumi.Input[str] allocation_id: The allocation ID.
        :param pulumi.Input[str] domain_name: The domain name to modify for the IP address.
        :param pulumi.Input[str] ptr_record: The DNS pointer (PTR) record for the IP address.
        """
        if allocation_id is not None:
            pulumi.set(__self__, "allocation_id", allocation_id)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if ptr_record is not None:
            pulumi.set(__self__, "ptr_record", ptr_record)
        if timeouts is not None:
            pulumi.set(__self__, "timeouts", timeouts)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> Optional[pulumi.Input[str]]:
        """
        The allocation ID.
        """
        return pulumi.get(self, "allocation_id")

    @allocation_id.setter
    def allocation_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "allocation_id", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name to modify for the IP address.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="ptrRecord")
    def ptr_record(self) -> Optional[pulumi.Input[str]]:
        """
        The DNS pointer (PTR) record for the IP address.
        """
        return pulumi.get(self, "ptr_record")

    @ptr_record.setter
    def ptr_record(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ptr_record", value)

    @property
    @pulumi.getter
    def timeouts(self) -> Optional[pulumi.Input['EipDomainNameTimeoutsArgs']]:
        return pulumi.get(self, "timeouts")

    @timeouts.setter
    def timeouts(self, value: Optional[pulumi.Input['EipDomainNameTimeoutsArgs']]):
        pulumi.set(self, "timeouts", value)


class EipDomainName(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[pulumi.InputType['EipDomainNameTimeoutsArgs']]] = None,
                 __props__=None):
        """
        Assigns a static reverse DNS record to an Elastic IP addresses. See [Using reverse DNS for email applications](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#Using_Elastic_Addressing_Reverse_DNS).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.Eip("example", domain="vpc")
        example_record = aws.route53.Record("example",
            zone_id=main["zoneId"],
            name="reverse",
            type=aws.route53.RecordType.A,
            records=[example.public_ip])
        example_eip_domain_name = aws.ec2.EipDomainName("example",
            allocation_id=example.allocation_id,
            domain_name=example_record.fqdn)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allocation_id: The allocation ID.
        :param pulumi.Input[str] domain_name: The domain name to modify for the IP address.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EipDomainNameArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Assigns a static reverse DNS record to an Elastic IP addresses. See [Using reverse DNS for email applications](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html#Using_Elastic_Addressing_Reverse_DNS).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.ec2.Eip("example", domain="vpc")
        example_record = aws.route53.Record("example",
            zone_id=main["zoneId"],
            name="reverse",
            type=aws.route53.RecordType.A,
            records=[example.public_ip])
        example_eip_domain_name = aws.ec2.EipDomainName("example",
            allocation_id=example.allocation_id,
            domain_name=example_record.fqdn)
        ```

        :param str resource_name: The name of the resource.
        :param EipDomainNameArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EipDomainNameArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocation_id: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 timeouts: Optional[pulumi.Input[pulumi.InputType['EipDomainNameTimeoutsArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EipDomainNameArgs.__new__(EipDomainNameArgs)

            if allocation_id is None and not opts.urn:
                raise TypeError("Missing required property 'allocation_id'")
            __props__.__dict__["allocation_id"] = allocation_id
            if domain_name is None and not opts.urn:
                raise TypeError("Missing required property 'domain_name'")
            __props__.__dict__["domain_name"] = domain_name
            __props__.__dict__["timeouts"] = timeouts
            __props__.__dict__["ptr_record"] = None
        super(EipDomainName, __self__).__init__(
            'aws:ec2/eipDomainName:EipDomainName',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allocation_id: Optional[pulumi.Input[str]] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            ptr_record: Optional[pulumi.Input[str]] = None,
            timeouts: Optional[pulumi.Input[pulumi.InputType['EipDomainNameTimeoutsArgs']]] = None) -> 'EipDomainName':
        """
        Get an existing EipDomainName resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] allocation_id: The allocation ID.
        :param pulumi.Input[str] domain_name: The domain name to modify for the IP address.
        :param pulumi.Input[str] ptr_record: The DNS pointer (PTR) record for the IP address.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EipDomainNameState.__new__(_EipDomainNameState)

        __props__.__dict__["allocation_id"] = allocation_id
        __props__.__dict__["domain_name"] = domain_name
        __props__.__dict__["ptr_record"] = ptr_record
        __props__.__dict__["timeouts"] = timeouts
        return EipDomainName(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allocationId")
    def allocation_id(self) -> pulumi.Output[str]:
        """
        The allocation ID.
        """
        return pulumi.get(self, "allocation_id")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The domain name to modify for the IP address.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="ptrRecord")
    def ptr_record(self) -> pulumi.Output[str]:
        """
        The DNS pointer (PTR) record for the IP address.
        """
        return pulumi.get(self, "ptr_record")

    @property
    @pulumi.getter
    def timeouts(self) -> pulumi.Output[Optional['outputs.EipDomainNameTimeouts']]:
        return pulumi.get(self, "timeouts")

