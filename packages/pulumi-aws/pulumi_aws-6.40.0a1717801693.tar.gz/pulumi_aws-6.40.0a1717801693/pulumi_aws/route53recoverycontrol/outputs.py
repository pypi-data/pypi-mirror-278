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
    'ClusterClusterEndpoint',
    'SafetyRuleRuleConfig',
]

@pulumi.output_type
class ClusterClusterEndpoint(dict):
    def __init__(__self__, *,
                 endpoint: Optional[str] = None,
                 region: Optional[str] = None):
        """
        :param str endpoint: Cluster endpoint.
        :param str region: Region of the endpoint.
        """
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[str]:
        """
        Cluster endpoint.
        """
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def region(self) -> Optional[str]:
        """
        Region of the endpoint.
        """
        return pulumi.get(self, "region")


@pulumi.output_type
class SafetyRuleRuleConfig(dict):
    def __init__(__self__, *,
                 inverted: bool,
                 threshold: int,
                 type: str):
        """
        :param bool inverted: Logical negation of the rule.
        :param int threshold: Number of controls that must be set when you specify an `ATLEAST` type rule.
        :param str type: Rule type. Valid values are `ATLEAST`, `AND`, and `OR`.
        """
        pulumi.set(__self__, "inverted", inverted)
        pulumi.set(__self__, "threshold", threshold)
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def inverted(self) -> bool:
        """
        Logical negation of the rule.
        """
        return pulumi.get(self, "inverted")

    @property
    @pulumi.getter
    def threshold(self) -> int:
        """
        Number of controls that must be set when you specify an `ATLEAST` type rule.
        """
        return pulumi.get(self, "threshold")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Rule type. Valid values are `ATLEAST`, `AND`, and `OR`.
        """
        return pulumi.get(self, "type")


