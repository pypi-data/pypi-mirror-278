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
    'GetSecretRotationResult',
    'AwaitableGetSecretRotationResult',
    'get_secret_rotation',
    'get_secret_rotation_output',
]

@pulumi.output_type
class GetSecretRotationResult:
    """
    A collection of values returned by getSecretRotation.
    """
    def __init__(__self__, id=None, rotation_enabled=None, rotation_lambda_arn=None, rotation_rules=None, secret_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if rotation_enabled and not isinstance(rotation_enabled, bool):
            raise TypeError("Expected argument 'rotation_enabled' to be a bool")
        pulumi.set(__self__, "rotation_enabled", rotation_enabled)
        if rotation_lambda_arn and not isinstance(rotation_lambda_arn, str):
            raise TypeError("Expected argument 'rotation_lambda_arn' to be a str")
        pulumi.set(__self__, "rotation_lambda_arn", rotation_lambda_arn)
        if rotation_rules and not isinstance(rotation_rules, list):
            raise TypeError("Expected argument 'rotation_rules' to be a list")
        pulumi.set(__self__, "rotation_rules", rotation_rules)
        if secret_id and not isinstance(secret_id, str):
            raise TypeError("Expected argument 'secret_id' to be a str")
        pulumi.set(__self__, "secret_id", secret_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="rotationEnabled")
    def rotation_enabled(self) -> bool:
        """
        ARN of the secret.
        """
        return pulumi.get(self, "rotation_enabled")

    @property
    @pulumi.getter(name="rotationLambdaArn")
    def rotation_lambda_arn(self) -> str:
        """
        Decrypted part of the protected secret information that was originally provided as a string.
        """
        return pulumi.get(self, "rotation_lambda_arn")

    @property
    @pulumi.getter(name="rotationRules")
    def rotation_rules(self) -> Sequence['outputs.GetSecretRotationRotationRuleResult']:
        """
        Decrypted part of the protected secret information that was originally provided as a binary. Base64 encoded.
        """
        return pulumi.get(self, "rotation_rules")

    @property
    @pulumi.getter(name="secretId")
    def secret_id(self) -> str:
        return pulumi.get(self, "secret_id")


class AwaitableGetSecretRotationResult(GetSecretRotationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecretRotationResult(
            id=self.id,
            rotation_enabled=self.rotation_enabled,
            rotation_lambda_arn=self.rotation_lambda_arn,
            rotation_rules=self.rotation_rules,
            secret_id=self.secret_id)


def get_secret_rotation(secret_id: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecretRotationResult:
    """
    Retrieve information about a Secrets Manager secret rotation. To retrieve secret metadata, see the `secretsmanager.Secret` data source. To retrieve a secret value, see the `secretsmanager.SecretVersion` data source.

    ## Example Usage

    ### Retrieve Secret Rotation Configuration

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.secretsmanager.get_secret_rotation(secret_id=example_aws_secretsmanager_secret["id"])
    ```


    :param str secret_id: Specifies the secret containing the version that you want to retrieve. You can specify either the ARN or the friendly name of the secret.
    """
    __args__ = dict()
    __args__['secretId'] = secret_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:secretsmanager/getSecretRotation:getSecretRotation', __args__, opts=opts, typ=GetSecretRotationResult).value

    return AwaitableGetSecretRotationResult(
        id=pulumi.get(__ret__, 'id'),
        rotation_enabled=pulumi.get(__ret__, 'rotation_enabled'),
        rotation_lambda_arn=pulumi.get(__ret__, 'rotation_lambda_arn'),
        rotation_rules=pulumi.get(__ret__, 'rotation_rules'),
        secret_id=pulumi.get(__ret__, 'secret_id'))


@_utilities.lift_output_func(get_secret_rotation)
def get_secret_rotation_output(secret_id: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecretRotationResult]:
    """
    Retrieve information about a Secrets Manager secret rotation. To retrieve secret metadata, see the `secretsmanager.Secret` data source. To retrieve a secret value, see the `secretsmanager.SecretVersion` data source.

    ## Example Usage

    ### Retrieve Secret Rotation Configuration

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.secretsmanager.get_secret_rotation(secret_id=example_aws_secretsmanager_secret["id"])
    ```


    :param str secret_id: Specifies the secret containing the version that you want to retrieve. You can specify either the ARN or the friendly name of the secret.
    """
    ...
