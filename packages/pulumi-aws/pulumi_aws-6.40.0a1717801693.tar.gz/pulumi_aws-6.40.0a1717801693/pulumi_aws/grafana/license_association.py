# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['LicenseAssociationArgs', 'LicenseAssociation']

@pulumi.input_type
class LicenseAssociationArgs:
    def __init__(__self__, *,
                 license_type: pulumi.Input[str],
                 workspace_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a LicenseAssociation resource.
        :param pulumi.Input[str] license_type: The type of license for the workspace license association. Valid values are `ENTERPRISE` and `ENTERPRISE_FREE_TRIAL`.
        :param pulumi.Input[str] workspace_id: The workspace id.
        """
        pulumi.set(__self__, "license_type", license_type)
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Input[str]:
        """
        The type of license for the workspace license association. Valid values are `ENTERPRISE` and `ENTERPRISE_FREE_TRIAL`.
        """
        return pulumi.get(self, "license_type")

    @license_type.setter
    def license_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "license_type", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Input[str]:
        """
        The workspace id.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "workspace_id", value)


@pulumi.input_type
class _LicenseAssociationState:
    def __init__(__self__, *,
                 free_trial_expiration: Optional[pulumi.Input[str]] = None,
                 license_expiration: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LicenseAssociation resources.
        :param pulumi.Input[str] free_trial_expiration: If `license_type` is set to `ENTERPRISE_FREE_TRIAL`, this is the expiration date of the free trial.
        :param pulumi.Input[str] license_expiration: If `license_type` is set to `ENTERPRISE`, this is the expiration date of the enterprise license.
        :param pulumi.Input[str] license_type: The type of license for the workspace license association. Valid values are `ENTERPRISE` and `ENTERPRISE_FREE_TRIAL`.
        :param pulumi.Input[str] workspace_id: The workspace id.
        """
        if free_trial_expiration is not None:
            pulumi.set(__self__, "free_trial_expiration", free_trial_expiration)
        if license_expiration is not None:
            pulumi.set(__self__, "license_expiration", license_expiration)
        if license_type is not None:
            pulumi.set(__self__, "license_type", license_type)
        if workspace_id is not None:
            pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="freeTrialExpiration")
    def free_trial_expiration(self) -> Optional[pulumi.Input[str]]:
        """
        If `license_type` is set to `ENTERPRISE_FREE_TRIAL`, this is the expiration date of the free trial.
        """
        return pulumi.get(self, "free_trial_expiration")

    @free_trial_expiration.setter
    def free_trial_expiration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "free_trial_expiration", value)

    @property
    @pulumi.getter(name="licenseExpiration")
    def license_expiration(self) -> Optional[pulumi.Input[str]]:
        """
        If `license_type` is set to `ENTERPRISE`, this is the expiration date of the enterprise license.
        """
        return pulumi.get(self, "license_expiration")

    @license_expiration.setter
    def license_expiration(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "license_expiration", value)

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of license for the workspace license association. Valid values are `ENTERPRISE` and `ENTERPRISE_FREE_TRIAL`.
        """
        return pulumi.get(self, "license_type")

    @license_type.setter
    def license_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "license_type", value)

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> Optional[pulumi.Input[str]]:
        """
        The workspace id.
        """
        return pulumi.get(self, "workspace_id")

    @workspace_id.setter
    def workspace_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workspace_id", value)


class LicenseAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 license_type: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Amazon Managed Grafana workspace license association resource.

        ## Example Usage

        ### Basic configuration

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        assume = aws.iam.Role("assume",
            name="grafana-assume",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {
                        "Service": "grafana.amazonaws.com",
                    },
                }],
            }))
        example_workspace = aws.grafana.Workspace("example",
            account_access_type="CURRENT_ACCOUNT",
            authentication_providers=["SAML"],
            permission_type="SERVICE_MANAGED",
            role_arn=assume.arn)
        example = aws.grafana.LicenseAssociation("example",
            license_type="ENTERPRISE_FREE_TRIAL",
            workspace_id=example_workspace.id)
        ```

        ## Import

        Using `pulumi import`, import Grafana workspace license association using the workspace's `id`. For example:

        ```sh
        $ pulumi import aws:grafana/licenseAssociation:LicenseAssociation example g-2054c75a02
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] license_type: The type of license for the workspace license association. Valid values are `ENTERPRISE` and `ENTERPRISE_FREE_TRIAL`.
        :param pulumi.Input[str] workspace_id: The workspace id.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LicenseAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Amazon Managed Grafana workspace license association resource.

        ## Example Usage

        ### Basic configuration

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        assume = aws.iam.Role("assume",
            name="grafana-assume",
            assume_role_policy=json.dumps({
                "Version": "2012-10-17",
                "Statement": [{
                    "Action": "sts:AssumeRole",
                    "Effect": "Allow",
                    "Sid": "",
                    "Principal": {
                        "Service": "grafana.amazonaws.com",
                    },
                }],
            }))
        example_workspace = aws.grafana.Workspace("example",
            account_access_type="CURRENT_ACCOUNT",
            authentication_providers=["SAML"],
            permission_type="SERVICE_MANAGED",
            role_arn=assume.arn)
        example = aws.grafana.LicenseAssociation("example",
            license_type="ENTERPRISE_FREE_TRIAL",
            workspace_id=example_workspace.id)
        ```

        ## Import

        Using `pulumi import`, import Grafana workspace license association using the workspace's `id`. For example:

        ```sh
        $ pulumi import aws:grafana/licenseAssociation:LicenseAssociation example g-2054c75a02
        ```

        :param str resource_name: The name of the resource.
        :param LicenseAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LicenseAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 license_type: Optional[pulumi.Input[str]] = None,
                 workspace_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = LicenseAssociationArgs.__new__(LicenseAssociationArgs)

            if license_type is None and not opts.urn:
                raise TypeError("Missing required property 'license_type'")
            __props__.__dict__["license_type"] = license_type
            if workspace_id is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_id'")
            __props__.__dict__["workspace_id"] = workspace_id
            __props__.__dict__["free_trial_expiration"] = None
            __props__.__dict__["license_expiration"] = None
        super(LicenseAssociation, __self__).__init__(
            'aws:grafana/licenseAssociation:LicenseAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            free_trial_expiration: Optional[pulumi.Input[str]] = None,
            license_expiration: Optional[pulumi.Input[str]] = None,
            license_type: Optional[pulumi.Input[str]] = None,
            workspace_id: Optional[pulumi.Input[str]] = None) -> 'LicenseAssociation':
        """
        Get an existing LicenseAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] free_trial_expiration: If `license_type` is set to `ENTERPRISE_FREE_TRIAL`, this is the expiration date of the free trial.
        :param pulumi.Input[str] license_expiration: If `license_type` is set to `ENTERPRISE`, this is the expiration date of the enterprise license.
        :param pulumi.Input[str] license_type: The type of license for the workspace license association. Valid values are `ENTERPRISE` and `ENTERPRISE_FREE_TRIAL`.
        :param pulumi.Input[str] workspace_id: The workspace id.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LicenseAssociationState.__new__(_LicenseAssociationState)

        __props__.__dict__["free_trial_expiration"] = free_trial_expiration
        __props__.__dict__["license_expiration"] = license_expiration
        __props__.__dict__["license_type"] = license_type
        __props__.__dict__["workspace_id"] = workspace_id
        return LicenseAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="freeTrialExpiration")
    def free_trial_expiration(self) -> pulumi.Output[str]:
        """
        If `license_type` is set to `ENTERPRISE_FREE_TRIAL`, this is the expiration date of the free trial.
        """
        return pulumi.get(self, "free_trial_expiration")

    @property
    @pulumi.getter(name="licenseExpiration")
    def license_expiration(self) -> pulumi.Output[str]:
        """
        If `license_type` is set to `ENTERPRISE`, this is the expiration date of the enterprise license.
        """
        return pulumi.get(self, "license_expiration")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Output[str]:
        """
        The type of license for the workspace license association. Valid values are `ENTERPRISE` and `ENTERPRISE_FREE_TRIAL`.
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> pulumi.Output[str]:
        """
        The workspace id.
        """
        return pulumi.get(self, "workspace_id")

