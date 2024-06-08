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

__all__ = ['LbCertificateArgs', 'LbCertificate']

@pulumi.input_type
class LbCertificateArgs:
    def __init__(__self__, *,
                 lb_name: pulumi.Input[str],
                 domain_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subject_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a LbCertificate resource.
        :param pulumi.Input[str] lb_name: The load balancer name where you want to create the SSL/TLS certificate.
        :param pulumi.Input[str] domain_name: The domain name (e.g., example.com) for your SSL/TLS certificate.
        :param pulumi.Input[str] name: The SSL/TLS certificate name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subject_alternative_names: Set of domains that should be SANs in the issued certificate. `domain_name` attribute is automatically added as a Subject Alternative Name.
        """
        pulumi.set(__self__, "lb_name", lb_name)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if subject_alternative_names is not None:
            pulumi.set(__self__, "subject_alternative_names", subject_alternative_names)

    @property
    @pulumi.getter(name="lbName")
    def lb_name(self) -> pulumi.Input[str]:
        """
        The load balancer name where you want to create the SSL/TLS certificate.
        """
        return pulumi.get(self, "lb_name")

    @lb_name.setter
    def lb_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "lb_name", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name (e.g., example.com) for your SSL/TLS certificate.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The SSL/TLS certificate name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="subjectAlternativeNames")
    def subject_alternative_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of domains that should be SANs in the issued certificate. `domain_name` attribute is automatically added as a Subject Alternative Name.
        """
        return pulumi.get(self, "subject_alternative_names")

    @subject_alternative_names.setter
    def subject_alternative_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subject_alternative_names", value)


@pulumi.input_type
class _LbCertificateState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 domain_validation_records: Optional[pulumi.Input[Sequence[pulumi.Input['LbCertificateDomainValidationRecordArgs']]]] = None,
                 lb_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subject_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 support_code: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LbCertificate resources.
        :param pulumi.Input[str] arn: The ARN of the lightsail certificate.
        :param pulumi.Input[str] created_at: The timestamp when the instance was created.
        :param pulumi.Input[str] domain_name: The domain name (e.g., example.com) for your SSL/TLS certificate.
        :param pulumi.Input[str] lb_name: The load balancer name where you want to create the SSL/TLS certificate.
        :param pulumi.Input[str] name: The SSL/TLS certificate name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subject_alternative_names: Set of domains that should be SANs in the issued certificate. `domain_name` attribute is automatically added as a Subject Alternative Name.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if domain_validation_records is not None:
            pulumi.set(__self__, "domain_validation_records", domain_validation_records)
        if lb_name is not None:
            pulumi.set(__self__, "lb_name", lb_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if subject_alternative_names is not None:
            pulumi.set(__self__, "subject_alternative_names", subject_alternative_names)
        if support_code is not None:
            pulumi.set(__self__, "support_code", support_code)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the lightsail certificate.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp when the instance was created.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name (e.g., example.com) for your SSL/TLS certificate.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="domainValidationRecords")
    def domain_validation_records(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['LbCertificateDomainValidationRecordArgs']]]]:
        return pulumi.get(self, "domain_validation_records")

    @domain_validation_records.setter
    def domain_validation_records(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['LbCertificateDomainValidationRecordArgs']]]]):
        pulumi.set(self, "domain_validation_records", value)

    @property
    @pulumi.getter(name="lbName")
    def lb_name(self) -> Optional[pulumi.Input[str]]:
        """
        The load balancer name where you want to create the SSL/TLS certificate.
        """
        return pulumi.get(self, "lb_name")

    @lb_name.setter
    def lb_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lb_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The SSL/TLS certificate name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="subjectAlternativeNames")
    def subject_alternative_names(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of domains that should be SANs in the issued certificate. `domain_name` attribute is automatically added as a Subject Alternative Name.
        """
        return pulumi.get(self, "subject_alternative_names")

    @subject_alternative_names.setter
    def subject_alternative_names(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "subject_alternative_names", value)

    @property
    @pulumi.getter(name="supportCode")
    def support_code(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "support_code")

    @support_code.setter
    def support_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "support_code", value)


class LbCertificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 lb_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subject_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Creates a Lightsail load balancer Certificate resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.lightsail.Lb("test",
            name="test-load-balancer",
            health_check_path="/",
            instance_port=80,
            tags={
                "foo": "bar",
            })
        test_lb_certificate = aws.lightsail.LbCertificate("test",
            name="test-load-balancer-certificate",
            lb_name=test.id,
            domain_name="test.com")
        ```

        ## Import

        Using `pulumi import`, import `aws_lightsail_lb_certificate` using the id attribute. For example:

        ```sh
        $ pulumi import aws:lightsail/lbCertificate:LbCertificate test example-load-balancer,example-load-balancer-certificate
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_name: The domain name (e.g., example.com) for your SSL/TLS certificate.
        :param pulumi.Input[str] lb_name: The load balancer name where you want to create the SSL/TLS certificate.
        :param pulumi.Input[str] name: The SSL/TLS certificate name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subject_alternative_names: Set of domains that should be SANs in the issued certificate. `domain_name` attribute is automatically added as a Subject Alternative Name.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LbCertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a Lightsail load balancer Certificate resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.lightsail.Lb("test",
            name="test-load-balancer",
            health_check_path="/",
            instance_port=80,
            tags={
                "foo": "bar",
            })
        test_lb_certificate = aws.lightsail.LbCertificate("test",
            name="test-load-balancer-certificate",
            lb_name=test.id,
            domain_name="test.com")
        ```

        ## Import

        Using `pulumi import`, import `aws_lightsail_lb_certificate` using the id attribute. For example:

        ```sh
        $ pulumi import aws:lightsail/lbCertificate:LbCertificate test example-load-balancer,example-load-balancer-certificate
        ```

        :param str resource_name: The name of the resource.
        :param LbCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LbCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 lb_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subject_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LbCertificateArgs.__new__(LbCertificateArgs)

            __props__.__dict__["domain_name"] = domain_name
            if lb_name is None and not opts.urn:
                raise TypeError("Missing required property 'lb_name'")
            __props__.__dict__["lb_name"] = lb_name
            __props__.__dict__["name"] = name
            __props__.__dict__["subject_alternative_names"] = subject_alternative_names
            __props__.__dict__["arn"] = None
            __props__.__dict__["created_at"] = None
            __props__.__dict__["domain_validation_records"] = None
            __props__.__dict__["support_code"] = None
        super(LbCertificate, __self__).__init__(
            'aws:lightsail/lbCertificate:LbCertificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            domain_validation_records: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['LbCertificateDomainValidationRecordArgs']]]]] = None,
            lb_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            subject_alternative_names: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            support_code: Optional[pulumi.Input[str]] = None) -> 'LbCertificate':
        """
        Get an existing LbCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the lightsail certificate.
        :param pulumi.Input[str] created_at: The timestamp when the instance was created.
        :param pulumi.Input[str] domain_name: The domain name (e.g., example.com) for your SSL/TLS certificate.
        :param pulumi.Input[str] lb_name: The load balancer name where you want to create the SSL/TLS certificate.
        :param pulumi.Input[str] name: The SSL/TLS certificate name.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subject_alternative_names: Set of domains that should be SANs in the issued certificate. `domain_name` attribute is automatically added as a Subject Alternative Name.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LbCertificateState.__new__(_LbCertificateState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["domain_name"] = domain_name
        __props__.__dict__["domain_validation_records"] = domain_validation_records
        __props__.__dict__["lb_name"] = lb_name
        __props__.__dict__["name"] = name
        __props__.__dict__["subject_alternative_names"] = subject_alternative_names
        __props__.__dict__["support_code"] = support_code
        return LbCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the lightsail certificate.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The timestamp when the instance was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        The domain name (e.g., example.com) for your SSL/TLS certificate.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="domainValidationRecords")
    def domain_validation_records(self) -> pulumi.Output[Sequence['outputs.LbCertificateDomainValidationRecord']]:
        return pulumi.get(self, "domain_validation_records")

    @property
    @pulumi.getter(name="lbName")
    def lb_name(self) -> pulumi.Output[str]:
        """
        The load balancer name where you want to create the SSL/TLS certificate.
        """
        return pulumi.get(self, "lb_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The SSL/TLS certificate name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="subjectAlternativeNames")
    def subject_alternative_names(self) -> pulumi.Output[Sequence[str]]:
        """
        Set of domains that should be SANs in the issued certificate. `domain_name` attribute is automatically added as a Subject Alternative Name.
        """
        return pulumi.get(self, "subject_alternative_names")

    @property
    @pulumi.getter(name="supportCode")
    def support_code(self) -> pulumi.Output[str]:
        return pulumi.get(self, "support_code")

