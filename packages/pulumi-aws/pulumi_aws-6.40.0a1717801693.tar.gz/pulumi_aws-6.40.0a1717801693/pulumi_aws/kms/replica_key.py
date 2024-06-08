# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ReplicaKeyArgs', 'ReplicaKey']

@pulumi.input_type
class ReplicaKeyArgs:
    def __init__(__self__, *,
                 primary_key_arn: pulumi.Input[str],
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ReplicaKey resource.
        :param pulumi.Input[str] primary_key_arn: The ARN of the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS Partition. You can create only one replica of a given primary key in each AWS Region.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
               The default value is `false`.
        :param pulumi.Input[int] deletion_window_in_days: The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
               If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
        :param pulumi.Input[str] description: A description of the KMS key.
        :param pulumi.Input[bool] enabled: Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. The default value is `true`.
        :param pulumi.Input[str] policy: The key policy to attach to the KMS key. If you do not specify a key policy, AWS KMS attaches the [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) to the KMS key.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the replica key. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "primary_key_arn", primary_key_arn)
        if bypass_policy_lockout_safety_check is not None:
            pulumi.set(__self__, "bypass_policy_lockout_safety_check", bypass_policy_lockout_safety_check)
        if deletion_window_in_days is not None:
            pulumi.set(__self__, "deletion_window_in_days", deletion_window_in_days)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="primaryKeyArn")
    def primary_key_arn(self) -> pulumi.Input[str]:
        """
        The ARN of the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS Partition. You can create only one replica of a given primary key in each AWS Region.
        """
        return pulumi.get(self, "primary_key_arn")

    @primary_key_arn.setter
    def primary_key_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "primary_key_arn", value)

    @property
    @pulumi.getter(name="bypassPolicyLockoutSafetyCheck")
    def bypass_policy_lockout_safety_check(self) -> Optional[pulumi.Input[bool]]:
        """
        A flag to indicate whether to bypass the key policy lockout safety check.
        Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
        For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        The default value is `false`.
        """
        return pulumi.get(self, "bypass_policy_lockout_safety_check")

    @bypass_policy_lockout_safety_check.setter
    def bypass_policy_lockout_safety_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bypass_policy_lockout_safety_check", value)

    @property
    @pulumi.getter(name="deletionWindowInDays")
    def deletion_window_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
        If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
        """
        return pulumi.get(self, "deletion_window_in_days")

    @deletion_window_in_days.setter
    def deletion_window_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "deletion_window_in_days", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the KMS key.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. The default value is `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The key policy to attach to the KMS key. If you do not specify a key policy, AWS KMS attaches the [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) to the KMS key.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the replica key. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ReplicaKeyState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 key_rotation_enabled: Optional[pulumi.Input[bool]] = None,
                 key_spec: Optional[pulumi.Input[str]] = None,
                 key_usage: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 primary_key_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering ReplicaKey resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the replica key. The key ARNs of related multi-Region keys differ only in the Region value.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
               The default value is `false`.
        :param pulumi.Input[int] deletion_window_in_days: The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
               If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
        :param pulumi.Input[str] description: A description of the KMS key.
        :param pulumi.Input[bool] enabled: Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. The default value is `true`.
        :param pulumi.Input[str] key_id: The key ID of the replica key. Related multi-Region keys have the same key ID.
        :param pulumi.Input[bool] key_rotation_enabled: A Boolean value that specifies whether key rotation is enabled. This is a shared property of multi-Region keys.
        :param pulumi.Input[str] key_spec: The type of key material in the KMS key. This is a shared property of multi-Region keys.
        :param pulumi.Input[str] key_usage: The [cryptographic operations](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations) for which you can use the KMS key. This is a shared property of multi-Region keys.
        :param pulumi.Input[str] policy: The key policy to attach to the KMS key. If you do not specify a key policy, AWS KMS attaches the [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) to the KMS key.
        :param pulumi.Input[str] primary_key_arn: The ARN of the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS Partition. You can create only one replica of a given primary key in each AWS Region.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the replica key. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if bypass_policy_lockout_safety_check is not None:
            pulumi.set(__self__, "bypass_policy_lockout_safety_check", bypass_policy_lockout_safety_check)
        if deletion_window_in_days is not None:
            pulumi.set(__self__, "deletion_window_in_days", deletion_window_in_days)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if key_id is not None:
            pulumi.set(__self__, "key_id", key_id)
        if key_rotation_enabled is not None:
            pulumi.set(__self__, "key_rotation_enabled", key_rotation_enabled)
        if key_spec is not None:
            pulumi.set(__self__, "key_spec", key_spec)
        if key_usage is not None:
            pulumi.set(__self__, "key_usage", key_usage)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if primary_key_arn is not None:
            pulumi.set(__self__, "primary_key_arn", primary_key_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the replica key. The key ARNs of related multi-Region keys differ only in the Region value.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="bypassPolicyLockoutSafetyCheck")
    def bypass_policy_lockout_safety_check(self) -> Optional[pulumi.Input[bool]]:
        """
        A flag to indicate whether to bypass the key policy lockout safety check.
        Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
        For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        The default value is `false`.
        """
        return pulumi.get(self, "bypass_policy_lockout_safety_check")

    @bypass_policy_lockout_safety_check.setter
    def bypass_policy_lockout_safety_check(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "bypass_policy_lockout_safety_check", value)

    @property
    @pulumi.getter(name="deletionWindowInDays")
    def deletion_window_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
        If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
        """
        return pulumi.get(self, "deletion_window_in_days")

    @deletion_window_in_days.setter
    def deletion_window_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "deletion_window_in_days", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the KMS key.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. The default value is `true`.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The key ID of the replica key. Related multi-Region keys have the same key ID.
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_id", value)

    @property
    @pulumi.getter(name="keyRotationEnabled")
    def key_rotation_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        A Boolean value that specifies whether key rotation is enabled. This is a shared property of multi-Region keys.
        """
        return pulumi.get(self, "key_rotation_enabled")

    @key_rotation_enabled.setter
    def key_rotation_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "key_rotation_enabled", value)

    @property
    @pulumi.getter(name="keySpec")
    def key_spec(self) -> Optional[pulumi.Input[str]]:
        """
        The type of key material in the KMS key. This is a shared property of multi-Region keys.
        """
        return pulumi.get(self, "key_spec")

    @key_spec.setter
    def key_spec(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_spec", value)

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> Optional[pulumi.Input[str]]:
        """
        The [cryptographic operations](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations) for which you can use the KMS key. This is a shared property of multi-Region keys.
        """
        return pulumi.get(self, "key_usage")

    @key_usage.setter
    def key_usage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_usage", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        The key policy to attach to the KMS key. If you do not specify a key policy, AWS KMS attaches the [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) to the KMS key.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="primaryKeyArn")
    def primary_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS Partition. You can create only one replica of a given primary key in each AWS Region.
        """
        return pulumi.get(self, "primary_key_arn")

    @primary_key_arn.setter
    def primary_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "primary_key_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the replica key. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class ReplicaKey(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 primary_key_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Manages a KMS multi-Region replica key.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        primary = aws.kms.Key("primary",
            description="Multi-Region primary key",
            deletion_window_in_days=30,
            multi_region=True)
        replica = aws.kms.ReplicaKey("replica",
            description="Multi-Region replica key",
            deletion_window_in_days=7,
            primary_key_arn=primary.arn)
        ```

        ## Import

        Using `pulumi import`, import KMS multi-Region replica keys using the `id`. For example:

        ```sh
        $ pulumi import aws:kms/replicaKey:ReplicaKey example 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
               The default value is `false`.
        :param pulumi.Input[int] deletion_window_in_days: The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
               If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
        :param pulumi.Input[str] description: A description of the KMS key.
        :param pulumi.Input[bool] enabled: Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. The default value is `true`.
        :param pulumi.Input[str] policy: The key policy to attach to the KMS key. If you do not specify a key policy, AWS KMS attaches the [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) to the KMS key.
        :param pulumi.Input[str] primary_key_arn: The ARN of the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS Partition. You can create only one replica of a given primary key in each AWS Region.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the replica key. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicaKeyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a KMS multi-Region replica key.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        primary = aws.kms.Key("primary",
            description="Multi-Region primary key",
            deletion_window_in_days=30,
            multi_region=True)
        replica = aws.kms.ReplicaKey("replica",
            description="Multi-Region replica key",
            deletion_window_in_days=7,
            primary_key_arn=primary.arn)
        ```

        ## Import

        Using `pulumi import`, import KMS multi-Region replica keys using the `id`. For example:

        ```sh
        $ pulumi import aws:kms/replicaKey:ReplicaKey example 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param ReplicaKeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicaKeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 primary_key_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ReplicaKeyArgs.__new__(ReplicaKeyArgs)

            __props__.__dict__["bypass_policy_lockout_safety_check"] = bypass_policy_lockout_safety_check
            __props__.__dict__["deletion_window_in_days"] = deletion_window_in_days
            __props__.__dict__["description"] = description
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["policy"] = policy
            if primary_key_arn is None and not opts.urn:
                raise TypeError("Missing required property 'primary_key_arn'")
            __props__.__dict__["primary_key_arn"] = primary_key_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["key_id"] = None
            __props__.__dict__["key_rotation_enabled"] = None
            __props__.__dict__["key_spec"] = None
            __props__.__dict__["key_usage"] = None
            __props__.__dict__["tags_all"] = None
        super(ReplicaKey, __self__).__init__(
            'aws:kms/replicaKey:ReplicaKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            bypass_policy_lockout_safety_check: Optional[pulumi.Input[bool]] = None,
            deletion_window_in_days: Optional[pulumi.Input[int]] = None,
            description: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            key_id: Optional[pulumi.Input[str]] = None,
            key_rotation_enabled: Optional[pulumi.Input[bool]] = None,
            key_spec: Optional[pulumi.Input[str]] = None,
            key_usage: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None,
            primary_key_arn: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'ReplicaKey':
        """
        Get an existing ReplicaKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the replica key. The key ARNs of related multi-Region keys differ only in the Region value.
        :param pulumi.Input[bool] bypass_policy_lockout_safety_check: A flag to indicate whether to bypass the key policy lockout safety check.
               Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
               For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
               The default value is `false`.
        :param pulumi.Input[int] deletion_window_in_days: The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
               If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
        :param pulumi.Input[str] description: A description of the KMS key.
        :param pulumi.Input[bool] enabled: Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. The default value is `true`.
        :param pulumi.Input[str] key_id: The key ID of the replica key. Related multi-Region keys have the same key ID.
        :param pulumi.Input[bool] key_rotation_enabled: A Boolean value that specifies whether key rotation is enabled. This is a shared property of multi-Region keys.
        :param pulumi.Input[str] key_spec: The type of key material in the KMS key. This is a shared property of multi-Region keys.
        :param pulumi.Input[str] key_usage: The [cryptographic operations](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations) for which you can use the KMS key. This is a shared property of multi-Region keys.
        :param pulumi.Input[str] policy: The key policy to attach to the KMS key. If you do not specify a key policy, AWS KMS attaches the [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) to the KMS key.
        :param pulumi.Input[str] primary_key_arn: The ARN of the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS Partition. You can create only one replica of a given primary key in each AWS Region.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the replica key. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ReplicaKeyState.__new__(_ReplicaKeyState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["bypass_policy_lockout_safety_check"] = bypass_policy_lockout_safety_check
        __props__.__dict__["deletion_window_in_days"] = deletion_window_in_days
        __props__.__dict__["description"] = description
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["key_id"] = key_id
        __props__.__dict__["key_rotation_enabled"] = key_rotation_enabled
        __props__.__dict__["key_spec"] = key_spec
        __props__.__dict__["key_usage"] = key_usage
        __props__.__dict__["policy"] = policy
        __props__.__dict__["primary_key_arn"] = primary_key_arn
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return ReplicaKey(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the replica key. The key ARNs of related multi-Region keys differ only in the Region value.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="bypassPolicyLockoutSafetyCheck")
    def bypass_policy_lockout_safety_check(self) -> pulumi.Output[Optional[bool]]:
        """
        A flag to indicate whether to bypass the key policy lockout safety check.
        Setting this value to true increases the risk that the KMS key becomes unmanageable. Do not set this value to true indiscriminately.
        For more information, refer to the scenario in the [Default Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default-allow-root-enable-iam) section in the _AWS Key Management Service Developer Guide_.
        The default value is `false`.
        """
        return pulumi.get(self, "bypass_policy_lockout_safety_check")

    @property
    @pulumi.getter(name="deletionWindowInDays")
    def deletion_window_in_days(self) -> pulumi.Output[Optional[int]]:
        """
        The waiting period, specified in number of days. After the waiting period ends, AWS KMS deletes the KMS key.
        If you specify a value, it must be between `7` and `30`, inclusive. If you do not specify a value, it defaults to `30`.
        """
        return pulumi.get(self, "deletion_window_in_days")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the KMS key.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the replica key is enabled. Disabled KMS keys cannot be used in cryptographic operations. The default value is `true`.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Output[str]:
        """
        The key ID of the replica key. Related multi-Region keys have the same key ID.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keyRotationEnabled")
    def key_rotation_enabled(self) -> pulumi.Output[bool]:
        """
        A Boolean value that specifies whether key rotation is enabled. This is a shared property of multi-Region keys.
        """
        return pulumi.get(self, "key_rotation_enabled")

    @property
    @pulumi.getter(name="keySpec")
    def key_spec(self) -> pulumi.Output[str]:
        """
        The type of key material in the KMS key. This is a shared property of multi-Region keys.
        """
        return pulumi.get(self, "key_spec")

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> pulumi.Output[str]:
        """
        The [cryptographic operations](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#cryptographic-operations) for which you can use the KMS key. This is a shared property of multi-Region keys.
        """
        return pulumi.get(self, "key_usage")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The key policy to attach to the KMS key. If you do not specify a key policy, AWS KMS attaches the [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html#key-policy-default) to the KMS key.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="primaryKeyArn")
    def primary_key_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the multi-Region primary key to replicate. The primary key must be in a different AWS Region of the same AWS Partition. You can create only one replica of a given primary key in each AWS Region.
        """
        return pulumi.get(self, "primary_key_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the replica key. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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

