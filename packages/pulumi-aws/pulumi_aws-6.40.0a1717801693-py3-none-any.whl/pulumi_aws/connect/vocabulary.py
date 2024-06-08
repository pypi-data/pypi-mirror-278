# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VocabularyArgs', 'Vocabulary']

@pulumi.input_type
class VocabularyArgs:
    def __init__(__self__, *,
                 content: pulumi.Input[str],
                 instance_id: pulumi.Input[str],
                 language_code: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Vocabulary resource.
        :param pulumi.Input[str] content: The content of the custom vocabulary in plain-text format with a table of values. Each row in the table represents a word or a phrase, described with Phrase, IPA, SoundsLike, and DisplayAs fields. Separate the fields with TAB characters. For more information, see [Create a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html#create-vocabulary-table). Minimum length of `1`. Maximum length of `60000`.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] language_code: The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-whatis.html). Valid Values are `ar-AE`, `de-CH`, `de-DE`, `en-AB`, `en-AU`, `en-GB`, `en-IE`, `en-IN`, `en-US`, `en-WL`, `es-ES`, `es-US`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN`.
        :param pulumi.Input[str] name: A unique name of the custom vocabulary. Must not be more than 140 characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the vocabulary. If configured with a provider
               `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "content", content)
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "language_code", language_code)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def content(self) -> pulumi.Input[str]:
        """
        The content of the custom vocabulary in plain-text format with a table of values. Each row in the table represents a word or a phrase, described with Phrase, IPA, SoundsLike, and DisplayAs fields. Separate the fields with TAB characters. For more information, see [Create a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html#create-vocabulary-table). Minimum length of `1`. Maximum length of `60000`.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: pulumi.Input[str]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="languageCode")
    def language_code(self) -> pulumi.Input[str]:
        """
        The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-whatis.html). Valid Values are `ar-AE`, `de-CH`, `de-DE`, `en-AB`, `en-AU`, `en-GB`, `en-IE`, `en-IN`, `en-US`, `en-WL`, `es-ES`, `es-US`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN`.
        """
        return pulumi.get(self, "language_code")

    @language_code.setter
    def language_code(self, value: pulumi.Input[str]):
        pulumi.set(self, "language_code", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A unique name of the custom vocabulary. Must not be more than 140 characters.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags to apply to the vocabulary. If configured with a provider
        `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _VocabularyState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 failure_reason: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 language_code: Optional[pulumi.Input[str]] = None,
                 last_modified_time: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 state: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 vocabulary_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Vocabulary resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the vocabulary.
        :param pulumi.Input[str] content: The content of the custom vocabulary in plain-text format with a table of values. Each row in the table represents a word or a phrase, described with Phrase, IPA, SoundsLike, and DisplayAs fields. Separate the fields with TAB characters. For more information, see [Create a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html#create-vocabulary-table). Minimum length of `1`. Maximum length of `60000`.
        :param pulumi.Input[str] failure_reason: The reason why the custom vocabulary was not created.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] language_code: The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-whatis.html). Valid Values are `ar-AE`, `de-CH`, `de-DE`, `en-AB`, `en-AU`, `en-GB`, `en-IE`, `en-IN`, `en-US`, `en-WL`, `es-ES`, `es-US`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN`.
        :param pulumi.Input[str] last_modified_time: The timestamp when the custom vocabulary was last modified.
        :param pulumi.Input[str] name: A unique name of the custom vocabulary. Must not be more than 140 characters.
        :param pulumi.Input[str] state: The current state of the custom vocabulary. Valid values are `CREATION_IN_PROGRESS`, `ACTIVE`, `CREATION_FAILED`, `DELETE_IN_PROGRESS`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the vocabulary. If configured with a provider
               `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] vocabulary_id: The identifier of the custom vocabulary.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if content is not None:
            pulumi.set(__self__, "content", content)
        if failure_reason is not None:
            pulumi.set(__self__, "failure_reason", failure_reason)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if language_code is not None:
            pulumi.set(__self__, "language_code", language_code)
        if last_modified_time is not None:
            pulumi.set(__self__, "last_modified_time", last_modified_time)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if state is not None:
            pulumi.set(__self__, "state", state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            warnings.warn("""Please use `tags` instead.""", DeprecationWarning)
            pulumi.log.warn("""tags_all is deprecated: Please use `tags` instead.""")
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if vocabulary_id is not None:
            pulumi.set(__self__, "vocabulary_id", vocabulary_id)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the vocabulary.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter
    def content(self) -> Optional[pulumi.Input[str]]:
        """
        The content of the custom vocabulary in plain-text format with a table of values. Each row in the table represents a word or a phrase, described with Phrase, IPA, SoundsLike, and DisplayAs fields. Separate the fields with TAB characters. For more information, see [Create a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html#create-vocabulary-table). Minimum length of `1`. Maximum length of `60000`.
        """
        return pulumi.get(self, "content")

    @content.setter
    def content(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "content", value)

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> Optional[pulumi.Input[str]]:
        """
        The reason why the custom vocabulary was not created.
        """
        return pulumi.get(self, "failure_reason")

    @failure_reason.setter
    def failure_reason(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "failure_reason", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="languageCode")
    def language_code(self) -> Optional[pulumi.Input[str]]:
        """
        The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-whatis.html). Valid Values are `ar-AE`, `de-CH`, `de-DE`, `en-AB`, `en-AU`, `en-GB`, `en-IE`, `en-IN`, `en-US`, `en-WL`, `es-ES`, `es-US`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN`.
        """
        return pulumi.get(self, "language_code")

    @language_code.setter
    def language_code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "language_code", value)

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> Optional[pulumi.Input[str]]:
        """
        The timestamp when the custom vocabulary was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @last_modified_time.setter
    def last_modified_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_modified_time", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A unique name of the custom vocabulary. Must not be more than 140 characters.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def state(self) -> Optional[pulumi.Input[str]]:
        """
        The current state of the custom vocabulary. Valid values are `CREATION_IN_PROGRESS`, `ACTIVE`, `CREATION_FAILED`, `DELETE_IN_PROGRESS`.
        """
        return pulumi.get(self, "state")

    @state.setter
    def state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "state", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Tags to apply to the vocabulary. If configured with a provider
        `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="vocabularyId")
    def vocabulary_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the custom vocabulary.
        """
        return pulumi.get(self, "vocabulary_id")

    @vocabulary_id.setter
    def vocabulary_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vocabulary_id", value)


class Vocabulary(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 language_code: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides an Amazon Connect Vocabulary resource. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.Vocabulary("example",
            instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
            name="example",
            content=\"\"\"Phrase\\x09IPA\\x09SoundsLike\\x09DisplayAs
        Los-Angeles\\x09\\x09\\x09Los Angeles
        F.B.I.\\x09ɛ f b i aɪ\\x09\\x09FBI
        Etienne\\x09\\x09eh-tee-en\\x09\"\"\",
            language_code="en-US",
            tags={
                "Key1": "Value1",
            })
        ```

        ## Import

        Using `pulumi import`, import Amazon Connect Vocabularies using the `instance_id` and `vocabulary_id` separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:connect/vocabulary:Vocabulary example f1288a1f-6193-445a-b47e-af739b2:c1d4e5f6-1b3c-1b3c-1b3c-c1d4e5f6c1d4e5
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] content: The content of the custom vocabulary in plain-text format with a table of values. Each row in the table represents a word or a phrase, described with Phrase, IPA, SoundsLike, and DisplayAs fields. Separate the fields with TAB characters. For more information, see [Create a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html#create-vocabulary-table). Minimum length of `1`. Maximum length of `60000`.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] language_code: The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-whatis.html). Valid Values are `ar-AE`, `de-CH`, `de-DE`, `en-AB`, `en-AU`, `en-GB`, `en-IE`, `en-IN`, `en-US`, `en-WL`, `es-ES`, `es-US`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN`.
        :param pulumi.Input[str] name: A unique name of the custom vocabulary. Must not be more than 140 characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the vocabulary. If configured with a provider
               `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VocabularyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Amazon Connect Vocabulary resource. For more information see
        [Amazon Connect: Getting Started](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-get-started.html)

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.connect.Vocabulary("example",
            instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
            name="example",
            content=\"\"\"Phrase\\x09IPA\\x09SoundsLike\\x09DisplayAs
        Los-Angeles\\x09\\x09\\x09Los Angeles
        F.B.I.\\x09ɛ f b i aɪ\\x09\\x09FBI
        Etienne\\x09\\x09eh-tee-en\\x09\"\"\",
            language_code="en-US",
            tags={
                "Key1": "Value1",
            })
        ```

        ## Import

        Using `pulumi import`, import Amazon Connect Vocabularies using the `instance_id` and `vocabulary_id` separated by a colon (`:`). For example:

        ```sh
        $ pulumi import aws:connect/vocabulary:Vocabulary example f1288a1f-6193-445a-b47e-af739b2:c1d4e5f6-1b3c-1b3c-1b3c-c1d4e5f6c1d4e5
        ```

        :param str resource_name: The name of the resource.
        :param VocabularyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VocabularyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 language_code: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VocabularyArgs.__new__(VocabularyArgs)

            if content is None and not opts.urn:
                raise TypeError("Missing required property 'content'")
            __props__.__dict__["content"] = content
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if language_code is None and not opts.urn:
                raise TypeError("Missing required property 'language_code'")
            __props__.__dict__["language_code"] = language_code
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["failure_reason"] = None
            __props__.__dict__["last_modified_time"] = None
            __props__.__dict__["state"] = None
            __props__.__dict__["tags_all"] = None
            __props__.__dict__["vocabulary_id"] = None
        super(Vocabulary, __self__).__init__(
            'aws:connect/vocabulary:Vocabulary',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            content: Optional[pulumi.Input[str]] = None,
            failure_reason: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            language_code: Optional[pulumi.Input[str]] = None,
            last_modified_time: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            state: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            vocabulary_id: Optional[pulumi.Input[str]] = None) -> 'Vocabulary':
        """
        Get an existing Vocabulary resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the vocabulary.
        :param pulumi.Input[str] content: The content of the custom vocabulary in plain-text format with a table of values. Each row in the table represents a word or a phrase, described with Phrase, IPA, SoundsLike, and DisplayAs fields. Separate the fields with TAB characters. For more information, see [Create a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html#create-vocabulary-table). Minimum length of `1`. Maximum length of `60000`.
        :param pulumi.Input[str] failure_reason: The reason why the custom vocabulary was not created.
        :param pulumi.Input[str] instance_id: Specifies the identifier of the hosting Amazon Connect Instance.
        :param pulumi.Input[str] language_code: The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-whatis.html). Valid Values are `ar-AE`, `de-CH`, `de-DE`, `en-AB`, `en-AU`, `en-GB`, `en-IE`, `en-IN`, `en-US`, `en-WL`, `es-ES`, `es-US`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN`.
        :param pulumi.Input[str] last_modified_time: The timestamp when the custom vocabulary was last modified.
        :param pulumi.Input[str] name: A unique name of the custom vocabulary. Must not be more than 140 characters.
        :param pulumi.Input[str] state: The current state of the custom vocabulary. Valid values are `CREATION_IN_PROGRESS`, `ACTIVE`, `CREATION_FAILED`, `DELETE_IN_PROGRESS`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to apply to the vocabulary. If configured with a provider
               `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] vocabulary_id: The identifier of the custom vocabulary.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _VocabularyState.__new__(_VocabularyState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["content"] = content
        __props__.__dict__["failure_reason"] = failure_reason
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["language_code"] = language_code
        __props__.__dict__["last_modified_time"] = last_modified_time
        __props__.__dict__["name"] = name
        __props__.__dict__["state"] = state
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["vocabulary_id"] = vocabulary_id
        return Vocabulary(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the vocabulary.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output[str]:
        """
        The content of the custom vocabulary in plain-text format with a table of values. Each row in the table represents a word or a phrase, described with Phrase, IPA, SoundsLike, and DisplayAs fields. Separate the fields with TAB characters. For more information, see [Create a custom vocabulary using a table](https://docs.aws.amazon.com/transcribe/latest/dg/custom-vocabulary.html#create-vocabulary-table). Minimum length of `1`. Maximum length of `60000`.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="failureReason")
    def failure_reason(self) -> pulumi.Output[str]:
        """
        The reason why the custom vocabulary was not created.
        """
        return pulumi.get(self, "failure_reason")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        Specifies the identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="languageCode")
    def language_code(self) -> pulumi.Output[str]:
        """
        The language code of the vocabulary entries. For a list of languages and their corresponding language codes, see [What is Amazon Transcribe?](https://docs.aws.amazon.com/transcribe/latest/dg/transcribe-whatis.html). Valid Values are `ar-AE`, `de-CH`, `de-DE`, `en-AB`, `en-AU`, `en-GB`, `en-IE`, `en-IN`, `en-US`, `en-WL`, `es-ES`, `es-US`, `fr-CA`, `fr-FR`, `hi-IN`, `it-IT`, `ja-JP`, `ko-KR`, `pt-BR`, `pt-PT`, `zh-CN`.
        """
        return pulumi.get(self, "language_code")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        The timestamp when the custom vocabulary was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        A unique name of the custom vocabulary. Must not be more than 140 characters.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The current state of the custom vocabulary. Valid values are `CREATION_IN_PROGRESS`, `ACTIVE`, `CREATION_FAILED`, `DELETE_IN_PROGRESS`.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags to apply to the vocabulary. If configured with a provider
        `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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
    @pulumi.getter(name="vocabularyId")
    def vocabulary_id(self) -> pulumi.Output[str]:
        """
        The identifier of the custom vocabulary.
        """
        return pulumi.get(self, "vocabulary_id")

