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
    'ConnectionAliasTimeouts',
    'DirectorySelfServicePermissions',
    'DirectoryWorkspaceAccessProperties',
    'DirectoryWorkspaceCreationProperties',
    'IpGroupRule',
    'WorkspaceWorkspaceProperties',
    'GetBundleComputeTypeResult',
    'GetBundleRootStorageResult',
    'GetBundleUserStorageResult',
    'GetDirectorySelfServicePermissionResult',
    'GetDirectoryWorkspaceAccessPropertyResult',
    'GetDirectoryWorkspaceCreationPropertyResult',
    'GetWorkspaceWorkspacePropertyResult',
]

@pulumi.output_type
class ConnectionAliasTimeouts(dict):
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
class DirectorySelfServicePermissions(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "changeComputeType":
            suggest = "change_compute_type"
        elif key == "increaseVolumeSize":
            suggest = "increase_volume_size"
        elif key == "rebuildWorkspace":
            suggest = "rebuild_workspace"
        elif key == "restartWorkspace":
            suggest = "restart_workspace"
        elif key == "switchRunningMode":
            suggest = "switch_running_mode"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DirectorySelfServicePermissions. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DirectorySelfServicePermissions.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DirectorySelfServicePermissions.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 change_compute_type: Optional[bool] = None,
                 increase_volume_size: Optional[bool] = None,
                 rebuild_workspace: Optional[bool] = None,
                 restart_workspace: Optional[bool] = None,
                 switch_running_mode: Optional[bool] = None):
        """
        :param bool change_compute_type: Whether WorkSpaces directory users can change the compute type (bundle) for their workspace. Default `false`.
        :param bool increase_volume_size: Whether WorkSpaces directory users can increase the volume size of the drives on their workspace. Default `false`.
        :param bool rebuild_workspace: Whether WorkSpaces directory users can rebuild the operating system of a workspace to its original state. Default `false`.
        :param bool restart_workspace: Whether WorkSpaces directory users can restart their workspace. Default `true`.
        :param bool switch_running_mode: Whether WorkSpaces directory users can switch the running mode of their workspace. Default `false`.
        """
        if change_compute_type is not None:
            pulumi.set(__self__, "change_compute_type", change_compute_type)
        if increase_volume_size is not None:
            pulumi.set(__self__, "increase_volume_size", increase_volume_size)
        if rebuild_workspace is not None:
            pulumi.set(__self__, "rebuild_workspace", rebuild_workspace)
        if restart_workspace is not None:
            pulumi.set(__self__, "restart_workspace", restart_workspace)
        if switch_running_mode is not None:
            pulumi.set(__self__, "switch_running_mode", switch_running_mode)

    @property
    @pulumi.getter(name="changeComputeType")
    def change_compute_type(self) -> Optional[bool]:
        """
        Whether WorkSpaces directory users can change the compute type (bundle) for their workspace. Default `false`.
        """
        return pulumi.get(self, "change_compute_type")

    @property
    @pulumi.getter(name="increaseVolumeSize")
    def increase_volume_size(self) -> Optional[bool]:
        """
        Whether WorkSpaces directory users can increase the volume size of the drives on their workspace. Default `false`.
        """
        return pulumi.get(self, "increase_volume_size")

    @property
    @pulumi.getter(name="rebuildWorkspace")
    def rebuild_workspace(self) -> Optional[bool]:
        """
        Whether WorkSpaces directory users can rebuild the operating system of a workspace to its original state. Default `false`.
        """
        return pulumi.get(self, "rebuild_workspace")

    @property
    @pulumi.getter(name="restartWorkspace")
    def restart_workspace(self) -> Optional[bool]:
        """
        Whether WorkSpaces directory users can restart their workspace. Default `true`.
        """
        return pulumi.get(self, "restart_workspace")

    @property
    @pulumi.getter(name="switchRunningMode")
    def switch_running_mode(self) -> Optional[bool]:
        """
        Whether WorkSpaces directory users can switch the running mode of their workspace. Default `false`.
        """
        return pulumi.get(self, "switch_running_mode")


@pulumi.output_type
class DirectoryWorkspaceAccessProperties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "deviceTypeAndroid":
            suggest = "device_type_android"
        elif key == "deviceTypeChromeos":
            suggest = "device_type_chromeos"
        elif key == "deviceTypeIos":
            suggest = "device_type_ios"
        elif key == "deviceTypeLinux":
            suggest = "device_type_linux"
        elif key == "deviceTypeOsx":
            suggest = "device_type_osx"
        elif key == "deviceTypeWeb":
            suggest = "device_type_web"
        elif key == "deviceTypeWindows":
            suggest = "device_type_windows"
        elif key == "deviceTypeZeroclient":
            suggest = "device_type_zeroclient"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DirectoryWorkspaceAccessProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DirectoryWorkspaceAccessProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DirectoryWorkspaceAccessProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 device_type_android: Optional[str] = None,
                 device_type_chromeos: Optional[str] = None,
                 device_type_ios: Optional[str] = None,
                 device_type_linux: Optional[str] = None,
                 device_type_osx: Optional[str] = None,
                 device_type_web: Optional[str] = None,
                 device_type_windows: Optional[str] = None,
                 device_type_zeroclient: Optional[str] = None):
        """
        :param str device_type_android: Indicates whether users can use Android devices to access their WorkSpaces.
        :param str device_type_chromeos: Indicates whether users can use Chromebooks to access their WorkSpaces.
        :param str device_type_ios: Indicates whether users can use iOS devices to access their WorkSpaces.
        :param str device_type_linux: Indicates whether users can use Linux clients to access their WorkSpaces.
        :param str device_type_osx: Indicates whether users can use macOS clients to access their WorkSpaces.
        :param str device_type_web: Indicates whether users can access their WorkSpaces through a web browser.
        :param str device_type_windows: Indicates whether users can use Windows clients to access their WorkSpaces.
        :param str device_type_zeroclient: Indicates whether users can use zero client devices to access their WorkSpaces.
        """
        if device_type_android is not None:
            pulumi.set(__self__, "device_type_android", device_type_android)
        if device_type_chromeos is not None:
            pulumi.set(__self__, "device_type_chromeos", device_type_chromeos)
        if device_type_ios is not None:
            pulumi.set(__self__, "device_type_ios", device_type_ios)
        if device_type_linux is not None:
            pulumi.set(__self__, "device_type_linux", device_type_linux)
        if device_type_osx is not None:
            pulumi.set(__self__, "device_type_osx", device_type_osx)
        if device_type_web is not None:
            pulumi.set(__self__, "device_type_web", device_type_web)
        if device_type_windows is not None:
            pulumi.set(__self__, "device_type_windows", device_type_windows)
        if device_type_zeroclient is not None:
            pulumi.set(__self__, "device_type_zeroclient", device_type_zeroclient)

    @property
    @pulumi.getter(name="deviceTypeAndroid")
    def device_type_android(self) -> Optional[str]:
        """
        Indicates whether users can use Android devices to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_android")

    @property
    @pulumi.getter(name="deviceTypeChromeos")
    def device_type_chromeos(self) -> Optional[str]:
        """
        Indicates whether users can use Chromebooks to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_chromeos")

    @property
    @pulumi.getter(name="deviceTypeIos")
    def device_type_ios(self) -> Optional[str]:
        """
        Indicates whether users can use iOS devices to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_ios")

    @property
    @pulumi.getter(name="deviceTypeLinux")
    def device_type_linux(self) -> Optional[str]:
        """
        Indicates whether users can use Linux clients to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_linux")

    @property
    @pulumi.getter(name="deviceTypeOsx")
    def device_type_osx(self) -> Optional[str]:
        """
        Indicates whether users can use macOS clients to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_osx")

    @property
    @pulumi.getter(name="deviceTypeWeb")
    def device_type_web(self) -> Optional[str]:
        """
        Indicates whether users can access their WorkSpaces through a web browser.
        """
        return pulumi.get(self, "device_type_web")

    @property
    @pulumi.getter(name="deviceTypeWindows")
    def device_type_windows(self) -> Optional[str]:
        """
        Indicates whether users can use Windows clients to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_windows")

    @property
    @pulumi.getter(name="deviceTypeZeroclient")
    def device_type_zeroclient(self) -> Optional[str]:
        """
        Indicates whether users can use zero client devices to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_zeroclient")


@pulumi.output_type
class DirectoryWorkspaceCreationProperties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "customSecurityGroupId":
            suggest = "custom_security_group_id"
        elif key == "defaultOu":
            suggest = "default_ou"
        elif key == "enableInternetAccess":
            suggest = "enable_internet_access"
        elif key == "enableMaintenanceMode":
            suggest = "enable_maintenance_mode"
        elif key == "userEnabledAsLocalAdministrator":
            suggest = "user_enabled_as_local_administrator"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in DirectoryWorkspaceCreationProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        DirectoryWorkspaceCreationProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        DirectoryWorkspaceCreationProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 custom_security_group_id: Optional[str] = None,
                 default_ou: Optional[str] = None,
                 enable_internet_access: Optional[bool] = None,
                 enable_maintenance_mode: Optional[bool] = None,
                 user_enabled_as_local_administrator: Optional[bool] = None):
        """
        :param str custom_security_group_id: The identifier of your custom security group. Should relate to the same VPC, where workspaces reside in.
        :param str default_ou: The default organizational unit (OU) for your WorkSpace directories. Should conform `"OU=<value>,DC=<value>,...,DC=<value>"` pattern.
        :param bool enable_internet_access: Indicates whether internet access is enabled for your WorkSpaces.
        :param bool enable_maintenance_mode: Indicates whether maintenance mode is enabled for your WorkSpaces. For more information, see [WorkSpace Maintenance](https://docs.aws.amazon.com/workspaces/latest/adminguide/workspace-maintenance.html)..
        :param bool user_enabled_as_local_administrator: Indicates whether users are local administrators of their WorkSpaces.
        """
        if custom_security_group_id is not None:
            pulumi.set(__self__, "custom_security_group_id", custom_security_group_id)
        if default_ou is not None:
            pulumi.set(__self__, "default_ou", default_ou)
        if enable_internet_access is not None:
            pulumi.set(__self__, "enable_internet_access", enable_internet_access)
        if enable_maintenance_mode is not None:
            pulumi.set(__self__, "enable_maintenance_mode", enable_maintenance_mode)
        if user_enabled_as_local_administrator is not None:
            pulumi.set(__self__, "user_enabled_as_local_administrator", user_enabled_as_local_administrator)

    @property
    @pulumi.getter(name="customSecurityGroupId")
    def custom_security_group_id(self) -> Optional[str]:
        """
        The identifier of your custom security group. Should relate to the same VPC, where workspaces reside in.
        """
        return pulumi.get(self, "custom_security_group_id")

    @property
    @pulumi.getter(name="defaultOu")
    def default_ou(self) -> Optional[str]:
        """
        The default organizational unit (OU) for your WorkSpace directories. Should conform `"OU=<value>,DC=<value>,...,DC=<value>"` pattern.
        """
        return pulumi.get(self, "default_ou")

    @property
    @pulumi.getter(name="enableInternetAccess")
    def enable_internet_access(self) -> Optional[bool]:
        """
        Indicates whether internet access is enabled for your WorkSpaces.
        """
        return pulumi.get(self, "enable_internet_access")

    @property
    @pulumi.getter(name="enableMaintenanceMode")
    def enable_maintenance_mode(self) -> Optional[bool]:
        """
        Indicates whether maintenance mode is enabled for your WorkSpaces. For more information, see [WorkSpace Maintenance](https://docs.aws.amazon.com/workspaces/latest/adminguide/workspace-maintenance.html)..
        """
        return pulumi.get(self, "enable_maintenance_mode")

    @property
    @pulumi.getter(name="userEnabledAsLocalAdministrator")
    def user_enabled_as_local_administrator(self) -> Optional[bool]:
        """
        Indicates whether users are local administrators of their WorkSpaces.
        """
        return pulumi.get(self, "user_enabled_as_local_administrator")


@pulumi.output_type
class IpGroupRule(dict):
    def __init__(__self__, *,
                 source: str,
                 description: Optional[str] = None):
        """
        :param str description: The description of the IP group.
        """
        pulumi.set(__self__, "source", source)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def source(self) -> str:
        return pulumi.get(self, "source")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        The description of the IP group.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class WorkspaceWorkspaceProperties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "computeTypeName":
            suggest = "compute_type_name"
        elif key == "rootVolumeSizeGib":
            suggest = "root_volume_size_gib"
        elif key == "runningMode":
            suggest = "running_mode"
        elif key == "runningModeAutoStopTimeoutInMinutes":
            suggest = "running_mode_auto_stop_timeout_in_minutes"
        elif key == "userVolumeSizeGib":
            suggest = "user_volume_size_gib"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in WorkspaceWorkspaceProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        WorkspaceWorkspaceProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        WorkspaceWorkspaceProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 compute_type_name: Optional[str] = None,
                 root_volume_size_gib: Optional[int] = None,
                 running_mode: Optional[str] = None,
                 running_mode_auto_stop_timeout_in_minutes: Optional[int] = None,
                 user_volume_size_gib: Optional[int] = None):
        """
        :param str compute_type_name: The compute type. For more information, see [Amazon WorkSpaces Bundles](http://aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles). Valid values are `VALUE`, `STANDARD`, `PERFORMANCE`, `POWER`, `GRAPHICS`, `POWERPRO`, `GRAPHICSPRO`, `GRAPHICS_G4DN`, and `GRAPHICSPRO_G4DN`.
        :param int root_volume_size_gib: The size of the root volume.
        :param str running_mode: The running mode. For more information, see [Manage the WorkSpace Running Mode](https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html). Valid values are `AUTO_STOP` and `ALWAYS_ON`.
        :param int running_mode_auto_stop_timeout_in_minutes: The time after a user logs off when WorkSpaces are automatically stopped. Configured in 60-minute intervals.
        :param int user_volume_size_gib: The size of the user storage.
        """
        if compute_type_name is not None:
            pulumi.set(__self__, "compute_type_name", compute_type_name)
        if root_volume_size_gib is not None:
            pulumi.set(__self__, "root_volume_size_gib", root_volume_size_gib)
        if running_mode is not None:
            pulumi.set(__self__, "running_mode", running_mode)
        if running_mode_auto_stop_timeout_in_minutes is not None:
            pulumi.set(__self__, "running_mode_auto_stop_timeout_in_minutes", running_mode_auto_stop_timeout_in_minutes)
        if user_volume_size_gib is not None:
            pulumi.set(__self__, "user_volume_size_gib", user_volume_size_gib)

    @property
    @pulumi.getter(name="computeTypeName")
    def compute_type_name(self) -> Optional[str]:
        """
        The compute type. For more information, see [Amazon WorkSpaces Bundles](http://aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles). Valid values are `VALUE`, `STANDARD`, `PERFORMANCE`, `POWER`, `GRAPHICS`, `POWERPRO`, `GRAPHICSPRO`, `GRAPHICS_G4DN`, and `GRAPHICSPRO_G4DN`.
        """
        return pulumi.get(self, "compute_type_name")

    @property
    @pulumi.getter(name="rootVolumeSizeGib")
    def root_volume_size_gib(self) -> Optional[int]:
        """
        The size of the root volume.
        """
        return pulumi.get(self, "root_volume_size_gib")

    @property
    @pulumi.getter(name="runningMode")
    def running_mode(self) -> Optional[str]:
        """
        The running mode. For more information, see [Manage the WorkSpace Running Mode](https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html). Valid values are `AUTO_STOP` and `ALWAYS_ON`.
        """
        return pulumi.get(self, "running_mode")

    @property
    @pulumi.getter(name="runningModeAutoStopTimeoutInMinutes")
    def running_mode_auto_stop_timeout_in_minutes(self) -> Optional[int]:
        """
        The time after a user logs off when WorkSpaces are automatically stopped. Configured in 60-minute intervals.
        """
        return pulumi.get(self, "running_mode_auto_stop_timeout_in_minutes")

    @property
    @pulumi.getter(name="userVolumeSizeGib")
    def user_volume_size_gib(self) -> Optional[int]:
        """
        The size of the user storage.
        """
        return pulumi.get(self, "user_volume_size_gib")


@pulumi.output_type
class GetBundleComputeTypeResult(dict):
    def __init__(__self__, *,
                 name: str):
        """
        :param str name: Name of the bundle. You cannot combine this parameter with `bundle_id`.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the bundle. You cannot combine this parameter with `bundle_id`.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class GetBundleRootStorageResult(dict):
    def __init__(__self__, *,
                 capacity: str):
        """
        :param str capacity: Size of the user storage.
        """
        pulumi.set(__self__, "capacity", capacity)

    @property
    @pulumi.getter
    def capacity(self) -> str:
        """
        Size of the user storage.
        """
        return pulumi.get(self, "capacity")


@pulumi.output_type
class GetBundleUserStorageResult(dict):
    def __init__(__self__, *,
                 capacity: str):
        """
        :param str capacity: Size of the user storage.
        """
        pulumi.set(__self__, "capacity", capacity)

    @property
    @pulumi.getter
    def capacity(self) -> str:
        """
        Size of the user storage.
        """
        return pulumi.get(self, "capacity")


@pulumi.output_type
class GetDirectorySelfServicePermissionResult(dict):
    def __init__(__self__, *,
                 change_compute_type: bool,
                 increase_volume_size: bool,
                 rebuild_workspace: bool,
                 restart_workspace: bool,
                 switch_running_mode: bool):
        """
        :param bool change_compute_type: Whether WorkSpaces directory users can change the compute type (bundle) for their workspace.
        :param bool increase_volume_size: Whether WorkSpaces directory users can increase the volume size of the drives on their workspace.
        :param bool rebuild_workspace: Whether WorkSpaces directory users can rebuild the operating system of a workspace to its original state.
        :param bool restart_workspace: Whether WorkSpaces directory users can restart their workspace.
        :param bool switch_running_mode: Whether WorkSpaces directory users can switch the running mode of their workspace.
        """
        pulumi.set(__self__, "change_compute_type", change_compute_type)
        pulumi.set(__self__, "increase_volume_size", increase_volume_size)
        pulumi.set(__self__, "rebuild_workspace", rebuild_workspace)
        pulumi.set(__self__, "restart_workspace", restart_workspace)
        pulumi.set(__self__, "switch_running_mode", switch_running_mode)

    @property
    @pulumi.getter(name="changeComputeType")
    def change_compute_type(self) -> bool:
        """
        Whether WorkSpaces directory users can change the compute type (bundle) for their workspace.
        """
        return pulumi.get(self, "change_compute_type")

    @property
    @pulumi.getter(name="increaseVolumeSize")
    def increase_volume_size(self) -> bool:
        """
        Whether WorkSpaces directory users can increase the volume size of the drives on their workspace.
        """
        return pulumi.get(self, "increase_volume_size")

    @property
    @pulumi.getter(name="rebuildWorkspace")
    def rebuild_workspace(self) -> bool:
        """
        Whether WorkSpaces directory users can rebuild the operating system of a workspace to its original state.
        """
        return pulumi.get(self, "rebuild_workspace")

    @property
    @pulumi.getter(name="restartWorkspace")
    def restart_workspace(self) -> bool:
        """
        Whether WorkSpaces directory users can restart their workspace.
        """
        return pulumi.get(self, "restart_workspace")

    @property
    @pulumi.getter(name="switchRunningMode")
    def switch_running_mode(self) -> bool:
        """
        Whether WorkSpaces directory users can switch the running mode of their workspace.
        """
        return pulumi.get(self, "switch_running_mode")


@pulumi.output_type
class GetDirectoryWorkspaceAccessPropertyResult(dict):
    def __init__(__self__, *,
                 device_type_android: str,
                 device_type_chromeos: str,
                 device_type_ios: str,
                 device_type_linux: str,
                 device_type_osx: str,
                 device_type_web: str,
                 device_type_windows: str,
                 device_type_zeroclient: str):
        """
        :param str device_type_android: (Optional) Indicates whether users can use Android devices to access their WorkSpaces.
        :param str device_type_chromeos: (Optional) Indicates whether users can use Chromebooks to access their WorkSpaces.
        :param str device_type_ios: (Optional) Indicates whether users can use iOS devices to access their WorkSpaces.
        :param str device_type_linux: (Optional) Indicates whether users can use Linux clients to access their WorkSpaces.
        :param str device_type_osx: (Optional) Indicates whether users can use macOS clients to access their WorkSpaces.
        :param str device_type_web: (Optional) Indicates whether users can access their WorkSpaces through a web browser.
        :param str device_type_windows: (Optional) Indicates whether users can use Windows clients to access their WorkSpaces.
        :param str device_type_zeroclient: (Optional) Indicates whether users can use zero client devices to access their WorkSpaces.
        """
        pulumi.set(__self__, "device_type_android", device_type_android)
        pulumi.set(__self__, "device_type_chromeos", device_type_chromeos)
        pulumi.set(__self__, "device_type_ios", device_type_ios)
        pulumi.set(__self__, "device_type_linux", device_type_linux)
        pulumi.set(__self__, "device_type_osx", device_type_osx)
        pulumi.set(__self__, "device_type_web", device_type_web)
        pulumi.set(__self__, "device_type_windows", device_type_windows)
        pulumi.set(__self__, "device_type_zeroclient", device_type_zeroclient)

    @property
    @pulumi.getter(name="deviceTypeAndroid")
    def device_type_android(self) -> str:
        """
        (Optional) Indicates whether users can use Android devices to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_android")

    @property
    @pulumi.getter(name="deviceTypeChromeos")
    def device_type_chromeos(self) -> str:
        """
        (Optional) Indicates whether users can use Chromebooks to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_chromeos")

    @property
    @pulumi.getter(name="deviceTypeIos")
    def device_type_ios(self) -> str:
        """
        (Optional) Indicates whether users can use iOS devices to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_ios")

    @property
    @pulumi.getter(name="deviceTypeLinux")
    def device_type_linux(self) -> str:
        """
        (Optional) Indicates whether users can use Linux clients to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_linux")

    @property
    @pulumi.getter(name="deviceTypeOsx")
    def device_type_osx(self) -> str:
        """
        (Optional) Indicates whether users can use macOS clients to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_osx")

    @property
    @pulumi.getter(name="deviceTypeWeb")
    def device_type_web(self) -> str:
        """
        (Optional) Indicates whether users can access their WorkSpaces through a web browser.
        """
        return pulumi.get(self, "device_type_web")

    @property
    @pulumi.getter(name="deviceTypeWindows")
    def device_type_windows(self) -> str:
        """
        (Optional) Indicates whether users can use Windows clients to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_windows")

    @property
    @pulumi.getter(name="deviceTypeZeroclient")
    def device_type_zeroclient(self) -> str:
        """
        (Optional) Indicates whether users can use zero client devices to access their WorkSpaces.
        """
        return pulumi.get(self, "device_type_zeroclient")


@pulumi.output_type
class GetDirectoryWorkspaceCreationPropertyResult(dict):
    def __init__(__self__, *,
                 custom_security_group_id: str,
                 default_ou: str,
                 enable_internet_access: bool,
                 enable_maintenance_mode: bool,
                 user_enabled_as_local_administrator: bool):
        """
        :param str custom_security_group_id: The identifier of your custom security group. Should relate to the same VPC, where workspaces reside in.
        :param str default_ou: The default organizational unit (OU) for your WorkSpace directories.
        :param bool enable_internet_access: Indicates whether internet access is enabled for your WorkSpaces.
        :param bool enable_maintenance_mode: Indicates whether maintenance mode is enabled for your WorkSpaces. For more information, see [WorkSpace Maintenance](https://docs.aws.amazon.com/workspaces/latest/adminguide/workspace-maintenance.html).
        :param bool user_enabled_as_local_administrator: Indicates whether users are local administrators of their WorkSpaces.
        """
        pulumi.set(__self__, "custom_security_group_id", custom_security_group_id)
        pulumi.set(__self__, "default_ou", default_ou)
        pulumi.set(__self__, "enable_internet_access", enable_internet_access)
        pulumi.set(__self__, "enable_maintenance_mode", enable_maintenance_mode)
        pulumi.set(__self__, "user_enabled_as_local_administrator", user_enabled_as_local_administrator)

    @property
    @pulumi.getter(name="customSecurityGroupId")
    def custom_security_group_id(self) -> str:
        """
        The identifier of your custom security group. Should relate to the same VPC, where workspaces reside in.
        """
        return pulumi.get(self, "custom_security_group_id")

    @property
    @pulumi.getter(name="defaultOu")
    def default_ou(self) -> str:
        """
        The default organizational unit (OU) for your WorkSpace directories.
        """
        return pulumi.get(self, "default_ou")

    @property
    @pulumi.getter(name="enableInternetAccess")
    def enable_internet_access(self) -> bool:
        """
        Indicates whether internet access is enabled for your WorkSpaces.
        """
        return pulumi.get(self, "enable_internet_access")

    @property
    @pulumi.getter(name="enableMaintenanceMode")
    def enable_maintenance_mode(self) -> bool:
        """
        Indicates whether maintenance mode is enabled for your WorkSpaces. For more information, see [WorkSpace Maintenance](https://docs.aws.amazon.com/workspaces/latest/adminguide/workspace-maintenance.html).
        """
        return pulumi.get(self, "enable_maintenance_mode")

    @property
    @pulumi.getter(name="userEnabledAsLocalAdministrator")
    def user_enabled_as_local_administrator(self) -> bool:
        """
        Indicates whether users are local administrators of their WorkSpaces.
        """
        return pulumi.get(self, "user_enabled_as_local_administrator")


@pulumi.output_type
class GetWorkspaceWorkspacePropertyResult(dict):
    def __init__(__self__, *,
                 compute_type_name: str,
                 root_volume_size_gib: int,
                 running_mode: str,
                 running_mode_auto_stop_timeout_in_minutes: int,
                 user_volume_size_gib: int):
        """
        :param str compute_type_name: Compute type. For more information, see [Amazon WorkSpaces Bundles](http://aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles). Valid values are `VALUE`, `STANDARD`, `PERFORMANCE`, `POWER`, `GRAPHICS`, `POWERPRO` and `GRAPHICSPRO`.
        :param int root_volume_size_gib: Size of the root volume.
        :param str running_mode: Running mode. For more information, see [Manage the WorkSpace Running Mode](https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html). Valid values are `AUTO_STOP` and `ALWAYS_ON`.
        :param int running_mode_auto_stop_timeout_in_minutes: Time after a user logs off when WorkSpaces are automatically stopped. Configured in 60-minute intervals.
        :param int user_volume_size_gib: Size of the user storage.
        """
        pulumi.set(__self__, "compute_type_name", compute_type_name)
        pulumi.set(__self__, "root_volume_size_gib", root_volume_size_gib)
        pulumi.set(__self__, "running_mode", running_mode)
        pulumi.set(__self__, "running_mode_auto_stop_timeout_in_minutes", running_mode_auto_stop_timeout_in_minutes)
        pulumi.set(__self__, "user_volume_size_gib", user_volume_size_gib)

    @property
    @pulumi.getter(name="computeTypeName")
    def compute_type_name(self) -> str:
        """
        Compute type. For more information, see [Amazon WorkSpaces Bundles](http://aws.amazon.com/workspaces/details/#Amazon_WorkSpaces_Bundles). Valid values are `VALUE`, `STANDARD`, `PERFORMANCE`, `POWER`, `GRAPHICS`, `POWERPRO` and `GRAPHICSPRO`.
        """
        return pulumi.get(self, "compute_type_name")

    @property
    @pulumi.getter(name="rootVolumeSizeGib")
    def root_volume_size_gib(self) -> int:
        """
        Size of the root volume.
        """
        return pulumi.get(self, "root_volume_size_gib")

    @property
    @pulumi.getter(name="runningMode")
    def running_mode(self) -> str:
        """
        Running mode. For more information, see [Manage the WorkSpace Running Mode](https://docs.aws.amazon.com/workspaces/latest/adminguide/running-mode.html). Valid values are `AUTO_STOP` and `ALWAYS_ON`.
        """
        return pulumi.get(self, "running_mode")

    @property
    @pulumi.getter(name="runningModeAutoStopTimeoutInMinutes")
    def running_mode_auto_stop_timeout_in_minutes(self) -> int:
        """
        Time after a user logs off when WorkSpaces are automatically stopped. Configured in 60-minute intervals.
        """
        return pulumi.get(self, "running_mode_auto_stop_timeout_in_minutes")

    @property
    @pulumi.getter(name="userVolumeSizeGib")
    def user_volume_size_gib(self) -> int:
        """
        Size of the user storage.
        """
        return pulumi.get(self, "user_volume_size_gib")


