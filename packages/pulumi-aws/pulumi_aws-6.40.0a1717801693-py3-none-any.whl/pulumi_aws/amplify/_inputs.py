# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'AppAutoBranchCreationConfigArgs',
    'AppCustomRuleArgs',
    'AppProductionBranchArgs',
    'DomainAssociationSubDomainArgs',
]

@pulumi.input_type
class AppAutoBranchCreationConfigArgs:
    def __init__(__self__, *,
                 basic_auth_credentials: Optional[pulumi.Input[str]] = None,
                 build_spec: Optional[pulumi.Input[str]] = None,
                 enable_auto_build: Optional[pulumi.Input[bool]] = None,
                 enable_basic_auth: Optional[pulumi.Input[bool]] = None,
                 enable_performance_mode: Optional[pulumi.Input[bool]] = None,
                 enable_pull_request_preview: Optional[pulumi.Input[bool]] = None,
                 environment_variables: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 framework: Optional[pulumi.Input[str]] = None,
                 pull_request_environment_name: Optional[pulumi.Input[str]] = None,
                 stage: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] basic_auth_credentials: Basic authorization credentials for the autocreated branch.
        :param pulumi.Input[str] build_spec: Build specification (build spec) for the autocreated branch.
        :param pulumi.Input[bool] enable_auto_build: Enables auto building for the autocreated branch.
        :param pulumi.Input[bool] enable_basic_auth: Enables basic authorization for the autocreated branch.
        :param pulumi.Input[bool] enable_performance_mode: Enables performance mode for the branch.
        :param pulumi.Input[bool] enable_pull_request_preview: Enables pull request previews for the autocreated branch.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] environment_variables: Environment variables for the autocreated branch.
        :param pulumi.Input[str] framework: Framework for the autocreated branch.
        :param pulumi.Input[str] pull_request_environment_name: Amplify environment name for the pull request.
        :param pulumi.Input[str] stage: Describes the current stage for the autocreated branch. Valid values: `PRODUCTION`, `BETA`, `DEVELOPMENT`, `EXPERIMENTAL`, `PULL_REQUEST`.
        """
        if basic_auth_credentials is not None:
            pulumi.set(__self__, "basic_auth_credentials", basic_auth_credentials)
        if build_spec is not None:
            pulumi.set(__self__, "build_spec", build_spec)
        if enable_auto_build is not None:
            pulumi.set(__self__, "enable_auto_build", enable_auto_build)
        if enable_basic_auth is not None:
            pulumi.set(__self__, "enable_basic_auth", enable_basic_auth)
        if enable_performance_mode is not None:
            pulumi.set(__self__, "enable_performance_mode", enable_performance_mode)
        if enable_pull_request_preview is not None:
            pulumi.set(__self__, "enable_pull_request_preview", enable_pull_request_preview)
        if environment_variables is not None:
            pulumi.set(__self__, "environment_variables", environment_variables)
        if framework is not None:
            pulumi.set(__self__, "framework", framework)
        if pull_request_environment_name is not None:
            pulumi.set(__self__, "pull_request_environment_name", pull_request_environment_name)
        if stage is not None:
            pulumi.set(__self__, "stage", stage)

    @property
    @pulumi.getter(name="basicAuthCredentials")
    def basic_auth_credentials(self) -> Optional[pulumi.Input[str]]:
        """
        Basic authorization credentials for the autocreated branch.
        """
        return pulumi.get(self, "basic_auth_credentials")

    @basic_auth_credentials.setter
    def basic_auth_credentials(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "basic_auth_credentials", value)

    @property
    @pulumi.getter(name="buildSpec")
    def build_spec(self) -> Optional[pulumi.Input[str]]:
        """
        Build specification (build spec) for the autocreated branch.
        """
        return pulumi.get(self, "build_spec")

    @build_spec.setter
    def build_spec(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "build_spec", value)

    @property
    @pulumi.getter(name="enableAutoBuild")
    def enable_auto_build(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables auto building for the autocreated branch.
        """
        return pulumi.get(self, "enable_auto_build")

    @enable_auto_build.setter
    def enable_auto_build(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_auto_build", value)

    @property
    @pulumi.getter(name="enableBasicAuth")
    def enable_basic_auth(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables basic authorization for the autocreated branch.
        """
        return pulumi.get(self, "enable_basic_auth")

    @enable_basic_auth.setter
    def enable_basic_auth(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_basic_auth", value)

    @property
    @pulumi.getter(name="enablePerformanceMode")
    def enable_performance_mode(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables performance mode for the branch.
        """
        return pulumi.get(self, "enable_performance_mode")

    @enable_performance_mode.setter
    def enable_performance_mode(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_performance_mode", value)

    @property
    @pulumi.getter(name="enablePullRequestPreview")
    def enable_pull_request_preview(self) -> Optional[pulumi.Input[bool]]:
        """
        Enables pull request previews for the autocreated branch.
        """
        return pulumi.get(self, "enable_pull_request_preview")

    @enable_pull_request_preview.setter
    def enable_pull_request_preview(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_pull_request_preview", value)

    @property
    @pulumi.getter(name="environmentVariables")
    def environment_variables(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Environment variables for the autocreated branch.
        """
        return pulumi.get(self, "environment_variables")

    @environment_variables.setter
    def environment_variables(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "environment_variables", value)

    @property
    @pulumi.getter
    def framework(self) -> Optional[pulumi.Input[str]]:
        """
        Framework for the autocreated branch.
        """
        return pulumi.get(self, "framework")

    @framework.setter
    def framework(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "framework", value)

    @property
    @pulumi.getter(name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> Optional[pulumi.Input[str]]:
        """
        Amplify environment name for the pull request.
        """
        return pulumi.get(self, "pull_request_environment_name")

    @pull_request_environment_name.setter
    def pull_request_environment_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pull_request_environment_name", value)

    @property
    @pulumi.getter
    def stage(self) -> Optional[pulumi.Input[str]]:
        """
        Describes the current stage for the autocreated branch. Valid values: `PRODUCTION`, `BETA`, `DEVELOPMENT`, `EXPERIMENTAL`, `PULL_REQUEST`.
        """
        return pulumi.get(self, "stage")

    @stage.setter
    def stage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage", value)


@pulumi.input_type
class AppCustomRuleArgs:
    def __init__(__self__, *,
                 source: pulumi.Input[str],
                 target: pulumi.Input[str],
                 condition: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] source: Source pattern for a URL rewrite or redirect rule.
        :param pulumi.Input[str] target: Target pattern for a URL rewrite or redirect rule.
        :param pulumi.Input[str] condition: Condition for a URL rewrite or redirect rule, such as a country code.
        :param pulumi.Input[str] status: Status code for a URL rewrite or redirect rule. Valid values: `200`, `301`, `302`, `404`, `404-200`.
        """
        pulumi.set(__self__, "source", source)
        pulumi.set(__self__, "target", target)
        if condition is not None:
            pulumi.set(__self__, "condition", condition)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def source(self) -> pulumi.Input[str]:
        """
        Source pattern for a URL rewrite or redirect rule.
        """
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: pulumi.Input[str]):
        pulumi.set(self, "source", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        Target pattern for a URL rewrite or redirect rule.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter
    def condition(self) -> Optional[pulumi.Input[str]]:
        """
        Condition for a URL rewrite or redirect rule, such as a country code.
        """
        return pulumi.get(self, "condition")

    @condition.setter
    def condition(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "condition", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status code for a URL rewrite or redirect rule. Valid values: `200`, `301`, `302`, `404`, `404-200`.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class AppProductionBranchArgs:
    def __init__(__self__, *,
                 branch_name: Optional[pulumi.Input[str]] = None,
                 last_deploy_time: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None,
                 thumbnail_url: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] branch_name: Branch name for the production branch.
        :param pulumi.Input[str] last_deploy_time: Last deploy time of the production branch.
        :param pulumi.Input[str] status: Status of the production branch.
        :param pulumi.Input[str] thumbnail_url: Thumbnail URL for the production branch.
        """
        if branch_name is not None:
            pulumi.set(__self__, "branch_name", branch_name)
        if last_deploy_time is not None:
            pulumi.set(__self__, "last_deploy_time", last_deploy_time)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if thumbnail_url is not None:
            pulumi.set(__self__, "thumbnail_url", thumbnail_url)

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> Optional[pulumi.Input[str]]:
        """
        Branch name for the production branch.
        """
        return pulumi.get(self, "branch_name")

    @branch_name.setter
    def branch_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "branch_name", value)

    @property
    @pulumi.getter(name="lastDeployTime")
    def last_deploy_time(self) -> Optional[pulumi.Input[str]]:
        """
        Last deploy time of the production branch.
        """
        return pulumi.get(self, "last_deploy_time")

    @last_deploy_time.setter
    def last_deploy_time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_deploy_time", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Status of the production branch.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="thumbnailUrl")
    def thumbnail_url(self) -> Optional[pulumi.Input[str]]:
        """
        Thumbnail URL for the production branch.
        """
        return pulumi.get(self, "thumbnail_url")

    @thumbnail_url.setter
    def thumbnail_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbnail_url", value)


@pulumi.input_type
class DomainAssociationSubDomainArgs:
    def __init__(__self__, *,
                 branch_name: pulumi.Input[str],
                 prefix: pulumi.Input[str],
                 dns_record: Optional[pulumi.Input[str]] = None,
                 verified: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[str] branch_name: Branch name setting for the subdomain.
        :param pulumi.Input[str] prefix: Prefix setting for the subdomain.
        :param pulumi.Input[str] dns_record: DNS record for the subdomain in a space-prefixed and space-delimited format (` CNAME <target>`).
        :param pulumi.Input[bool] verified: Verified status of the subdomain.
        """
        pulumi.set(__self__, "branch_name", branch_name)
        pulumi.set(__self__, "prefix", prefix)
        if dns_record is not None:
            pulumi.set(__self__, "dns_record", dns_record)
        if verified is not None:
            pulumi.set(__self__, "verified", verified)

    @property
    @pulumi.getter(name="branchName")
    def branch_name(self) -> pulumi.Input[str]:
        """
        Branch name setting for the subdomain.
        """
        return pulumi.get(self, "branch_name")

    @branch_name.setter
    def branch_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "branch_name", value)

    @property
    @pulumi.getter
    def prefix(self) -> pulumi.Input[str]:
        """
        Prefix setting for the subdomain.
        """
        return pulumi.get(self, "prefix")

    @prefix.setter
    def prefix(self, value: pulumi.Input[str]):
        pulumi.set(self, "prefix", value)

    @property
    @pulumi.getter(name="dnsRecord")
    def dns_record(self) -> Optional[pulumi.Input[str]]:
        """
        DNS record for the subdomain in a space-prefixed and space-delimited format (` CNAME <target>`).
        """
        return pulumi.get(self, "dns_record")

    @dns_record.setter
    def dns_record(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "dns_record", value)

    @property
    @pulumi.getter
    def verified(self) -> Optional[pulumi.Input[bool]]:
        """
        Verified status of the subdomain.
        """
        return pulumi.get(self, "verified")

    @verified.setter
    def verified(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "verified", value)


