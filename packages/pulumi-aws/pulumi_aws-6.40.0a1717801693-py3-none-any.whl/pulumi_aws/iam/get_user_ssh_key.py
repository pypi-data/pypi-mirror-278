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
    'GetUserSshKeyResult',
    'AwaitableGetUserSshKeyResult',
    'get_user_ssh_key',
    'get_user_ssh_key_output',
]

@pulumi.output_type
class GetUserSshKeyResult:
    """
    A collection of values returned by getUserSshKey.
    """
    def __init__(__self__, encoding=None, fingerprint=None, id=None, public_key=None, ssh_public_key_id=None, status=None, username=None):
        if encoding and not isinstance(encoding, str):
            raise TypeError("Expected argument 'encoding' to be a str")
        pulumi.set(__self__, "encoding", encoding)
        if fingerprint and not isinstance(fingerprint, str):
            raise TypeError("Expected argument 'fingerprint' to be a str")
        pulumi.set(__self__, "fingerprint", fingerprint)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if public_key and not isinstance(public_key, str):
            raise TypeError("Expected argument 'public_key' to be a str")
        pulumi.set(__self__, "public_key", public_key)
        if ssh_public_key_id and not isinstance(ssh_public_key_id, str):
            raise TypeError("Expected argument 'ssh_public_key_id' to be a str")
        pulumi.set(__self__, "ssh_public_key_id", ssh_public_key_id)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if username and not isinstance(username, str):
            raise TypeError("Expected argument 'username' to be a str")
        pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def encoding(self) -> str:
        return pulumi.get(self, "encoding")

    @property
    @pulumi.getter
    def fingerprint(self) -> str:
        """
        MD5 message digest of the SSH public key.
        """
        return pulumi.get(self, "fingerprint")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> str:
        """
        SSH public key.
        """
        return pulumi.get(self, "public_key")

    @property
    @pulumi.getter(name="sshPublicKeyId")
    def ssh_public_key_id(self) -> str:
        return pulumi.get(self, "ssh_public_key_id")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the SSH public key. Active means that the key can be used for authentication with an CodeCommit repository. Inactive means that the key cannot be used.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def username(self) -> str:
        return pulumi.get(self, "username")


class AwaitableGetUserSshKeyResult(GetUserSshKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUserSshKeyResult(
            encoding=self.encoding,
            fingerprint=self.fingerprint,
            id=self.id,
            public_key=self.public_key,
            ssh_public_key_id=self.ssh_public_key_id,
            status=self.status,
            username=self.username)


def get_user_ssh_key(encoding: Optional[str] = None,
                     ssh_public_key_id: Optional[str] = None,
                     username: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUserSshKeyResult:
    """
    Use this data source to get information about a SSH public key associated with the specified IAM user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_user_ssh_key(encoding="SSH",
        ssh_public_key_id="APKARUZ32GUTKIGARLXE",
        username="test-user")
    ```


    :param str encoding: Specifies the public key encoding format to use in the response. To retrieve the public key in ssh-rsa format, use `SSH`. To retrieve the public key in PEM format, use `PEM`.
    :param str ssh_public_key_id: Unique identifier for the SSH public key.
    :param str username: Name of the IAM user associated with the SSH public key.
    """
    __args__ = dict()
    __args__['encoding'] = encoding
    __args__['sshPublicKeyId'] = ssh_public_key_id
    __args__['username'] = username
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:iam/getUserSshKey:getUserSshKey', __args__, opts=opts, typ=GetUserSshKeyResult).value

    return AwaitableGetUserSshKeyResult(
        encoding=pulumi.get(__ret__, 'encoding'),
        fingerprint=pulumi.get(__ret__, 'fingerprint'),
        id=pulumi.get(__ret__, 'id'),
        public_key=pulumi.get(__ret__, 'public_key'),
        ssh_public_key_id=pulumi.get(__ret__, 'ssh_public_key_id'),
        status=pulumi.get(__ret__, 'status'),
        username=pulumi.get(__ret__, 'username'))


@_utilities.lift_output_func(get_user_ssh_key)
def get_user_ssh_key_output(encoding: Optional[pulumi.Input[str]] = None,
                            ssh_public_key_id: Optional[pulumi.Input[str]] = None,
                            username: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUserSshKeyResult]:
    """
    Use this data source to get information about a SSH public key associated with the specified IAM user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.iam.get_user_ssh_key(encoding="SSH",
        ssh_public_key_id="APKARUZ32GUTKIGARLXE",
        username="test-user")
    ```


    :param str encoding: Specifies the public key encoding format to use in the response. To retrieve the public key in ssh-rsa format, use `SSH`. To retrieve the public key in PEM format, use `PEM`.
    :param str ssh_public_key_id: Unique identifier for the SSH public key.
    :param str username: Name of the IAM user associated with the SSH public key.
    """
    ...
