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

__all__ = ['WebhookArgs', 'Webhook']

@pulumi.input_type
class WebhookArgs:
    def __init__(__self__, *,
                 authentication: pulumi.Input[str],
                 filters: pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]],
                 target_action: pulumi.Input[str],
                 target_pipeline: pulumi.Input[str],
                 authentication_configuration: Optional[pulumi.Input['WebhookAuthenticationConfigurationArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Webhook resource.
        :param pulumi.Input[str] authentication: The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        :param pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]] filters: One or more `filter` blocks. Filter blocks are documented below.
        :param pulumi.Input[str] target_action: The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        :param pulumi.Input[str] target_pipeline: The name of the pipeline.
        :param pulumi.Input['WebhookAuthenticationConfigurationArgs'] authentication_configuration: An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        :param pulumi.Input[str] name: The name of the webhook.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "authentication", authentication)
        pulumi.set(__self__, "filters", filters)
        pulumi.set(__self__, "target_action", target_action)
        pulumi.set(__self__, "target_pipeline", target_pipeline)
        if authentication_configuration is not None:
            pulumi.set(__self__, "authentication_configuration", authentication_configuration)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def authentication(self) -> pulumi.Input[str]:
        """
        The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: pulumi.Input[str]):
        pulumi.set(self, "authentication", value)

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]]:
        """
        One or more `filter` blocks. Filter blocks are documented below.
        """
        return pulumi.get(self, "filters")

    @filters.setter
    def filters(self, value: pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]]):
        pulumi.set(self, "filters", value)

    @property
    @pulumi.getter(name="targetAction")
    def target_action(self) -> pulumi.Input[str]:
        """
        The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        """
        return pulumi.get(self, "target_action")

    @target_action.setter
    def target_action(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_action", value)

    @property
    @pulumi.getter(name="targetPipeline")
    def target_pipeline(self) -> pulumi.Input[str]:
        """
        The name of the pipeline.
        """
        return pulumi.get(self, "target_pipeline")

    @target_pipeline.setter
    def target_pipeline(self, value: pulumi.Input[str]):
        pulumi.set(self, "target_pipeline", value)

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> Optional[pulumi.Input['WebhookAuthenticationConfigurationArgs']]:
        """
        An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        """
        return pulumi.get(self, "authentication_configuration")

    @authentication_configuration.setter
    def authentication_configuration(self, value: Optional[pulumi.Input['WebhookAuthenticationConfigurationArgs']]):
        pulumi.set(self, "authentication_configuration", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the webhook.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _WebhookState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 authentication_configuration: Optional[pulumi.Input['WebhookAuthenticationConfigurationArgs']] = None,
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_action: Optional[pulumi.Input[str]] = None,
                 target_pipeline: Optional[pulumi.Input[str]] = None,
                 url: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Webhook resources.
        :param pulumi.Input[str] arn: The CodePipeline webhook's ARN.
        :param pulumi.Input[str] authentication: The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        :param pulumi.Input['WebhookAuthenticationConfigurationArgs'] authentication_configuration: An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        :param pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]] filters: One or more `filter` blocks. Filter blocks are documented below.
        :param pulumi.Input[str] name: The name of the webhook.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] target_action: The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        :param pulumi.Input[str] target_pipeline: The name of the pipeline.
        :param pulumi.Input[str] url: The CodePipeline webhook's URL. POST events to this endpoint to trigger the target.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if authentication is not None:
            pulumi.set(__self__, "authentication", authentication)
        if authentication_configuration is not None:
            pulumi.set(__self__, "authentication_configuration", authentication_configuration)
        if filters is not None:
            pulumi.set(__self__, "filters", filters)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if target_action is not None:
            pulumi.set(__self__, "target_action", target_action)
        if target_pipeline is not None:
            pulumi.set(__self__, "target_pipeline", target_pipeline)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The CodePipeline webhook's ARN.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def authentication(self) -> Optional[pulumi.Input[str]]:
        """
        The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        """
        return pulumi.get(self, "authentication")

    @authentication.setter
    def authentication(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "authentication", value)

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> Optional[pulumi.Input['WebhookAuthenticationConfigurationArgs']]:
        """
        An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        """
        return pulumi.get(self, "authentication_configuration")

    @authentication_configuration.setter
    def authentication_configuration(self, value: Optional[pulumi.Input['WebhookAuthenticationConfigurationArgs']]):
        pulumi.set(self, "authentication_configuration", value)

    @property
    @pulumi.getter
    def filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]]]:
        """
        One or more `filter` blocks. Filter blocks are documented below.
        """
        return pulumi.get(self, "filters")

    @filters.setter
    def filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['WebhookFilterArgs']]]]):
        pulumi.set(self, "filters", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the webhook.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="targetAction")
    def target_action(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        """
        return pulumi.get(self, "target_action")

    @target_action.setter
    def target_action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_action", value)

    @property
    @pulumi.getter(name="targetPipeline")
    def target_pipeline(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the pipeline.
        """
        return pulumi.get(self, "target_pipeline")

    @target_pipeline.setter
    def target_pipeline(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_pipeline", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        """
        The CodePipeline webhook's URL. POST events to this endpoint to trigger the target.
        """
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)


class Webhook(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 authentication_configuration: Optional[pulumi.Input[pulumi.InputType['WebhookAuthenticationConfigurationArgs']]] = None,
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookFilterArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_action: Optional[pulumi.Input[str]] = None,
                 target_pipeline: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a CodePipeline Webhook.

        ## Import

        Using `pulumi import`, import CodePipeline Webhooks using their ARN. For example:

        ```sh
        $ pulumi import aws:codepipeline/webhook:Webhook example arn:aws:codepipeline:us-west-2:123456789012:webhook:example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authentication: The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        :param pulumi.Input[pulumi.InputType['WebhookAuthenticationConfigurationArgs']] authentication_configuration: An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookFilterArgs']]]] filters: One or more `filter` blocks. Filter blocks are documented below.
        :param pulumi.Input[str] name: The name of the webhook.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] target_action: The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        :param pulumi.Input[str] target_pipeline: The name of the pipeline.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebhookArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CodePipeline Webhook.

        ## Import

        Using `pulumi import`, import CodePipeline Webhooks using their ARN. For example:

        ```sh
        $ pulumi import aws:codepipeline/webhook:Webhook example arn:aws:codepipeline:us-west-2:123456789012:webhook:example
        ```

        :param str resource_name: The name of the resource.
        :param WebhookArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebhookArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authentication: Optional[pulumi.Input[str]] = None,
                 authentication_configuration: Optional[pulumi.Input[pulumi.InputType['WebhookAuthenticationConfigurationArgs']]] = None,
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookFilterArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_action: Optional[pulumi.Input[str]] = None,
                 target_pipeline: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = WebhookArgs.__new__(WebhookArgs)

            if authentication is None and not opts.urn:
                raise TypeError("Missing required property 'authentication'")
            __props__.__dict__["authentication"] = authentication
            __props__.__dict__["authentication_configuration"] = authentication_configuration
            if filters is None and not opts.urn:
                raise TypeError("Missing required property 'filters'")
            __props__.__dict__["filters"] = filters
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            if target_action is None and not opts.urn:
                raise TypeError("Missing required property 'target_action'")
            __props__.__dict__["target_action"] = target_action
            if target_pipeline is None and not opts.urn:
                raise TypeError("Missing required property 'target_pipeline'")
            __props__.__dict__["target_pipeline"] = target_pipeline
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["url"] = None
        super(Webhook, __self__).__init__(
            'aws:codepipeline/webhook:Webhook',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            authentication: Optional[pulumi.Input[str]] = None,
            authentication_configuration: Optional[pulumi.Input[pulumi.InputType['WebhookAuthenticationConfigurationArgs']]] = None,
            filters: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookFilterArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            target_action: Optional[pulumi.Input[str]] = None,
            target_pipeline: Optional[pulumi.Input[str]] = None,
            url: Optional[pulumi.Input[str]] = None) -> 'Webhook':
        """
        Get an existing Webhook resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The CodePipeline webhook's ARN.
        :param pulumi.Input[str] authentication: The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        :param pulumi.Input[pulumi.InputType['WebhookAuthenticationConfigurationArgs']] authentication_configuration: An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['WebhookFilterArgs']]]] filters: One or more `filter` blocks. Filter blocks are documented below.
        :param pulumi.Input[str] name: The name of the webhook.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] target_action: The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        :param pulumi.Input[str] target_pipeline: The name of the pipeline.
        :param pulumi.Input[str] url: The CodePipeline webhook's URL. POST events to this endpoint to trigger the target.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _WebhookState.__new__(_WebhookState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["authentication"] = authentication
        __props__.__dict__["authentication_configuration"] = authentication_configuration
        __props__.__dict__["filters"] = filters
        __props__.__dict__["name"] = name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["target_action"] = target_action
        __props__.__dict__["target_pipeline"] = target_pipeline
        __props__.__dict__["url"] = url
        return Webhook(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The CodePipeline webhook's ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def authentication(self) -> pulumi.Output[str]:
        """
        The type of authentication  to use. One of `IP`, `GITHUB_HMAC`, or `UNAUTHENTICATED`.
        """
        return pulumi.get(self, "authentication")

    @property
    @pulumi.getter(name="authenticationConfiguration")
    def authentication_configuration(self) -> pulumi.Output[Optional['outputs.WebhookAuthenticationConfiguration']]:
        """
        An `auth` block. Required for `IP` and `GITHUB_HMAC`. Auth blocks are documented below.
        """
        return pulumi.get(self, "authentication_configuration")

    @property
    @pulumi.getter
    def filters(self) -> pulumi.Output[Sequence['outputs.WebhookFilter']]:
        """
        One or more `filter` blocks. Filter blocks are documented below.
        """
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the webhook.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="targetAction")
    def target_action(self) -> pulumi.Output[str]:
        """
        The name of the action in a pipeline you want to connect to the webhook. The action must be from the source (first) stage of the pipeline.
        """
        return pulumi.get(self, "target_action")

    @property
    @pulumi.getter(name="targetPipeline")
    def target_pipeline(self) -> pulumi.Output[str]:
        """
        The name of the pipeline.
        """
        return pulumi.get(self, "target_pipeline")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The CodePipeline webhook's URL. POST events to this endpoint to trigger the target.
        """
        return pulumi.get(self, "url")

