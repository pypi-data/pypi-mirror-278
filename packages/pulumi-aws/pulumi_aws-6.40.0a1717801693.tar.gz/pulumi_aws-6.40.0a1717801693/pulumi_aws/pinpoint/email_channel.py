# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['EmailChannelArgs', 'EmailChannel']

@pulumi.input_type
class EmailChannelArgs:
    def __init__(__self__, *,
                 application_id: pulumi.Input[str],
                 from_address: pulumi.Input[str],
                 identity: pulumi.Input[str],
                 configuration_set: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a EmailChannel resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] from_address: The email address used to send emails from. You can use email only (`user@example.com`) or friendly address (`User <user@example.com>`). This field comply with [RFC 5322](https://www.ietf.org/rfc/rfc5322.txt).
        :param pulumi.Input[str] identity: The ARN of an identity verified with SES.
        :param pulumi.Input[str] configuration_set: The ARN of the Amazon SES configuration set that you want to apply to messages that you send through the channel.
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] role_arn: The ARN of an IAM Role used to submit events to Mobile Analytics' event ingestion service.
        """
        pulumi.set(__self__, "application_id", application_id)
        pulumi.set(__self__, "from_address", from_address)
        pulumi.set(__self__, "identity", identity)
        if configuration_set is not None:
            pulumi.set(__self__, "configuration_set", configuration_set)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Input[str]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter(name="fromAddress")
    def from_address(self) -> pulumi.Input[str]:
        """
        The email address used to send emails from. You can use email only (`user@example.com`) or friendly address (`User <user@example.com>`). This field comply with [RFC 5322](https://www.ietf.org/rfc/rfc5322.txt).
        """
        return pulumi.get(self, "from_address")

    @from_address.setter
    def from_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "from_address", value)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Input[str]:
        """
        The ARN of an identity verified with SES.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: pulumi.Input[str]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="configurationSet")
    def configuration_set(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the Amazon SES configuration set that you want to apply to messages that you send through the channel.
        """
        return pulumi.get(self, "configuration_set")

    @configuration_set.setter
    def configuration_set(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_set", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the channel is enabled or disabled. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of an IAM Role used to submit events to Mobile Analytics' event ingestion service.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)


@pulumi.input_type
class _EmailChannelState:
    def __init__(__self__, *,
                 application_id: Optional[pulumi.Input[str]] = None,
                 configuration_set: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 from_address: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[str]] = None,
                 messages_per_second: Optional[pulumi.Input[int]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering EmailChannel resources.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] configuration_set: The ARN of the Amazon SES configuration set that you want to apply to messages that you send through the channel.
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] from_address: The email address used to send emails from. You can use email only (`user@example.com`) or friendly address (`User <user@example.com>`). This field comply with [RFC 5322](https://www.ietf.org/rfc/rfc5322.txt).
        :param pulumi.Input[str] identity: The ARN of an identity verified with SES.
        :param pulumi.Input[int] messages_per_second: Messages per second that can be sent.
        :param pulumi.Input[str] role_arn: The ARN of an IAM Role used to submit events to Mobile Analytics' event ingestion service.
        """
        if application_id is not None:
            pulumi.set(__self__, "application_id", application_id)
        if configuration_set is not None:
            pulumi.set(__self__, "configuration_set", configuration_set)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if from_address is not None:
            pulumi.set(__self__, "from_address", from_address)
        if identity is not None:
            pulumi.set(__self__, "identity", identity)
        if messages_per_second is not None:
            pulumi.set(__self__, "messages_per_second", messages_per_second)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> Optional[pulumi.Input[str]]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @application_id.setter
    def application_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "application_id", value)

    @property
    @pulumi.getter(name="configurationSet")
    def configuration_set(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the Amazon SES configuration set that you want to apply to messages that you send through the channel.
        """
        return pulumi.get(self, "configuration_set")

    @configuration_set.setter
    def configuration_set(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_set", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether the channel is enabled or disabled. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="fromAddress")
    def from_address(self) -> Optional[pulumi.Input[str]]:
        """
        The email address used to send emails from. You can use email only (`user@example.com`) or friendly address (`User <user@example.com>`). This field comply with [RFC 5322](https://www.ietf.org/rfc/rfc5322.txt).
        """
        return pulumi.get(self, "from_address")

    @from_address.setter
    def from_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "from_address", value)

    @property
    @pulumi.getter
    def identity(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of an identity verified with SES.
        """
        return pulumi.get(self, "identity")

    @identity.setter
    def identity(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity", value)

    @property
    @pulumi.getter(name="messagesPerSecond")
    def messages_per_second(self) -> Optional[pulumi.Input[int]]:
        """
        Messages per second that can be sent.
        """
        return pulumi.get(self, "messages_per_second")

    @messages_per_second.setter
    def messages_per_second(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "messages_per_second", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of an IAM Role used to submit events to Mobile Analytics' event ingestion service.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)


class EmailChannel(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 configuration_set: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 from_address: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Pinpoint Email Channel resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        app = aws.pinpoint.App("app")
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["pinpoint.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        role = aws.iam.Role("role", assume_role_policy=assume_role.json)
        email = aws.pinpoint.EmailChannel("email",
            application_id=app.application_id,
            from_address="user@example.com",
            role_arn=role.arn)
        identity = aws.ses.DomainIdentity("identity", domain="example.com")
        role_policy = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=[
                "mobileanalytics:PutEvents",
                "mobileanalytics:PutItems",
            ],
            resources=["*"],
        )])
        role_policy_role_policy = aws.iam.RolePolicy("role_policy",
            name="role_policy",
            role=role.id,
            policy=role_policy.json)
        ```

        ## Import

        Using `pulumi import`, import Pinpoint Email Channel using the `application-id`. For example:

        ```sh
        $ pulumi import aws:pinpoint/emailChannel:EmailChannel email application-id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] configuration_set: The ARN of the Amazon SES configuration set that you want to apply to messages that you send through the channel.
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] from_address: The email address used to send emails from. You can use email only (`user@example.com`) or friendly address (`User <user@example.com>`). This field comply with [RFC 5322](https://www.ietf.org/rfc/rfc5322.txt).
        :param pulumi.Input[str] identity: The ARN of an identity verified with SES.
        :param pulumi.Input[str] role_arn: The ARN of an IAM Role used to submit events to Mobile Analytics' event ingestion service.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EmailChannelArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Pinpoint Email Channel resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        app = aws.pinpoint.App("app")
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["pinpoint.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        role = aws.iam.Role("role", assume_role_policy=assume_role.json)
        email = aws.pinpoint.EmailChannel("email",
            application_id=app.application_id,
            from_address="user@example.com",
            role_arn=role.arn)
        identity = aws.ses.DomainIdentity("identity", domain="example.com")
        role_policy = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            actions=[
                "mobileanalytics:PutEvents",
                "mobileanalytics:PutItems",
            ],
            resources=["*"],
        )])
        role_policy_role_policy = aws.iam.RolePolicy("role_policy",
            name="role_policy",
            role=role.id,
            policy=role_policy.json)
        ```

        ## Import

        Using `pulumi import`, import Pinpoint Email Channel using the `application-id`. For example:

        ```sh
        $ pulumi import aws:pinpoint/emailChannel:EmailChannel email application-id
        ```

        :param str resource_name: The name of the resource.
        :param EmailChannelArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EmailChannelArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_id: Optional[pulumi.Input[str]] = None,
                 configuration_set: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 from_address: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EmailChannelArgs.__new__(EmailChannelArgs)

            if application_id is None and not opts.urn:
                raise TypeError("Missing required property 'application_id'")
            __props__.__dict__["application_id"] = application_id
            __props__.__dict__["configuration_set"] = configuration_set
            __props__.__dict__["enabled"] = enabled
            if from_address is None and not opts.urn:
                raise TypeError("Missing required property 'from_address'")
            __props__.__dict__["from_address"] = from_address
            if identity is None and not opts.urn:
                raise TypeError("Missing required property 'identity'")
            __props__.__dict__["identity"] = identity
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["messages_per_second"] = None
        super(EmailChannel, __self__).__init__(
            'aws:pinpoint/emailChannel:EmailChannel',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            application_id: Optional[pulumi.Input[str]] = None,
            configuration_set: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            from_address: Optional[pulumi.Input[str]] = None,
            identity: Optional[pulumi.Input[str]] = None,
            messages_per_second: Optional[pulumi.Input[int]] = None,
            role_arn: Optional[pulumi.Input[str]] = None) -> 'EmailChannel':
        """
        Get an existing EmailChannel resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_id: The application ID.
        :param pulumi.Input[str] configuration_set: The ARN of the Amazon SES configuration set that you want to apply to messages that you send through the channel.
        :param pulumi.Input[bool] enabled: Whether the channel is enabled or disabled. Defaults to `true`.
        :param pulumi.Input[str] from_address: The email address used to send emails from. You can use email only (`user@example.com`) or friendly address (`User <user@example.com>`). This field comply with [RFC 5322](https://www.ietf.org/rfc/rfc5322.txt).
        :param pulumi.Input[str] identity: The ARN of an identity verified with SES.
        :param pulumi.Input[int] messages_per_second: Messages per second that can be sent.
        :param pulumi.Input[str] role_arn: The ARN of an IAM Role used to submit events to Mobile Analytics' event ingestion service.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EmailChannelState.__new__(_EmailChannelState)

        __props__.__dict__["application_id"] = application_id
        __props__.__dict__["configuration_set"] = configuration_set
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["from_address"] = from_address
        __props__.__dict__["identity"] = identity
        __props__.__dict__["messages_per_second"] = messages_per_second
        __props__.__dict__["role_arn"] = role_arn
        return EmailChannel(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationId")
    def application_id(self) -> pulumi.Output[str]:
        """
        The application ID.
        """
        return pulumi.get(self, "application_id")

    @property
    @pulumi.getter(name="configurationSet")
    def configuration_set(self) -> pulumi.Output[Optional[str]]:
        """
        The ARN of the Amazon SES configuration set that you want to apply to messages that you send through the channel.
        """
        return pulumi.get(self, "configuration_set")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the channel is enabled or disabled. Defaults to `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="fromAddress")
    def from_address(self) -> pulumi.Output[str]:
        """
        The email address used to send emails from. You can use email only (`user@example.com`) or friendly address (`User <user@example.com>`). This field comply with [RFC 5322](https://www.ietf.org/rfc/rfc5322.txt).
        """
        return pulumi.get(self, "from_address")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[str]:
        """
        The ARN of an identity verified with SES.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="messagesPerSecond")
    def messages_per_second(self) -> pulumi.Output[int]:
        """
        Messages per second that can be sent.
        """
        return pulumi.get(self, "messages_per_second")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The ARN of an IAM Role used to submit events to Mobile Analytics' event ingestion service.
        """
        return pulumi.get(self, "role_arn")

