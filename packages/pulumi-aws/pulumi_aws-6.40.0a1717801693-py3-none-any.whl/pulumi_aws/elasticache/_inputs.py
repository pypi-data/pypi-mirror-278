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
    'ClusterCacheNodeArgs',
    'ClusterLogDeliveryConfigurationArgs',
    'GlobalReplicationGroupGlobalNodeGroupArgs',
    'ParameterGroupParameterArgs',
    'ReplicationGroupLogDeliveryConfigurationArgs',
    'ServerlessCacheCacheUsageLimitsArgs',
    'ServerlessCacheCacheUsageLimitsDataStorageArgs',
    'ServerlessCacheCacheUsageLimitsEcpuPerSecondArgs',
    'ServerlessCacheEndpointArgs',
    'ServerlessCacheReaderEndpointArgs',
    'ServerlessCacheTimeoutsArgs',
    'UserAuthenticationModeArgs',
    'GetUserAuthenticationModeArgs',
]

@pulumi.input_type
class ClusterCacheNodeArgs:
    def __init__(__self__, *,
                 address: Optional[pulumi.Input[str]] = None,
                 availability_zone: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 outpost_arn: Optional[pulumi.Input[str]] = None,
                 port: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] availability_zone: Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        :param pulumi.Input[int] port: The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if availability_zone is not None:
            pulumi.set(__self__, "availability_zone", availability_zone)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if outpost_arn is not None:
            pulumi.set(__self__, "outpost_arn", outpost_arn)
        if port is not None:
            pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="availabilityZone")
    def availability_zone(self) -> Optional[pulumi.Input[str]]:
        """
        Availability Zone for the cache cluster. If you want to create cache nodes in multi-az, use `preferred_availability_zones` instead. Default: System chosen Availability Zone. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "availability_zone")

    @availability_zone.setter
    def availability_zone(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "availability_zone", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "outpost_arn")

    @outpost_arn.setter
    def outpost_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "outpost_arn", value)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port number on which each of the cache nodes will accept connections. For Memcached the default is 11211, and for Redis the default port is 6379. Cannot be provided with `replication_group_id`. Changing this value will re-create the resource.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class ClusterLogDeliveryConfigurationArgs:
    def __init__(__self__, *,
                 destination: pulumi.Input[str],
                 destination_type: pulumi.Input[str],
                 log_format: pulumi.Input[str],
                 log_type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] destination: Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        :param pulumi.Input[str] destination_type: For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        :param pulumi.Input[str] log_format: Valid values are `json` or `text`
        :param pulumi.Input[str] log_type: Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Input[str]:
        """
        Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> pulumi.Input[str]:
        """
        For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        """
        return pulumi.get(self, "destination_type")

    @destination_type.setter
    def destination_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_type", value)

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> pulumi.Input[str]:
        """
        Valid values are `json` or `text`
        """
        return pulumi.get(self, "log_format")

    @log_format.setter
    def log_format(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_format", value)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> pulumi.Input[str]:
        """
        Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_type", value)


@pulumi.input_type
class GlobalReplicationGroupGlobalNodeGroupArgs:
    def __init__(__self__, *,
                 global_node_group_id: Optional[pulumi.Input[str]] = None,
                 slots: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] global_node_group_id: The ID of the global node group.
        :param pulumi.Input[str] slots: The keyspace for this node group.
        """
        if global_node_group_id is not None:
            pulumi.set(__self__, "global_node_group_id", global_node_group_id)
        if slots is not None:
            pulumi.set(__self__, "slots", slots)

    @property
    @pulumi.getter(name="globalNodeGroupId")
    def global_node_group_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the global node group.
        """
        return pulumi.get(self, "global_node_group_id")

    @global_node_group_id.setter
    def global_node_group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "global_node_group_id", value)

    @property
    @pulumi.getter
    def slots(self) -> Optional[pulumi.Input[str]]:
        """
        The keyspace for this node group.
        """
        return pulumi.get(self, "slots")

    @slots.setter
    def slots(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "slots", value)


@pulumi.input_type
class ParameterGroupParameterArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] name: The name of the ElastiCache parameter.
        :param pulumi.Input[str] value: The value of the ElastiCache parameter.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the ElastiCache parameter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value of the ElastiCache parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ReplicationGroupLogDeliveryConfigurationArgs:
    def __init__(__self__, *,
                 destination: pulumi.Input[str],
                 destination_type: pulumi.Input[str],
                 log_format: pulumi.Input[str],
                 log_type: pulumi.Input[str]):
        """
        :param pulumi.Input[str] destination: Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        :param pulumi.Input[str] destination_type: For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        :param pulumi.Input[str] log_format: Valid values are `json` or `text`
        :param pulumi.Input[str] log_type: Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        pulumi.set(__self__, "destination", destination)
        pulumi.set(__self__, "destination_type", destination_type)
        pulumi.set(__self__, "log_format", log_format)
        pulumi.set(__self__, "log_type", log_type)

    @property
    @pulumi.getter
    def destination(self) -> pulumi.Input[str]:
        """
        Name of either the CloudWatch Logs LogGroup or Kinesis Data Firehose resource.
        """
        return pulumi.get(self, "destination")

    @destination.setter
    def destination(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination", value)

    @property
    @pulumi.getter(name="destinationType")
    def destination_type(self) -> pulumi.Input[str]:
        """
        For CloudWatch Logs use `cloudwatch-logs` or for Kinesis Data Firehose use `kinesis-firehose`.
        """
        return pulumi.get(self, "destination_type")

    @destination_type.setter
    def destination_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "destination_type", value)

    @property
    @pulumi.getter(name="logFormat")
    def log_format(self) -> pulumi.Input[str]:
        """
        Valid values are `json` or `text`
        """
        return pulumi.get(self, "log_format")

    @log_format.setter
    def log_format(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_format", value)

    @property
    @pulumi.getter(name="logType")
    def log_type(self) -> pulumi.Input[str]:
        """
        Valid values are  `slow-log` or `engine-log`. Max 1 of each.
        """
        return pulumi.get(self, "log_type")

    @log_type.setter
    def log_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_type", value)


@pulumi.input_type
class ServerlessCacheCacheUsageLimitsArgs:
    def __init__(__self__, *,
                 data_storage: Optional[pulumi.Input['ServerlessCacheCacheUsageLimitsDataStorageArgs']] = None,
                 ecpu_per_seconds: Optional[pulumi.Input[Sequence[pulumi.Input['ServerlessCacheCacheUsageLimitsEcpuPerSecondArgs']]]] = None):
        if data_storage is not None:
            pulumi.set(__self__, "data_storage", data_storage)
        if ecpu_per_seconds is not None:
            pulumi.set(__self__, "ecpu_per_seconds", ecpu_per_seconds)

    @property
    @pulumi.getter(name="dataStorage")
    def data_storage(self) -> Optional[pulumi.Input['ServerlessCacheCacheUsageLimitsDataStorageArgs']]:
        return pulumi.get(self, "data_storage")

    @data_storage.setter
    def data_storage(self, value: Optional[pulumi.Input['ServerlessCacheCacheUsageLimitsDataStorageArgs']]):
        pulumi.set(self, "data_storage", value)

    @property
    @pulumi.getter(name="ecpuPerSeconds")
    def ecpu_per_seconds(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ServerlessCacheCacheUsageLimitsEcpuPerSecondArgs']]]]:
        return pulumi.get(self, "ecpu_per_seconds")

    @ecpu_per_seconds.setter
    def ecpu_per_seconds(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ServerlessCacheCacheUsageLimitsEcpuPerSecondArgs']]]]):
        pulumi.set(self, "ecpu_per_seconds", value)


@pulumi.input_type
class ServerlessCacheCacheUsageLimitsDataStorageArgs:
    def __init__(__self__, *,
                 unit: pulumi.Input[str],
                 maximum: Optional[pulumi.Input[int]] = None,
                 minimum: Optional[pulumi.Input[int]] = None):
        pulumi.set(__self__, "unit", unit)
        if maximum is not None:
            pulumi.set(__self__, "maximum", maximum)
        if minimum is not None:
            pulumi.set(__self__, "minimum", minimum)

    @property
    @pulumi.getter
    def unit(self) -> pulumi.Input[str]:
        return pulumi.get(self, "unit")

    @unit.setter
    def unit(self, value: pulumi.Input[str]):
        pulumi.set(self, "unit", value)

    @property
    @pulumi.getter
    def maximum(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "maximum")

    @maximum.setter
    def maximum(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "maximum", value)

    @property
    @pulumi.getter
    def minimum(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "minimum")

    @minimum.setter
    def minimum(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "minimum", value)


@pulumi.input_type
class ServerlessCacheCacheUsageLimitsEcpuPerSecondArgs:
    def __init__(__self__, *,
                 maximum: Optional[pulumi.Input[int]] = None,
                 minimum: Optional[pulumi.Input[int]] = None):
        if maximum is not None:
            pulumi.set(__self__, "maximum", maximum)
        if minimum is not None:
            pulumi.set(__self__, "minimum", minimum)

    @property
    @pulumi.getter
    def maximum(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "maximum")

    @maximum.setter
    def maximum(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "maximum", value)

    @property
    @pulumi.getter
    def minimum(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "minimum")

    @minimum.setter
    def minimum(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "minimum", value)


@pulumi.input_type
class ServerlessCacheEndpointArgs:
    def __init__(__self__, *,
                 address: pulumi.Input[str],
                 port: pulumi.Input[int]):
        """
        :param pulumi.Input[str] address: The DNS hostname of the cache node.
        :param pulumi.Input[int] port: The port number that the cache engine is listening on. Set as integer.
        """
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Input[str]:
        """
        The DNS hostname of the cache node.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: pulumi.Input[str]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The port number that the cache engine is listening on. Set as integer.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class ServerlessCacheReaderEndpointArgs:
    def __init__(__self__, *,
                 address: pulumi.Input[str],
                 port: pulumi.Input[int]):
        """
        :param pulumi.Input[str] address: The DNS hostname of the cache node.
        :param pulumi.Input[int] port: The port number that the cache engine is listening on. Set as integer.
        """
        pulumi.set(__self__, "address", address)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def address(self) -> pulumi.Input[str]:
        """
        The DNS hostname of the cache node.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: pulumi.Input[str]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The port number that the cache engine is listening on. Set as integer.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class ServerlessCacheTimeoutsArgs:
    def __init__(__self__, *,
                 create: Optional[pulumi.Input[str]] = None,
                 delete: Optional[pulumi.Input[str]] = None,
                 update: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] create: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        :param pulumi.Input[str] delete: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        :param pulumi.Input[str] update: A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        if create is not None:
            pulumi.set(__self__, "create", create)
        if delete is not None:
            pulumi.set(__self__, "delete", delete)
        if update is not None:
            pulumi.set(__self__, "update", update)

    @property
    @pulumi.getter
    def create(self) -> Optional[pulumi.Input[str]]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "create")

    @create.setter
    def create(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "create", value)

    @property
    @pulumi.getter
    def delete(self) -> Optional[pulumi.Input[str]]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours). Setting a timeout for a Delete operation is only applicable if changes are saved into state before the destroy operation occurs.
        """
        return pulumi.get(self, "delete")

    @delete.setter
    def delete(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "delete", value)

    @property
    @pulumi.getter
    def update(self) -> Optional[pulumi.Input[str]]:
        """
        A string that can be [parsed as a duration](https://pkg.go.dev/time#ParseDuration) consisting of numbers and unit suffixes, such as "30s" or "2h45m". Valid time units are "s" (seconds), "m" (minutes), "h" (hours).
        """
        return pulumi.get(self, "update")

    @update.setter
    def update(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "update", value)


@pulumi.input_type
class UserAuthenticationModeArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 password_count: Optional[pulumi.Input[int]] = None,
                 passwords: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] type: Specifies the authentication type. Possible options are: `password`, `no-password-required` or `iam`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] passwords: Specifies the passwords to use for authentication if `type` is set to `password`.
        """
        pulumi.set(__self__, "type", type)
        if password_count is not None:
            pulumi.set(__self__, "password_count", password_count)
        if passwords is not None:
            pulumi.set(__self__, "passwords", passwords)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        Specifies the authentication type. Possible options are: `password`, `no-password-required` or `iam`.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="passwordCount")
    def password_count(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "password_count")

    @password_count.setter
    def password_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "password_count", value)

    @property
    @pulumi.getter
    def passwords(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Specifies the passwords to use for authentication if `type` is set to `password`.
        """
        return pulumi.get(self, "passwords")

    @passwords.setter
    def passwords(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "passwords", value)


@pulumi.input_type
class GetUserAuthenticationModeArgs:
    def __init__(__self__, *,
                 password_count: Optional[int] = None,
                 type: Optional[str] = None):
        if password_count is not None:
            pulumi.set(__self__, "password_count", password_count)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="passwordCount")
    def password_count(self) -> Optional[int]:
        return pulumi.get(self, "password_count")

    @password_count.setter
    def password_count(self, value: Optional[int]):
        pulumi.set(self, "password_count", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[str]):
        pulumi.set(self, "type", value)


