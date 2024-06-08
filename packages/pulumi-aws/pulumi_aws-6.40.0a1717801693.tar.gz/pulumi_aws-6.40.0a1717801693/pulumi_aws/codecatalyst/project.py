# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ProjectArgs', 'Project']

@pulumi.input_type
class ProjectArgs:
    def __init__(__self__, *,
                 display_name: pulumi.Input[str],
                 space_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Project resource.
        :param pulumi.Input[str] display_name: The friendly name of the project that will be displayed to users.
               
               The following arguments are optional:
        :param pulumi.Input[str] space_name: The name of the space.
        :param pulumi.Input[str] description: The description of the project. This description will be displayed to all users of the project. We recommend providing a brief description of the project and its intended purpose.
        """
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "space_name", space_name)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Input[str]:
        """
        The friendly name of the project that will be displayed to users.

        The following arguments are optional:
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter(name="spaceName")
    def space_name(self) -> pulumi.Input[str]:
        """
        The name of the space.
        """
        return pulumi.get(self, "space_name")

    @space_name.setter
    def space_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "space_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the project. This description will be displayed to all users of the project. We recommend providing a brief description of the project and its intended purpose.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)


@pulumi.input_type
class _ProjectState:
    def __init__(__self__, *,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 space_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Project resources.
        :param pulumi.Input[str] description: The description of the project. This description will be displayed to all users of the project. We recommend providing a brief description of the project and its intended purpose.
        :param pulumi.Input[str] display_name: The friendly name of the project that will be displayed to users.
               
               The following arguments are optional:
        :param pulumi.Input[str] name: The name of the project in the space.
        :param pulumi.Input[str] space_name: The name of the space.
        """
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if space_name is not None:
            pulumi.set(__self__, "space_name", space_name)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the project. This description will be displayed to all users of the project. We recommend providing a brief description of the project and its intended purpose.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        The friendly name of the project that will be displayed to users.

        The following arguments are optional:
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the project in the space.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="spaceName")
    def space_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the space.
        """
        return pulumi.get(self, "space_name")

    @space_name.setter
    def space_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "space_name", value)


class Project(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 space_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource for managing an AWS CodeCatalyst Project.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.codecatalyst.Project("test",
            space_name="myproject",
            display_name="MyProject",
            description="My CodeCatalyst Project created using Pulumi")
        ```

        ## Import

        Using `pulumi import`, import CodeCatalyst Project using the `id`. For example:

        ```sh
        $ pulumi import aws:codecatalyst/project:Project example project-id-12345678
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the project. This description will be displayed to all users of the project. We recommend providing a brief description of the project and its intended purpose.
        :param pulumi.Input[str] display_name: The friendly name of the project that will be displayed to users.
               
               The following arguments are optional:
        :param pulumi.Input[str] space_name: The name of the space.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ProjectArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS CodeCatalyst Project.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.codecatalyst.Project("test",
            space_name="myproject",
            display_name="MyProject",
            description="My CodeCatalyst Project created using Pulumi")
        ```

        ## Import

        Using `pulumi import`, import CodeCatalyst Project using the `id`. For example:

        ```sh
        $ pulumi import aws:codecatalyst/project:Project example project-id-12345678
        ```

        :param str resource_name: The name of the resource.
        :param ProjectArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ProjectArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 space_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ProjectArgs.__new__(ProjectArgs)

            __props__.__dict__["description"] = description
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__.__dict__["display_name"] = display_name
            if space_name is None and not opts.urn:
                raise TypeError("Missing required property 'space_name'")
            __props__.__dict__["space_name"] = space_name
            __props__.__dict__["name"] = None
        super(Project, __self__).__init__(
            'aws:codecatalyst/project:Project',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            space_name: Optional[pulumi.Input[str]] = None) -> 'Project':
        """
        Get an existing Project resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: The description of the project. This description will be displayed to all users of the project. We recommend providing a brief description of the project and its intended purpose.
        :param pulumi.Input[str] display_name: The friendly name of the project that will be displayed to users.
               
               The following arguments are optional:
        :param pulumi.Input[str] name: The name of the project in the space.
        :param pulumi.Input[str] space_name: The name of the space.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ProjectState.__new__(_ProjectState)

        __props__.__dict__["description"] = description
        __props__.__dict__["display_name"] = display_name
        __props__.__dict__["name"] = name
        __props__.__dict__["space_name"] = space_name
        return Project(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the project. This description will be displayed to all users of the project. We recommend providing a brief description of the project and its intended purpose.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The friendly name of the project that will be displayed to users.

        The following arguments are optional:
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the project in the space.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="spaceName")
    def space_name(self) -> pulumi.Output[str]:
        """
        The name of the space.
        """
        return pulumi.get(self, "space_name")

