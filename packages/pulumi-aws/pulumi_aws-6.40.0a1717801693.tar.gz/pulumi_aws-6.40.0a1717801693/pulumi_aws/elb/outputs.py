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
    'LoadBalancerAccessLogs',
    'LoadBalancerHealthCheck',
    'LoadBalancerListener',
    'LoadBalancerPolicyPolicyAttribute',
    'SslNegotiationPolicyAttribute',
    'GetLoadBalancerAccessLogsResult',
    'GetLoadBalancerHealthCheckResult',
    'GetLoadBalancerListenerResult',
]

@pulumi.output_type
class LoadBalancerAccessLogs(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketPrefix":
            suggest = "bucket_prefix"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoadBalancerAccessLogs. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadBalancerAccessLogs.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoadBalancerAccessLogs.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket: str,
                 bucket_prefix: Optional[str] = None,
                 enabled: Optional[bool] = None,
                 interval: Optional[int] = None):
        """
        :param str bucket: The S3 bucket name to store the logs in.
        :param str bucket_prefix: The S3 bucket prefix. Logs are stored in the root if not configured.
        :param bool enabled: Boolean to enable / disable `access_logs`. Default is `true`
        :param int interval: The publishing interval in minutes. Valid values: `5` and `60`. Default: `60`
        """
        pulumi.set(__self__, "bucket", bucket)
        if bucket_prefix is not None:
            pulumi.set(__self__, "bucket_prefix", bucket_prefix)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if interval is not None:
            pulumi.set(__self__, "interval", interval)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        """
        The S3 bucket name to store the logs in.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> Optional[str]:
        """
        The S3 bucket prefix. Logs are stored in the root if not configured.
        """
        return pulumi.get(self, "bucket_prefix")

    @property
    @pulumi.getter
    def enabled(self) -> Optional[bool]:
        """
        Boolean to enable / disable `access_logs`. Default is `true`
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def interval(self) -> Optional[int]:
        """
        The publishing interval in minutes. Valid values: `5` and `60`. Default: `60`
        """
        return pulumi.get(self, "interval")


@pulumi.output_type
class LoadBalancerHealthCheck(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "healthyThreshold":
            suggest = "healthy_threshold"
        elif key == "unhealthyThreshold":
            suggest = "unhealthy_threshold"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoadBalancerHealthCheck. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadBalancerHealthCheck.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoadBalancerHealthCheck.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 healthy_threshold: int,
                 interval: int,
                 target: str,
                 timeout: int,
                 unhealthy_threshold: int):
        """
        :param int healthy_threshold: The number of checks before the instance is declared healthy.
        :param int interval: The interval between checks.
        :param str target: The target of the check. Valid pattern is "${PROTOCOL}:${PORT}${PATH}", where PROTOCOL
               values are:
               * `HTTP`, `HTTPS` - PORT and PATH are required
               * `TCP`, `SSL` - PORT is required, PATH is not supported
        :param int timeout: The length of time before the check times out.
        :param int unhealthy_threshold: The number of checks before the instance is declared unhealthy.
        """
        pulumi.set(__self__, "healthy_threshold", healthy_threshold)
        pulumi.set(__self__, "interval", interval)
        pulumi.set(__self__, "target", target)
        pulumi.set(__self__, "timeout", timeout)
        pulumi.set(__self__, "unhealthy_threshold", unhealthy_threshold)

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> int:
        """
        The number of checks before the instance is declared healthy.
        """
        return pulumi.get(self, "healthy_threshold")

    @property
    @pulumi.getter
    def interval(self) -> int:
        """
        The interval between checks.
        """
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter
    def target(self) -> str:
        """
        The target of the check. Valid pattern is "${PROTOCOL}:${PORT}${PATH}", where PROTOCOL
        values are:
        * `HTTP`, `HTTPS` - PORT and PATH are required
        * `TCP`, `SSL` - PORT is required, PATH is not supported
        """
        return pulumi.get(self, "target")

    @property
    @pulumi.getter
    def timeout(self) -> int:
        """
        The length of time before the check times out.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter(name="unhealthyThreshold")
    def unhealthy_threshold(self) -> int:
        """
        The number of checks before the instance is declared unhealthy.
        """
        return pulumi.get(self, "unhealthy_threshold")


@pulumi.output_type
class LoadBalancerListener(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "instancePort":
            suggest = "instance_port"
        elif key == "instanceProtocol":
            suggest = "instance_protocol"
        elif key == "lbPort":
            suggest = "lb_port"
        elif key == "lbProtocol":
            suggest = "lb_protocol"
        elif key == "sslCertificateId":
            suggest = "ssl_certificate_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LoadBalancerListener. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LoadBalancerListener.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LoadBalancerListener.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 instance_port: int,
                 instance_protocol: str,
                 lb_port: int,
                 lb_protocol: str,
                 ssl_certificate_id: Optional[str] = None):
        """
        :param int instance_port: The port on the instance to route to
        :param str instance_protocol: The protocol to use to the instance. Valid
               values are `HTTP`, `HTTPS`, `TCP`, or `SSL`
        :param int lb_port: The port to listen on for the load balancer
        :param str lb_protocol: The protocol to listen on. Valid values are `HTTP`,
               `HTTPS`, `TCP`, or `SSL`
        :param str ssl_certificate_id: The ARN of an SSL certificate you have
               uploaded to AWS IAM. **Note ECDSA-specific restrictions below.  Only valid when `lb_protocol` is either HTTPS or SSL**
        """
        pulumi.set(__self__, "instance_port", instance_port)
        pulumi.set(__self__, "instance_protocol", instance_protocol)
        pulumi.set(__self__, "lb_port", lb_port)
        pulumi.set(__self__, "lb_protocol", lb_protocol)
        if ssl_certificate_id is not None:
            pulumi.set(__self__, "ssl_certificate_id", ssl_certificate_id)

    @property
    @pulumi.getter(name="instancePort")
    def instance_port(self) -> int:
        """
        The port on the instance to route to
        """
        return pulumi.get(self, "instance_port")

    @property
    @pulumi.getter(name="instanceProtocol")
    def instance_protocol(self) -> str:
        """
        The protocol to use to the instance. Valid
        values are `HTTP`, `HTTPS`, `TCP`, or `SSL`
        """
        return pulumi.get(self, "instance_protocol")

    @property
    @pulumi.getter(name="lbPort")
    def lb_port(self) -> int:
        """
        The port to listen on for the load balancer
        """
        return pulumi.get(self, "lb_port")

    @property
    @pulumi.getter(name="lbProtocol")
    def lb_protocol(self) -> str:
        """
        The protocol to listen on. Valid values are `HTTP`,
        `HTTPS`, `TCP`, or `SSL`
        """
        return pulumi.get(self, "lb_protocol")

    @property
    @pulumi.getter(name="sslCertificateId")
    def ssl_certificate_id(self) -> Optional[str]:
        """
        The ARN of an SSL certificate you have
        uploaded to AWS IAM. **Note ECDSA-specific restrictions below.  Only valid when `lb_protocol` is either HTTPS or SSL**
        """
        return pulumi.get(self, "ssl_certificate_id")


@pulumi.output_type
class LoadBalancerPolicyPolicyAttribute(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 value: Optional[str] = None):
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        return pulumi.get(self, "value")


@pulumi.output_type
class SslNegotiationPolicyAttribute(dict):
    def __init__(__self__, *,
                 name: str,
                 value: str):
        """
        :param str name: The name of the attribute
        :param str value: The value of the attribute
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the attribute
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the attribute
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class GetLoadBalancerAccessLogsResult(dict):
    def __init__(__self__, *,
                 bucket: str,
                 bucket_prefix: str,
                 enabled: bool,
                 interval: int):
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "bucket_prefix", bucket_prefix)
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "interval", interval)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="bucketPrefix")
    def bucket_prefix(self) -> str:
        return pulumi.get(self, "bucket_prefix")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def interval(self) -> int:
        return pulumi.get(self, "interval")


@pulumi.output_type
class GetLoadBalancerHealthCheckResult(dict):
    def __init__(__self__, *,
                 healthy_threshold: int,
                 interval: int,
                 target: str,
                 timeout: int,
                 unhealthy_threshold: int):
        pulumi.set(__self__, "healthy_threshold", healthy_threshold)
        pulumi.set(__self__, "interval", interval)
        pulumi.set(__self__, "target", target)
        pulumi.set(__self__, "timeout", timeout)
        pulumi.set(__self__, "unhealthy_threshold", unhealthy_threshold)

    @property
    @pulumi.getter(name="healthyThreshold")
    def healthy_threshold(self) -> int:
        return pulumi.get(self, "healthy_threshold")

    @property
    @pulumi.getter
    def interval(self) -> int:
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter
    def target(self) -> str:
        return pulumi.get(self, "target")

    @property
    @pulumi.getter
    def timeout(self) -> int:
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter(name="unhealthyThreshold")
    def unhealthy_threshold(self) -> int:
        return pulumi.get(self, "unhealthy_threshold")


@pulumi.output_type
class GetLoadBalancerListenerResult(dict):
    def __init__(__self__, *,
                 instance_port: int,
                 instance_protocol: str,
                 lb_port: int,
                 lb_protocol: str,
                 ssl_certificate_id: str):
        pulumi.set(__self__, "instance_port", instance_port)
        pulumi.set(__self__, "instance_protocol", instance_protocol)
        pulumi.set(__self__, "lb_port", lb_port)
        pulumi.set(__self__, "lb_protocol", lb_protocol)
        pulumi.set(__self__, "ssl_certificate_id", ssl_certificate_id)

    @property
    @pulumi.getter(name="instancePort")
    def instance_port(self) -> int:
        return pulumi.get(self, "instance_port")

    @property
    @pulumi.getter(name="instanceProtocol")
    def instance_protocol(self) -> str:
        return pulumi.get(self, "instance_protocol")

    @property
    @pulumi.getter(name="lbPort")
    def lb_port(self) -> int:
        return pulumi.get(self, "lb_port")

    @property
    @pulumi.getter(name="lbProtocol")
    def lb_protocol(self) -> str:
        return pulumi.get(self, "lb_protocol")

    @property
    @pulumi.getter(name="sslCertificateId")
    def ssl_certificate_id(self) -> str:
        return pulumi.get(self, "ssl_certificate_id")


