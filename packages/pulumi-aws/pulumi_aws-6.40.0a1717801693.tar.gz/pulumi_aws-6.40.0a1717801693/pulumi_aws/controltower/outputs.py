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
    'LandingZoneDriftStatus',
]

@pulumi.output_type
class LandingZoneDriftStatus(dict):
    def __init__(__self__, *,
                 status: Optional[str] = None):
        """
        :param str status: The drift status of the landing zone.
        """
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The drift status of the landing zone.
        """
        return pulumi.get(self, "status")


