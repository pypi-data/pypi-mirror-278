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
    'RepositoryAssociationKmsKeyDetails',
    'RepositoryAssociationRepository',
    'RepositoryAssociationRepositoryBitbucket',
    'RepositoryAssociationRepositoryCodecommit',
    'RepositoryAssociationRepositoryGithubEnterpriseServer',
    'RepositoryAssociationRepositoryS3Bucket',
    'RepositoryAssociationS3RepositoryDetail',
    'RepositoryAssociationS3RepositoryDetailCodeArtifact',
]

@pulumi.output_type
class RepositoryAssociationKmsKeyDetails(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "encryptionOption":
            suggest = "encryption_option"
        elif key == "kmsKeyId":
            suggest = "kms_key_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryAssociationKmsKeyDetails. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryAssociationKmsKeyDetails.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryAssociationKmsKeyDetails.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 encryption_option: Optional[str] = None,
                 kms_key_id: Optional[str] = None):
        """
        :param str encryption_option: The encryption option for a repository association. It is either owned by AWS Key Management Service (KMS) (`AWS_OWNED_CMK`) or customer managed (`CUSTOMER_MANAGED_CMK`).
        :param str kms_key_id: The ID of the AWS KMS key that is associated with a repository association.
        """
        if encryption_option is not None:
            pulumi.set(__self__, "encryption_option", encryption_option)
        if kms_key_id is not None:
            pulumi.set(__self__, "kms_key_id", kms_key_id)

    @property
    @pulumi.getter(name="encryptionOption")
    def encryption_option(self) -> Optional[str]:
        """
        The encryption option for a repository association. It is either owned by AWS Key Management Service (KMS) (`AWS_OWNED_CMK`) or customer managed (`CUSTOMER_MANAGED_CMK`).
        """
        return pulumi.get(self, "encryption_option")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[str]:
        """
        The ID of the AWS KMS key that is associated with a repository association.
        """
        return pulumi.get(self, "kms_key_id")


@pulumi.output_type
class RepositoryAssociationRepository(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "githubEnterpriseServer":
            suggest = "github_enterprise_server"
        elif key == "s3Bucket":
            suggest = "s3_bucket"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryAssociationRepository. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryAssociationRepository.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryAssociationRepository.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bitbucket: Optional['outputs.RepositoryAssociationRepositoryBitbucket'] = None,
                 codecommit: Optional['outputs.RepositoryAssociationRepositoryCodecommit'] = None,
                 github_enterprise_server: Optional['outputs.RepositoryAssociationRepositoryGithubEnterpriseServer'] = None,
                 s3_bucket: Optional['outputs.RepositoryAssociationRepositoryS3Bucket'] = None):
        if bitbucket is not None:
            pulumi.set(__self__, "bitbucket", bitbucket)
        if codecommit is not None:
            pulumi.set(__self__, "codecommit", codecommit)
        if github_enterprise_server is not None:
            pulumi.set(__self__, "github_enterprise_server", github_enterprise_server)
        if s3_bucket is not None:
            pulumi.set(__self__, "s3_bucket", s3_bucket)

    @property
    @pulumi.getter
    def bitbucket(self) -> Optional['outputs.RepositoryAssociationRepositoryBitbucket']:
        return pulumi.get(self, "bitbucket")

    @property
    @pulumi.getter
    def codecommit(self) -> Optional['outputs.RepositoryAssociationRepositoryCodecommit']:
        return pulumi.get(self, "codecommit")

    @property
    @pulumi.getter(name="githubEnterpriseServer")
    def github_enterprise_server(self) -> Optional['outputs.RepositoryAssociationRepositoryGithubEnterpriseServer']:
        return pulumi.get(self, "github_enterprise_server")

    @property
    @pulumi.getter(name="s3Bucket")
    def s3_bucket(self) -> Optional['outputs.RepositoryAssociationRepositoryS3Bucket']:
        return pulumi.get(self, "s3_bucket")


@pulumi.output_type
class RepositoryAssociationRepositoryBitbucket(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "connectionArn":
            suggest = "connection_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryAssociationRepositoryBitbucket. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryAssociationRepositoryBitbucket.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryAssociationRepositoryBitbucket.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 connection_arn: str,
                 name: str,
                 owner: str):
        """
        :param str connection_arn: The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection.
        :param str name: The name of the third party source repository.
        :param str owner: The username for the account that owns the repository.
        """
        pulumi.set(__self__, "connection_arn", connection_arn)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "owner", owner)

    @property
    @pulumi.getter(name="connectionArn")
    def connection_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection.
        """
        return pulumi.get(self, "connection_arn")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the third party source repository.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> str:
        """
        The username for the account that owns the repository.
        """
        return pulumi.get(self, "owner")


@pulumi.output_type
class RepositoryAssociationRepositoryCodecommit(dict):
    def __init__(__self__, *,
                 name: str):
        """
        :param str name: The name of the AWS CodeCommit repository.
        """
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the AWS CodeCommit repository.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class RepositoryAssociationRepositoryGithubEnterpriseServer(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "connectionArn":
            suggest = "connection_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryAssociationRepositoryGithubEnterpriseServer. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryAssociationRepositoryGithubEnterpriseServer.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryAssociationRepositoryGithubEnterpriseServer.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 connection_arn: str,
                 name: str,
                 owner: str):
        """
        :param str connection_arn: The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection.
        :param str name: The name of the third party source repository.
        :param str owner: The username for the account that owns the repository.
        """
        pulumi.set(__self__, "connection_arn", connection_arn)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "owner", owner)

    @property
    @pulumi.getter(name="connectionArn")
    def connection_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of an AWS CodeStar Connections connection.
        """
        return pulumi.get(self, "connection_arn")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the third party source repository.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> str:
        """
        The username for the account that owns the repository.
        """
        return pulumi.get(self, "owner")


@pulumi.output_type
class RepositoryAssociationRepositoryS3Bucket(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryAssociationRepositoryS3Bucket. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryAssociationRepositoryS3Bucket.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryAssociationRepositoryS3Bucket.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: str,
                 name: str):
        """
        :param str bucket_name: The name of the S3 bucket used for associating a new S3 repository. Note: The name must begin with `codeguru-reviewer-`.
        :param str name: The name of the repository in the S3 bucket.
        """
        pulumi.set(__self__, "bucket_name", bucket_name)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> str:
        """
        The name of the S3 bucket used for associating a new S3 repository. Note: The name must begin with `codeguru-reviewer-`.
        """
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the repository in the S3 bucket.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class RepositoryAssociationS3RepositoryDetail(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bucketName":
            suggest = "bucket_name"
        elif key == "codeArtifacts":
            suggest = "code_artifacts"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryAssociationS3RepositoryDetail. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryAssociationS3RepositoryDetail.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryAssociationS3RepositoryDetail.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 bucket_name: Optional[str] = None,
                 code_artifacts: Optional[Sequence['outputs.RepositoryAssociationS3RepositoryDetailCodeArtifact']] = None):
        if bucket_name is not None:
            pulumi.set(__self__, "bucket_name", bucket_name)
        if code_artifacts is not None:
            pulumi.set(__self__, "code_artifacts", code_artifacts)

    @property
    @pulumi.getter(name="bucketName")
    def bucket_name(self) -> Optional[str]:
        return pulumi.get(self, "bucket_name")

    @property
    @pulumi.getter(name="codeArtifacts")
    def code_artifacts(self) -> Optional[Sequence['outputs.RepositoryAssociationS3RepositoryDetailCodeArtifact']]:
        return pulumi.get(self, "code_artifacts")


@pulumi.output_type
class RepositoryAssociationS3RepositoryDetailCodeArtifact(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "buildArtifactsObjectKey":
            suggest = "build_artifacts_object_key"
        elif key == "sourceCodeArtifactsObjectKey":
            suggest = "source_code_artifacts_object_key"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in RepositoryAssociationS3RepositoryDetailCodeArtifact. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        RepositoryAssociationS3RepositoryDetailCodeArtifact.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        RepositoryAssociationS3RepositoryDetailCodeArtifact.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 build_artifacts_object_key: Optional[str] = None,
                 source_code_artifacts_object_key: Optional[str] = None):
        if build_artifacts_object_key is not None:
            pulumi.set(__self__, "build_artifacts_object_key", build_artifacts_object_key)
        if source_code_artifacts_object_key is not None:
            pulumi.set(__self__, "source_code_artifacts_object_key", source_code_artifacts_object_key)

    @property
    @pulumi.getter(name="buildArtifactsObjectKey")
    def build_artifacts_object_key(self) -> Optional[str]:
        return pulumi.get(self, "build_artifacts_object_key")

    @property
    @pulumi.getter(name="sourceCodeArtifactsObjectKey")
    def source_code_artifacts_object_key(self) -> Optional[str]:
        return pulumi.get(self, "source_code_artifacts_object_key")


