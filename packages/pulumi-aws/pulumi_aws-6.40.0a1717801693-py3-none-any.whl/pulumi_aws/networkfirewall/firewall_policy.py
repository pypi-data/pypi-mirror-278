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

__all__ = ['FirewallPolicyArgs', 'FirewallPolicy']

@pulumi.input_type
class FirewallPolicyArgs:
    def __init__(__self__, *,
                 firewall_policy: pulumi.Input['FirewallPolicyFirewallPolicyArgs'],
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_configuration: Optional[pulumi.Input['FirewallPolicyEncryptionConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a FirewallPolicy resource.
        :param pulumi.Input['FirewallPolicyFirewallPolicyArgs'] firewall_policy: A configuration block describing the rule groups and policy actions to use in the firewall policy. See Firewall Policy below for details.
        :param pulumi.Input[str] description: A friendly description of the firewall policy.
        :param pulumi.Input['FirewallPolicyEncryptionConfigurationArgs'] encryption_configuration: KMS encryption configuration settings. See Encryption Configuration below for details.
        :param pulumi.Input[str] name: A friendly name of the firewall policy.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "firewall_policy", firewall_policy)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encryption_configuration is not None:
            pulumi.set(__self__, "encryption_configuration", encryption_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="firewallPolicy")
    def firewall_policy(self) -> pulumi.Input['FirewallPolicyFirewallPolicyArgs']:
        """
        A configuration block describing the rule groups and policy actions to use in the firewall policy. See Firewall Policy below for details.
        """
        return pulumi.get(self, "firewall_policy")

    @firewall_policy.setter
    def firewall_policy(self, value: pulumi.Input['FirewallPolicyFirewallPolicyArgs']):
        pulumi.set(self, "firewall_policy", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A friendly description of the firewall policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> Optional[pulumi.Input['FirewallPolicyEncryptionConfigurationArgs']]:
        """
        KMS encryption configuration settings. See Encryption Configuration below for details.
        """
        return pulumi.get(self, "encryption_configuration")

    @encryption_configuration.setter
    def encryption_configuration(self, value: Optional[pulumi.Input['FirewallPolicyEncryptionConfigurationArgs']]):
        pulumi.set(self, "encryption_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A friendly name of the firewall policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _FirewallPolicyState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_configuration: Optional[pulumi.Input['FirewallPolicyEncryptionConfigurationArgs']] = None,
                 firewall_policy: Optional[pulumi.Input['FirewallPolicyFirewallPolicyArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 update_token: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering FirewallPolicy resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) that identifies the firewall policy.
        :param pulumi.Input[str] description: A friendly description of the firewall policy.
        :param pulumi.Input['FirewallPolicyEncryptionConfigurationArgs'] encryption_configuration: KMS encryption configuration settings. See Encryption Configuration below for details.
        :param pulumi.Input['FirewallPolicyFirewallPolicyArgs'] firewall_policy: A configuration block describing the rule groups and policy actions to use in the firewall policy. See Firewall Policy below for details.
        :param pulumi.Input[str] name: A friendly name of the firewall policy.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] update_token: A string token used when updating a firewall policy.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if encryption_configuration is not None:
            pulumi.set(__self__, "encryption_configuration", encryption_configuration)
        if firewall_policy is not None:
            pulumi.set(__self__, "firewall_policy", firewall_policy)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if update_token is not None:
            pulumi.set(__self__, "update_token", update_token)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) that identifies the firewall policy.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A friendly description of the firewall policy.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> Optional[pulumi.Input['FirewallPolicyEncryptionConfigurationArgs']]:
        """
        KMS encryption configuration settings. See Encryption Configuration below for details.
        """
        return pulumi.get(self, "encryption_configuration")

    @encryption_configuration.setter
    def encryption_configuration(self, value: Optional[pulumi.Input['FirewallPolicyEncryptionConfigurationArgs']]):
        pulumi.set(self, "encryption_configuration", value)

    @property
    @pulumi.getter(name="firewallPolicy")
    def firewall_policy(self) -> Optional[pulumi.Input['FirewallPolicyFirewallPolicyArgs']]:
        """
        A configuration block describing the rule groups and policy actions to use in the firewall policy. See Firewall Policy below for details.
        """
        return pulumi.get(self, "firewall_policy")

    @firewall_policy.setter
    def firewall_policy(self, value: Optional[pulumi.Input['FirewallPolicyFirewallPolicyArgs']]):
        pulumi.set(self, "firewall_policy", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A friendly name of the firewall policy.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="updateToken")
    def update_token(self) -> Optional[pulumi.Input[str]]:
        """
        A string token used when updating a firewall policy.
        """
        return pulumi.get(self, "update_token")

    @update_token.setter
    def update_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update_token", value)


class FirewallPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_configuration: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyEncryptionConfigurationArgs']]] = None,
                 firewall_policy: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyFirewallPolicyArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides an AWS Network Firewall Firewall Policy Resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkfirewall.FirewallPolicy("example",
            name="example",
            firewall_policy=aws.networkfirewall.FirewallPolicyFirewallPolicyArgs(
                stateless_default_actions=["aws:pass"],
                stateless_fragment_default_actions=["aws:drop"],
                stateless_rule_group_references=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessRuleGroupReferenceArgs(
                    priority=1,
                    resource_arn=example_aws_networkfirewall_rule_group["arn"],
                )],
                tls_inspection_configuration_arn="arn:aws:network-firewall:REGION:ACCT:tls-configuration/example",
            ),
            tags={
                "Tag1": "Value1",
                "Tag2": "Value2",
            })
        ```

        ## Policy with a HOME_NET Override

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkfirewall.FirewallPolicy("example",
            name="example",
            firewall_policy=aws.networkfirewall.FirewallPolicyFirewallPolicyArgs(
                policy_variables=aws.networkfirewall.FirewallPolicyFirewallPolicyPolicyVariablesArgs(
                    rule_variables=[aws.networkfirewall.FirewallPolicyFirewallPolicyPolicyVariablesRuleVariableArgs(
                        key="HOME_NET",
                        ip_set=aws.networkfirewall.FirewallPolicyFirewallPolicyPolicyVariablesRuleVariableIpSetArgs(
                            definitions=[
                                "10.0.0.0/16",
                                "10.1.0.0/24",
                            ],
                        ),
                    )],
                ),
                stateless_default_actions=["aws:pass"],
                stateless_fragment_default_actions=["aws:drop"],
                stateless_rule_group_references=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessRuleGroupReferenceArgs(
                    priority=1,
                    resource_arn=example_aws_networkfirewall_rule_group["arn"],
                )],
            ),
            tags={
                "Tag1": "Value1",
                "Tag2": "Value2",
            })
        ```

        ## Policy with a Custom Action for Stateless Inspection

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.networkfirewall.FirewallPolicy("test",
            name="example",
            firewall_policy=aws.networkfirewall.FirewallPolicyFirewallPolicyArgs(
                stateless_default_actions=[
                    "aws:pass",
                    "ExampleCustomAction",
                ],
                stateless_fragment_default_actions=["aws:drop"],
                stateless_custom_actions=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionArgs(
                    action_definition=aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionActionDefinitionArgs(
                        publish_metric_action=aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionActionDefinitionPublishMetricActionArgs(
                            dimensions=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionActionDefinitionPublishMetricActionDimensionArgs(
                                value="1",
                            )],
                        ),
                    ),
                    action_name="ExampleCustomAction",
                )],
            ))
        ```

        ## Import

        Using `pulumi import`, import Network Firewall Policies using their `arn`. For example:

        ```sh
        $ pulumi import aws:networkfirewall/firewallPolicy:FirewallPolicy example arn:aws:network-firewall:us-west-1:123456789012:firewall-policy/example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A friendly description of the firewall policy.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyEncryptionConfigurationArgs']] encryption_configuration: KMS encryption configuration settings. See Encryption Configuration below for details.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyFirewallPolicyArgs']] firewall_policy: A configuration block describing the rule groups and policy actions to use in the firewall policy. See Firewall Policy below for details.
        :param pulumi.Input[str] name: A friendly name of the firewall policy.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FirewallPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an AWS Network Firewall Firewall Policy Resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkfirewall.FirewallPolicy("example",
            name="example",
            firewall_policy=aws.networkfirewall.FirewallPolicyFirewallPolicyArgs(
                stateless_default_actions=["aws:pass"],
                stateless_fragment_default_actions=["aws:drop"],
                stateless_rule_group_references=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessRuleGroupReferenceArgs(
                    priority=1,
                    resource_arn=example_aws_networkfirewall_rule_group["arn"],
                )],
                tls_inspection_configuration_arn="arn:aws:network-firewall:REGION:ACCT:tls-configuration/example",
            ),
            tags={
                "Tag1": "Value1",
                "Tag2": "Value2",
            })
        ```

        ## Policy with a HOME_NET Override

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.networkfirewall.FirewallPolicy("example",
            name="example",
            firewall_policy=aws.networkfirewall.FirewallPolicyFirewallPolicyArgs(
                policy_variables=aws.networkfirewall.FirewallPolicyFirewallPolicyPolicyVariablesArgs(
                    rule_variables=[aws.networkfirewall.FirewallPolicyFirewallPolicyPolicyVariablesRuleVariableArgs(
                        key="HOME_NET",
                        ip_set=aws.networkfirewall.FirewallPolicyFirewallPolicyPolicyVariablesRuleVariableIpSetArgs(
                            definitions=[
                                "10.0.0.0/16",
                                "10.1.0.0/24",
                            ],
                        ),
                    )],
                ),
                stateless_default_actions=["aws:pass"],
                stateless_fragment_default_actions=["aws:drop"],
                stateless_rule_group_references=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessRuleGroupReferenceArgs(
                    priority=1,
                    resource_arn=example_aws_networkfirewall_rule_group["arn"],
                )],
            ),
            tags={
                "Tag1": "Value1",
                "Tag2": "Value2",
            })
        ```

        ## Policy with a Custom Action for Stateless Inspection

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.networkfirewall.FirewallPolicy("test",
            name="example",
            firewall_policy=aws.networkfirewall.FirewallPolicyFirewallPolicyArgs(
                stateless_default_actions=[
                    "aws:pass",
                    "ExampleCustomAction",
                ],
                stateless_fragment_default_actions=["aws:drop"],
                stateless_custom_actions=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionArgs(
                    action_definition=aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionActionDefinitionArgs(
                        publish_metric_action=aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionActionDefinitionPublishMetricActionArgs(
                            dimensions=[aws.networkfirewall.FirewallPolicyFirewallPolicyStatelessCustomActionActionDefinitionPublishMetricActionDimensionArgs(
                                value="1",
                            )],
                        ),
                    ),
                    action_name="ExampleCustomAction",
                )],
            ))
        ```

        ## Import

        Using `pulumi import`, import Network Firewall Policies using their `arn`. For example:

        ```sh
        $ pulumi import aws:networkfirewall/firewallPolicy:FirewallPolicy example arn:aws:network-firewall:us-west-1:123456789012:firewall-policy/example
        ```

        :param str resource_name: The name of the resource.
        :param FirewallPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FirewallPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 encryption_configuration: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyEncryptionConfigurationArgs']]] = None,
                 firewall_policy: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyFirewallPolicyArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FirewallPolicyArgs.__new__(FirewallPolicyArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["encryption_configuration"] = encryption_configuration
            if firewall_policy is None and not opts.urn:
                raise TypeError("Missing required property 'firewall_policy'")
            __props__.__dict__["firewall_policy"] = firewall_policy
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["update_token"] = None
        super(FirewallPolicy, __self__).__init__(
            'aws:networkfirewall/firewallPolicy:FirewallPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            encryption_configuration: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyEncryptionConfigurationArgs']]] = None,
            firewall_policy: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyFirewallPolicyArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            update_token: Optional[pulumi.Input[str]] = None) -> 'FirewallPolicy':
        """
        Get an existing FirewallPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) that identifies the firewall policy.
        :param pulumi.Input[str] description: A friendly description of the firewall policy.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyEncryptionConfigurationArgs']] encryption_configuration: KMS encryption configuration settings. See Encryption Configuration below for details.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyFirewallPolicyArgs']] firewall_policy: A configuration block describing the rule groups and policy actions to use in the firewall policy. See Firewall Policy below for details.
        :param pulumi.Input[str] name: A friendly name of the firewall policy.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] update_token: A string token used when updating a firewall policy.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FirewallPolicyState.__new__(_FirewallPolicyState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["description"] = description
        __props__.__dict__["encryption_configuration"] = encryption_configuration
        __props__.__dict__["firewall_policy"] = firewall_policy
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["update_token"] = update_token
        return FirewallPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) that identifies the firewall policy.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A friendly description of the firewall policy.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="encryptionConfiguration")
    def encryption_configuration(self) -> pulumi.Output[Optional['outputs.FirewallPolicyEncryptionConfiguration']]:
        """
        KMS encryption configuration settings. See Encryption Configuration below for details.
        """
        return pulumi.get(self, "encryption_configuration")

    @property
    @pulumi.getter(name="firewallPolicy")
    def firewall_policy(self) -> pulumi.Output['outputs.FirewallPolicyFirewallPolicy']:
        """
        A configuration block describing the rule groups and policy actions to use in the firewall policy. See Firewall Policy below for details.
        """
        return pulumi.get(self, "firewall_policy")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A friendly name of the firewall policy.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of resource tags to associate with the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="updateToken")
    def update_token(self) -> pulumi.Output[str]:
        """
        A string token used when updating a firewall policy.
        """
        return pulumi.get(self, "update_token")

