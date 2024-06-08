# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['IdentityPolicyArgs', 'IdentityPolicy']

@pulumi.input_type
class IdentityPolicyArgs:
    def __init__(__self__, *,
                 identity: pulumi.Input[str],
                 policy: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a IdentityPolicy resource.
        :param pulumi.Input[str] identity: Name or Amazon Resource Name (ARN) of the SES Identity.
        :param pulumi.Input[str] policy: JSON string of the policy.
        :param pulumi.Input[str] name: Name of the policy.
        """
        pulumi.set(__self__, "identity", identity)
        pulumi.set(__self__, "policy", policy)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Input[str]:
        """
        Name or Amazon Resource Name (ARN) of the SES Identity.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: pulumi.Input[str]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        JSON string of the policy.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _IdentityPolicyState:
    def __init__(__self__, *,
                 identity: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering IdentityPolicy resources.
        :param pulumi.Input[str] identity: Name or Amazon Resource Name (ARN) of the SES Identity.
        :param pulumi.Input[str] name: Name of the policy.
        :param pulumi.Input[str] policy: JSON string of the policy.
        """
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input[str]]:
        """
        Name or Amazon Resource Name (ARN) of the SES Identity.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        JSON string of the policy.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)


class IdentityPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a SES Identity Policy. More information about SES Sending Authorization Policies can be found in the [SES Developer Guide](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/sending-authorization-policies.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_domain_identity = aws.ses.DomainIdentity("example", domain="example.com")
        example = aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            actions=[
                "SES:SendEmail",
                "SES:SendRawEmail",
            ],
            resources=[example_domain_identity.arn],
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                identifiers=["*"],
                type="AWS",
            )],
        )])
        example_identity_policy = aws.ses.IdentityPolicy("example",
            identity=example_domain_identity.arn,
            name="example",
            policy=example.json)
        ```

        ## Import

        Using `pulumi import`, import SES Identity Policies using the identity and policy name, separated by a pipe character (`|`). For example:

        ```sh
        $ pulumi import aws:ses/identityPolicy:IdentityPolicy example 'example.com|example'
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identity: Name or Amazon Resource Name (ARN) of the SES Identity.
        :param pulumi.Input[str] name: Name of the policy.
        :param pulumi.Input[str] policy: JSON string of the policy.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: IdentityPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a SES Identity Policy. More information about SES Sending Authorization Policies can be found in the [SES Developer Guide](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/sending-authorization-policies.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_domain_identity = aws.ses.DomainIdentity("example", domain="example.com")
        example = aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            actions=[
                "SES:SendEmail",
                "SES:SendRawEmail",
            ],
            resources=[example_domain_identity.arn],
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                identifiers=["*"],
                type="AWS",
            )],
        )])
        example_identity_policy = aws.ses.IdentityPolicy("example",
            identity=example_domain_identity.arn,
            name="example",
            policy=example.json)
        ```

        ## Import

        Using `pulumi import`, import SES Identity Policies using the identity and policy name, separated by a pipe character (`|`). For example:

        ```sh
        $ pulumi import aws:ses/identityPolicy:IdentityPolicy example 'example.com|example'
        ```

        :param str resource_name: The name of the resource.
        :param IdentityPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(IdentityPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = IdentityPolicyArgs.__new__(IdentityPolicyArgs)

            if identity is None and not opts.urn:
                raise TypeError("Missing required property 'identity'")
            __props__.__dict__["identity"] = identity
            __props__.__dict__["name"] = name
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
        super(IdentityPolicy, __self__).__init__(
            'aws:ses/identityPolicy:IdentityPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            identity: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None) -> 'IdentityPolicy':
        """
        Get an existing IdentityPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identity: Name or Amazon Resource Name (ARN) of the SES Identity.
        :param pulumi.Input[str] name: Name of the policy.
        :param pulumi.Input[str] policy: JSON string of the policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _IdentityPolicyState.__new__(_IdentityPolicyState)

        __props__.__dict__["identity"] = identity
        __props__.__dict__["name"] = name
        __props__.__dict__["policy"] = policy
        return IdentityPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[str]:
        """
        Name or Amazon Resource Name (ARN) of the SES Identity.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        JSON string of the policy.
        """
        return pulumi.get(self, "policy")

