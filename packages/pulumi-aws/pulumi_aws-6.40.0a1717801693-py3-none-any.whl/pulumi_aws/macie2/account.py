# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['AccountArgs', 'Account']

@pulumi.input_type
class AccountArgs:
    def __init__(__self__, *,
                 finding_publishing_frequency: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Account resource.
        :param pulumi.Input[str] finding_publishing_frequency: Specifies how often to publish updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly called Amazon CloudWatch Events). Valid values are `FIFTEEN_MINUTES`, `ONE_HOUR` or `SIX_HOURS`.
        :param pulumi.Input[str] status: Specifies the status for the account. To enable Amazon Macie and start all Macie activities for the account, set this value to `ENABLED`. Valid values are `ENABLED` or `PAUSED`.
        """
        if finding_publishing_frequency is not None:
            pulumi.set(__self__, "finding_publishing_frequency", finding_publishing_frequency)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how often to publish updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly called Amazon CloudWatch Events). Valid values are `FIFTEEN_MINUTES`, `ONE_HOUR` or `SIX_HOURS`.
        """
        return pulumi.get(self, "finding_publishing_frequency")

    @finding_publishing_frequency.setter
    def finding_publishing_frequency(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "finding_publishing_frequency", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status for the account. To enable Amazon Macie and start all Macie activities for the account, set this value to `ENABLED`. Valid values are `ENABLED` or `PAUSED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class _AccountState:
    def __init__(__self__, *,
                 created_at: Optional[pulumi.Input[str]] = None,
                 finding_publishing_frequency: Optional[pulumi.Input[str]] = None,
                 service_role: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Account resources.
        :param pulumi.Input[str] created_at: The date and time, in UTC and extended RFC 3339 format, when the Amazon Macie account was created.
        :param pulumi.Input[str] finding_publishing_frequency: Specifies how often to publish updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly called Amazon CloudWatch Events). Valid values are `FIFTEEN_MINUTES`, `ONE_HOUR` or `SIX_HOURS`.
        :param pulumi.Input[str] service_role: The Amazon Resource Name (ARN) of the service-linked role that allows Macie to monitor and analyze data in AWS resources for the account.
        :param pulumi.Input[str] status: Specifies the status for the account. To enable Amazon Macie and start all Macie activities for the account, set this value to `ENABLED`. Valid values are `ENABLED` or `PAUSED`.
        :param pulumi.Input[str] updated_at: The date and time, in UTC and extended RFC 3339 format, of the most recent change to the status of the Macie account.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if finding_publishing_frequency is not None:
            pulumi.set(__self__, "finding_publishing_frequency", finding_publishing_frequency)
        if service_role is not None:
            pulumi.set(__self__, "service_role", service_role)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time, in UTC and extended RFC 3339 format, when the Amazon Macie account was created.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter(name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies how often to publish updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly called Amazon CloudWatch Events). Valid values are `FIFTEEN_MINUTES`, `ONE_HOUR` or `SIX_HOURS`.
        """
        return pulumi.get(self, "finding_publishing_frequency")

    @finding_publishing_frequency.setter
    def finding_publishing_frequency(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "finding_publishing_frequency", value)

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the service-linked role that allows Macie to monitor and analyze data in AWS resources for the account.
        """
        return pulumi.get(self, "service_role")

    @service_role.setter
    def service_role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "service_role", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the status for the account. To enable Amazon Macie and start all Macie activities for the account, set this value to `ENABLED`. Valid values are `ENABLED` or `PAUSED`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[str]]:
        """
        The date and time, in UTC and extended RFC 3339 format, of the most recent change to the status of the Macie account.
        """
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_at", value)


class Account(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 finding_publishing_frequency: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a resource to manage an [AWS Macie Account](https://docs.aws.amazon.com/macie/latest/APIReference/macie.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.macie2.Account("test",
            finding_publishing_frequency="FIFTEEN_MINUTES",
            status="ENABLED")
        ```

        ## Import

        Using `pulumi import`, import `aws_macie2_account` using the id. For example:

        ```sh
        $ pulumi import aws:macie2/account:Account example abcd1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] finding_publishing_frequency: Specifies how often to publish updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly called Amazon CloudWatch Events). Valid values are `FIFTEEN_MINUTES`, `ONE_HOUR` or `SIX_HOURS`.
        :param pulumi.Input[str] status: Specifies the status for the account. To enable Amazon Macie and start all Macie activities for the account, set this value to `ENABLED`. Valid values are `ENABLED` or `PAUSED`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AccountArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a resource to manage an [AWS Macie Account](https://docs.aws.amazon.com/macie/latest/APIReference/macie.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.macie2.Account("test",
            finding_publishing_frequency="FIFTEEN_MINUTES",
            status="ENABLED")
        ```

        ## Import

        Using `pulumi import`, import `aws_macie2_account` using the id. For example:

        ```sh
        $ pulumi import aws:macie2/account:Account example abcd1
        ```

        :param str resource_name: The name of the resource.
        :param AccountArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AccountArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 finding_publishing_frequency: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = AccountArgs.__new__(AccountArgs)

            __props__.__dict__["finding_publishing_frequency"] = finding_publishing_frequency
            __props__.__dict__["status"] = status
            __props__.__dict__["created_at"] = None
            __props__.__dict__["service_role"] = None
            __props__.__dict__["updated_at"] = None
        super(Account, __self__).__init__(
            'aws:macie2/account:Account',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            finding_publishing_frequency: Optional[pulumi.Input[str]] = None,
            service_role: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            updated_at: Optional[pulumi.Input[str]] = None) -> 'Account':
        """
        Get an existing Account resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] created_at: The date and time, in UTC and extended RFC 3339 format, when the Amazon Macie account was created.
        :param pulumi.Input[str] finding_publishing_frequency: Specifies how often to publish updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly called Amazon CloudWatch Events). Valid values are `FIFTEEN_MINUTES`, `ONE_HOUR` or `SIX_HOURS`.
        :param pulumi.Input[str] service_role: The Amazon Resource Name (ARN) of the service-linked role that allows Macie to monitor and analyze data in AWS resources for the account.
        :param pulumi.Input[str] status: Specifies the status for the account. To enable Amazon Macie and start all Macie activities for the account, set this value to `ENABLED`. Valid values are `ENABLED` or `PAUSED`.
        :param pulumi.Input[str] updated_at: The date and time, in UTC and extended RFC 3339 format, of the most recent change to the status of the Macie account.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _AccountState.__new__(_AccountState)

        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["finding_publishing_frequency"] = finding_publishing_frequency
        __props__.__dict__["service_role"] = service_role
        __props__.__dict__["status"] = status
        __props__.__dict__["updated_at"] = updated_at
        return Account(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        The date and time, in UTC and extended RFC 3339 format, when the Amazon Macie account was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="findingPublishingFrequency")
    def finding_publishing_frequency(self) -> pulumi.Output[str]:
        """
        Specifies how often to publish updates to policy findings for the account. This includes publishing updates to AWS Security Hub and Amazon EventBridge (formerly called Amazon CloudWatch Events). Valid values are `FIFTEEN_MINUTES`, `ONE_HOUR` or `SIX_HOURS`.
        """
        return pulumi.get(self, "finding_publishing_frequency")

    @property
    @pulumi.getter(name="serviceRole")
    def service_role(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the service-linked role that allows Macie to monitor and analyze data in AWS resources for the account.
        """
        return pulumi.get(self, "service_role")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Specifies the status for the account. To enable Amazon Macie and start all Macie activities for the account, set this value to `ENABLED`. Valid values are `ENABLED` or `PAUSED`.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        The date and time, in UTC and extended RFC 3339 format, of the most recent change to the status of the Macie account.
        """
        return pulumi.get(self, "updated_at")

