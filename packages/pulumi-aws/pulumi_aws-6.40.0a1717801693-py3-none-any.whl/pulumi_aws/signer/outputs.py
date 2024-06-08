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
    'SigningJobDestination',
    'SigningJobDestinationS3',
    'SigningJobRevocationRecord',
    'SigningJobSignedObject',
    'SigningJobSignedObjectS3',
    'SigningJobSource',
    'SigningJobSourceS3',
    'SigningProfileRevocationRecord',
    'SigningProfileSignatureValidityPeriod',
    'SigningProfileSigningMaterial',
    'GetSigningJobRevocationRecordResult',
    'GetSigningJobSignedObjectResult',
    'GetSigningJobSignedObjectS3Result',
    'GetSigningJobSourceResult',
    'GetSigningJobSourceS3Result',
    'GetSigningProfileRevocationRecordResult',
    'GetSigningProfileSignatureValidityPeriodResult',
]

@pulumi.output_type
class SigningJobDestination(dict):
    def __init__(__self__, *,
                 s3: 'outputs.SigningJobDestinationS3'):
        """
        :param 'SigningJobDestinationS3Args' s3: A configuration block describing the S3 Destination object: See S3 Destination below for details.
        """
        pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter
    def s3(self) -> 'outputs.SigningJobDestinationS3':
        """
        A configuration block describing the S3 Destination object: See S3 Destination below for details.
        """
        return pulumi.get(self, "s3")


@pulumi.output_type
class SigningJobDestinationS3(dict):
    def __init__(__self__, *,
                 bucket: str,
                 prefix: Optional[str] = None):
        pulumi.set(__self__, "bucket", bucket)
        if prefix is not None:
            pulumi.set(__self__, "prefix", prefix)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def prefix(self) -> Optional[str]:
        return pulumi.get(self, "prefix")


@pulumi.output_type
class SigningJobRevocationRecord(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "revokedAt":
            suggest = "revoked_at"
        elif key == "revokedBy":
            suggest = "revoked_by"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SigningJobRevocationRecord. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SigningJobRevocationRecord.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SigningJobRevocationRecord.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 reason: Optional[str] = None,
                 revoked_at: Optional[str] = None,
                 revoked_by: Optional[str] = None):
        if reason is not None:
            pulumi.set(__self__, "reason", reason)
        if revoked_at is not None:
            pulumi.set(__self__, "revoked_at", revoked_at)
        if revoked_by is not None:
            pulumi.set(__self__, "revoked_by", revoked_by)

    @property
    @pulumi.getter
    def reason(self) -> Optional[str]:
        return pulumi.get(self, "reason")

    @property
    @pulumi.getter(name="revokedAt")
    def revoked_at(self) -> Optional[str]:
        return pulumi.get(self, "revoked_at")

    @property
    @pulumi.getter(name="revokedBy")
    def revoked_by(self) -> Optional[str]:
        return pulumi.get(self, "revoked_by")


@pulumi.output_type
class SigningJobSignedObject(dict):
    def __init__(__self__, *,
                 s3s: Optional[Sequence['outputs.SigningJobSignedObjectS3']] = None):
        if s3s is not None:
            pulumi.set(__self__, "s3s", s3s)

    @property
    @pulumi.getter
    def s3s(self) -> Optional[Sequence['outputs.SigningJobSignedObjectS3']]:
        return pulumi.get(self, "s3s")


@pulumi.output_type
class SigningJobSignedObjectS3(dict):
    def __init__(__self__, *,
                 bucket: Optional[str] = None,
                 key: Optional[str] = None):
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if key is not None:
            pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[str]:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def key(self) -> Optional[str]:
        return pulumi.get(self, "key")


@pulumi.output_type
class SigningJobSource(dict):
    def __init__(__self__, *,
                 s3: 'outputs.SigningJobSourceS3'):
        """
        :param 'SigningJobSourceS3Args' s3: A configuration block describing the S3 Source object: See S3 Source below for details.
        """
        pulumi.set(__self__, "s3", s3)

    @property
    @pulumi.getter
    def s3(self) -> 'outputs.SigningJobSourceS3':
        """
        A configuration block describing the S3 Source object: See S3 Source below for details.
        """
        return pulumi.get(self, "s3")


@pulumi.output_type
class SigningJobSourceS3(dict):
    def __init__(__self__, *,
                 bucket: str,
                 key: str,
                 version: str):
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def version(self) -> str:
        return pulumi.get(self, "version")


@pulumi.output_type
class SigningProfileRevocationRecord(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "revocationEffectiveFrom":
            suggest = "revocation_effective_from"
        elif key == "revokedAt":
            suggest = "revoked_at"
        elif key == "revokedBy":
            suggest = "revoked_by"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SigningProfileRevocationRecord. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SigningProfileRevocationRecord.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SigningProfileRevocationRecord.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 revocation_effective_from: Optional[str] = None,
                 revoked_at: Optional[str] = None,
                 revoked_by: Optional[str] = None):
        """
        :param str revocation_effective_from: The time when revocation becomes effective.
        :param str revoked_at: The time when the signing profile was revoked.
        :param str revoked_by: The identity of the revoker.
        """
        if revocation_effective_from is not None:
            pulumi.set(__self__, "revocation_effective_from", revocation_effective_from)
        if revoked_at is not None:
            pulumi.set(__self__, "revoked_at", revoked_at)
        if revoked_by is not None:
            pulumi.set(__self__, "revoked_by", revoked_by)

    @property
    @pulumi.getter(name="revocationEffectiveFrom")
    def revocation_effective_from(self) -> Optional[str]:
        """
        The time when revocation becomes effective.
        """
        return pulumi.get(self, "revocation_effective_from")

    @property
    @pulumi.getter(name="revokedAt")
    def revoked_at(self) -> Optional[str]:
        """
        The time when the signing profile was revoked.
        """
        return pulumi.get(self, "revoked_at")

    @property
    @pulumi.getter(name="revokedBy")
    def revoked_by(self) -> Optional[str]:
        """
        The identity of the revoker.
        """
        return pulumi.get(self, "revoked_by")


@pulumi.output_type
class SigningProfileSignatureValidityPeriod(dict):
    def __init__(__self__, *,
                 type: str,
                 value: int):
        """
        :param str type: The time unit for signature validity. Valid values: `DAYS`, `MONTHS`, `YEARS`.
        :param int value: The numerical value of the time unit for signature validity.
        """
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The time unit for signature validity. Valid values: `DAYS`, `MONTHS`, `YEARS`.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> int:
        """
        The numerical value of the time unit for signature validity.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class SigningProfileSigningMaterial(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "certificateArn":
            suggest = "certificate_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SigningProfileSigningMaterial. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SigningProfileSigningMaterial.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SigningProfileSigningMaterial.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 certificate_arn: str):
        """
        :param str certificate_arn: The Amazon Resource Name (ARN) of the certificates that is used to sign your code.
        """
        pulumi.set(__self__, "certificate_arn", certificate_arn)

    @property
    @pulumi.getter(name="certificateArn")
    def certificate_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the certificates that is used to sign your code.
        """
        return pulumi.get(self, "certificate_arn")


@pulumi.output_type
class GetSigningJobRevocationRecordResult(dict):
    def __init__(__self__, *,
                 reason: str,
                 revoked_at: str,
                 revoked_by: str):
        pulumi.set(__self__, "reason", reason)
        pulumi.set(__self__, "revoked_at", revoked_at)
        pulumi.set(__self__, "revoked_by", revoked_by)

    @property
    @pulumi.getter
    def reason(self) -> str:
        return pulumi.get(self, "reason")

    @property
    @pulumi.getter(name="revokedAt")
    def revoked_at(self) -> str:
        return pulumi.get(self, "revoked_at")

    @property
    @pulumi.getter(name="revokedBy")
    def revoked_by(self) -> str:
        return pulumi.get(self, "revoked_by")


@pulumi.output_type
class GetSigningJobSignedObjectResult(dict):
    def __init__(__self__, *,
                 s3s: Sequence['outputs.GetSigningJobSignedObjectS3Result']):
        pulumi.set(__self__, "s3s", s3s)

    @property
    @pulumi.getter
    def s3s(self) -> Sequence['outputs.GetSigningJobSignedObjectS3Result']:
        return pulumi.get(self, "s3s")


@pulumi.output_type
class GetSigningJobSignedObjectS3Result(dict):
    def __init__(__self__, *,
                 bucket: str,
                 key: str):
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "key", key)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")


@pulumi.output_type
class GetSigningJobSourceResult(dict):
    def __init__(__self__, *,
                 s3s: Sequence['outputs.GetSigningJobSourceS3Result']):
        pulumi.set(__self__, "s3s", s3s)

    @property
    @pulumi.getter
    def s3s(self) -> Sequence['outputs.GetSigningJobSourceS3Result']:
        return pulumi.get(self, "s3s")


@pulumi.output_type
class GetSigningJobSourceS3Result(dict):
    def __init__(__self__, *,
                 bucket: str,
                 key: str,
                 version: str):
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def version(self) -> str:
        return pulumi.get(self, "version")


@pulumi.output_type
class GetSigningProfileRevocationRecordResult(dict):
    def __init__(__self__, *,
                 revocation_effective_from: str,
                 revoked_at: str,
                 revoked_by: str):
        pulumi.set(__self__, "revocation_effective_from", revocation_effective_from)
        pulumi.set(__self__, "revoked_at", revoked_at)
        pulumi.set(__self__, "revoked_by", revoked_by)

    @property
    @pulumi.getter(name="revocationEffectiveFrom")
    def revocation_effective_from(self) -> str:
        return pulumi.get(self, "revocation_effective_from")

    @property
    @pulumi.getter(name="revokedAt")
    def revoked_at(self) -> str:
        return pulumi.get(self, "revoked_at")

    @property
    @pulumi.getter(name="revokedBy")
    def revoked_by(self) -> str:
        return pulumi.get(self, "revoked_by")


@pulumi.output_type
class GetSigningProfileSignatureValidityPeriodResult(dict):
    def __init__(__self__, *,
                 type: str,
                 value: int):
        pulumi.set(__self__, "type", type)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def type(self) -> str:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def value(self) -> int:
        return pulumi.get(self, "value")


