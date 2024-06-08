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

__all__ = ['HumanTaskUIArgs', 'HumanTaskUI']

@pulumi.input_type
class HumanTaskUIArgs:
    def __init__(__self__, *,
                 human_task_ui_name: pulumi.Input[str],
                 ui_template: pulumi.Input['HumanTaskUIUiTemplateArgs'],
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a HumanTaskUI resource.
        :param pulumi.Input[str] human_task_ui_name: The name of the Human Task UI.
        :param pulumi.Input['HumanTaskUIUiTemplateArgs'] ui_template: The Liquid template for the worker user interface. See UI Template below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "human_task_ui_name", human_task_ui_name)
        pulumi.set(__self__, "ui_template", ui_template)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="humanTaskUiName")
    def human_task_ui_name(self) -> pulumi.Input[str]:
        """
        The name of the Human Task UI.
        """
        return pulumi.get(self, "human_task_ui_name")

    @human_task_ui_name.setter
    def human_task_ui_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "human_task_ui_name", value)

    @property
    @pulumi.getter(name="uiTemplate")
    def ui_template(self) -> pulumi.Input['HumanTaskUIUiTemplateArgs']:
        """
        The Liquid template for the worker user interface. See UI Template below.
        """
        return pulumi.get(self, "ui_template")

    @ui_template.setter
    def ui_template(self, value: pulumi.Input['HumanTaskUIUiTemplateArgs']):
        pulumi.set(self, "ui_template", value)

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
class _HumanTaskUIState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 human_task_ui_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ui_template: Optional[pulumi.Input['HumanTaskUIUiTemplateArgs']] = None):
        """
        Input properties used for looking up and filtering HumanTaskUI resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Human Task UI.
        :param pulumi.Input[str] human_task_ui_name: The name of the Human Task UI.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input['HumanTaskUIUiTemplateArgs'] ui_template: The Liquid template for the worker user interface. See UI Template below.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if human_task_ui_name is not None:
            pulumi.set(__self__, "human_task_ui_name", human_task_ui_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if ui_template is not None:
            pulumi.set(__self__, "ui_template", ui_template)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Human Task UI.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="humanTaskUiName")
    def human_task_ui_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Human Task UI.
        """
        return pulumi.get(self, "human_task_ui_name")

    @human_task_ui_name.setter
    def human_task_ui_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "human_task_ui_name", value)

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
    @pulumi.getter(name="uiTemplate")
    def ui_template(self) -> Optional[pulumi.Input['HumanTaskUIUiTemplateArgs']]:
        """
        The Liquid template for the worker user interface. See UI Template below.
        """
        return pulumi.get(self, "ui_template")

    @ui_template.setter
    def ui_template(self, value: Optional[pulumi.Input['HumanTaskUIUiTemplateArgs']]):
        pulumi.set(self, "ui_template", value)


class HumanTaskUI(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 human_task_ui_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ui_template: Optional[pulumi.Input[pulumi.InputType['HumanTaskUIUiTemplateArgs']]] = None,
                 __props__=None):
        """
        Provides a SageMaker Human Task UI resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        example = aws.sagemaker.HumanTaskUI("example",
            human_task_ui_name="example",
            ui_template=aws.sagemaker.HumanTaskUIUiTemplateArgs(
                content=std.file(input="sagemaker-human-task-ui-template.html").result,
            ))
        ```

        ## Import

        Using `pulumi import`, import SageMaker Human Task UIs using the `human_task_ui_name`. For example:

        ```sh
        $ pulumi import aws:sagemaker/humanTaskUI:HumanTaskUI example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] human_task_ui_name: The name of the Human Task UI.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[pulumi.InputType['HumanTaskUIUiTemplateArgs']] ui_template: The Liquid template for the worker user interface. See UI Template below.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HumanTaskUIArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a SageMaker Human Task UI resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws
        import pulumi_std as std

        example = aws.sagemaker.HumanTaskUI("example",
            human_task_ui_name="example",
            ui_template=aws.sagemaker.HumanTaskUIUiTemplateArgs(
                content=std.file(input="sagemaker-human-task-ui-template.html").result,
            ))
        ```

        ## Import

        Using `pulumi import`, import SageMaker Human Task UIs using the `human_task_ui_name`. For example:

        ```sh
        $ pulumi import aws:sagemaker/humanTaskUI:HumanTaskUI example example
        ```

        :param str resource_name: The name of the resource.
        :param HumanTaskUIArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HumanTaskUIArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 human_task_ui_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ui_template: Optional[pulumi.Input[pulumi.InputType['HumanTaskUIUiTemplateArgs']]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HumanTaskUIArgs.__new__(HumanTaskUIArgs)

            if human_task_ui_name is None and not opts.urn:
                raise TypeError("Missing required property 'human_task_ui_name'")
            __props__.__dict__["human_task_ui_name"] = human_task_ui_name
            __props__.__dict__["tags"] = tags
            if ui_template is None and not opts.urn:
                raise TypeError("Missing required property 'ui_template'")
            __props__.__dict__["ui_template"] = ui_template
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(HumanTaskUI, __self__).__init__(
            'aws:sagemaker/humanTaskUI:HumanTaskUI',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            human_task_ui_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            ui_template: Optional[pulumi.Input[pulumi.InputType['HumanTaskUIUiTemplateArgs']]] = None) -> 'HumanTaskUI':
        """
        Get an existing HumanTaskUI resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Human Task UI.
        :param pulumi.Input[str] human_task_ui_name: The name of the Human Task UI.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[pulumi.InputType['HumanTaskUIUiTemplateArgs']] ui_template: The Liquid template for the worker user interface. See UI Template below.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HumanTaskUIState.__new__(_HumanTaskUIState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["human_task_ui_name"] = human_task_ui_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["ui_template"] = ui_template
        return HumanTaskUI(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Human Task UI.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="humanTaskUiName")
    def human_task_ui_name(self) -> pulumi.Output[str]:
        """
        The name of the Human Task UI.
        """
        return pulumi.get(self, "human_task_ui_name")

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
    @pulumi.getter(name="uiTemplate")
    def ui_template(self) -> pulumi.Output['outputs.HumanTaskUIUiTemplate']:
        """
        The Liquid template for the worker user interface. See UI Template below.
        """
        return pulumi.get(self, "ui_template")

