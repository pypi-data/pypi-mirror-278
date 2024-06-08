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

__all__ = [
    'PipelineBufferOptions',
    'PipelineEncryptionAtRestOptions',
    'PipelineLogPublishingOptions',
    'PipelineLogPublishingOptionsCloudwatchLogDestination',
    'PipelineTimeouts',
    'PipelineVpcOptions',
]

@pulumi.output_type
class PipelineBufferOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "persistentBufferEnabled":
            suggest = "persistent_buffer_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineBufferOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineBufferOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineBufferOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 persistent_buffer_enabled: bool):
        """
        :param bool persistent_buffer_enabled: Whether persistent buffering should be enabled.
        """
        pulumi.set(__self__, "persistent_buffer_enabled", persistent_buffer_enabled)

    @property
    @pulumi.getter(name="persistentBufferEnabled")
    def persistent_buffer_enabled(self) -> bool:
        """
        Whether persistent buffering should be enabled.
        """
        return pulumi.get(self, "persistent_buffer_enabled")


@pulumi.output_type
class PipelineEncryptionAtRestOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "kmsKeyArn":
            suggest = "kms_key_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineEncryptionAtRestOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineEncryptionAtRestOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineEncryptionAtRestOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 kms_key_arn: str):
        """
        :param str kms_key_arn: The ARN of the KMS key used to encrypt data-at-rest in OpenSearch Ingestion. By default, data is encrypted using an AWS owned key.
        """
        pulumi.set(__self__, "kms_key_arn", kms_key_arn)

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> str:
        """
        The ARN of the KMS key used to encrypt data-at-rest in OpenSearch Ingestion. By default, data is encrypted using an AWS owned key.
        """
        return pulumi.get(self, "kms_key_arn")


@pulumi.output_type
class PipelineLogPublishingOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "cloudwatchLogDestination":
            suggest = "cloudwatch_log_destination"
        elif key == "isLoggingEnabled":
            suggest = "is_logging_enabled"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineLogPublishingOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineLogPublishingOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineLogPublishingOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 cloudwatch_log_destination: Optional['outputs.PipelineLogPublishingOptionsCloudwatchLogDestination'] = None,
                 is_logging_enabled: Optional[bool] = None):
        """
        :param 'PipelineLogPublishingOptionsCloudwatchLogDestinationArgs' cloudwatch_log_destination: The destination for OpenSearch Ingestion logs sent to Amazon CloudWatch Logs. This parameter is required if IsLoggingEnabled is set to true. See `cloudwatch_log_destination` below.
        :param bool is_logging_enabled: Whether logs should be published.
        """
        if cloudwatch_log_destination is not None:
            pulumi.set(__self__, "cloudwatch_log_destination", cloudwatch_log_destination)
        if is_logging_enabled is not None:
            pulumi.set(__self__, "is_logging_enabled", is_logging_enabled)

    @property
    @pulumi.getter(name="cloudwatchLogDestination")
    def cloudwatch_log_destination(self) -> Optional['outputs.PipelineLogPublishingOptionsCloudwatchLogDestination']:
        """
        The destination for OpenSearch Ingestion logs sent to Amazon CloudWatch Logs. This parameter is required if IsLoggingEnabled is set to true. See `cloudwatch_log_destination` below.
        """
        return pulumi.get(self, "cloudwatch_log_destination")

    @property
    @pulumi.getter(name="isLoggingEnabled")
    def is_logging_enabled(self) -> Optional[bool]:
        """
        Whether logs should be published.
        """
        return pulumi.get(self, "is_logging_enabled")


@pulumi.output_type
class PipelineLogPublishingOptionsCloudwatchLogDestination(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logGroup":
            suggest = "log_group"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineLogPublishingOptionsCloudwatchLogDestination. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineLogPublishingOptionsCloudwatchLogDestination.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineLogPublishingOptionsCloudwatchLogDestination.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 log_group: str):
        """
        :param str log_group: The name of the CloudWatch Logs group to send pipeline logs to. You can specify an existing log group or create a new one. For example, /aws/OpenSearchService/IngestionService/my-pipeline.
        """
        pulumi.set(__self__, "log_group", log_group)

    @property
    @pulumi.getter(name="logGroup")
    def log_group(self) -> str:
        """
        The name of the CloudWatch Logs group to send pipeline logs to. You can specify an existing log group or create a new one. For example, /aws/OpenSearchService/IngestionService/my-pipeline.
        """
        return pulumi.get(self, "log_group")


@pulumi.output_type
class PipelineTimeouts(dict):
    def __init__(__self__, *,
                 create: Optional[str] = None,
                 delete: Optional[str] = None,
                 update: Optional[str] = None):
        """
        :param str create: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        :param str delete: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        :param str update: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        if create is not None:
            pulumi.set(__self__, "create", create)
        if delete is not None:
            pulumi.set(__self__, "delete", delete)
        if update is not None:
            pulumi.set(__self__, "update", update)

    @property
    @pulumi.getter
    def create(self) -> Optional[str]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "create")

    @property
    @pulumi.getter
    def delete(self) -> Optional[str]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        """
        return pulumi.get(self, "delete")

    @property
    @pulumi.getter
    def update(self) -> Optional[str]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "update")


@pulumi.output_type
class PipelineVpcOptions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "subnetIds":
            suggest = "subnet_ids"
        elif key == "securityGroupIds":
            suggest = "security_group_ids"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PipelineVpcOptions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PipelineVpcOptions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PipelineVpcOptions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 subnet_ids: Sequence[str],
                 security_group_ids: Optional[Sequence[str]] = None):
        """
        :param Sequence[str] subnet_ids: A list of subnet IDs associated with the VPC endpoint.
        :param Sequence[str] security_group_ids: A list of security groups associated with the VPC endpoint.
        """
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if security_group_ids is not None:
            pulumi.set(__self__, "security_group_ids", security_group_ids)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        A list of subnet IDs associated with the VPC endpoint.
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Optional[Sequence[str]]:
        """
        A list of security groups associated with the VPC endpoint.
        """
        return pulumi.get(self, "security_group_ids")


