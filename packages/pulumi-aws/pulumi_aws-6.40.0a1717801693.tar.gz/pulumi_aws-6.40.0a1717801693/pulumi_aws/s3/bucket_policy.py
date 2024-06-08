# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BucketPolicyArgs', 'BucketPolicy']

@pulumi.input_type
class BucketPolicyArgs:
    def __init__(__self__, *,
                 bucket: pulumi.Input[str],
                 policy: pulumi.Input[str]):
        """
        The set of arguments for constructing a BucketPolicy resource.
        :param pulumi.Input[str] bucket: Name of the bucket to which to apply the policy.
        :param pulumi.Input[str] policy: Text of the policy. Although this is a bucket policy rather than an IAM policy, the `iam_get_policy_document` data source may be used, so long as it specifies a principal. For more information about building AWS IAM policy documents, see the AWS IAM Policy Document Guide. Note: Bucket policies are limited to 20 KB in size.
        """
        pulumi.set(__self__, "bucket", bucket)
        pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Input[str]:
        """
        Name of the bucket to which to apply the policy.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Input[str]:
        """
        Text of the policy. Although this is a bucket policy rather than an IAM policy, the `iam_get_policy_document` data source may be used, so long as it specifies a principal. For more information about building AWS IAM policy documents, see the AWS IAM Policy Document Guide. Note: Bucket policies are limited to 20 KB in size.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: pulumi.Input[str]):
        pulumi.set(self, "policy", value)


@pulumi.input_type
class _BucketPolicyState:
    def __init__(__self__, *,
                 bucket: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BucketPolicy resources.
        :param pulumi.Input[str] bucket: Name of the bucket to which to apply the policy.
        :param pulumi.Input[str] policy: Text of the policy. Although this is a bucket policy rather than an IAM policy, the `iam_get_policy_document` data source may be used, so long as it specifies a principal. For more information about building AWS IAM policy documents, see the AWS IAM Policy Document Guide. Note: Bucket policies are limited to 20 KB in size.
        """
        if bucket is not None:
            pulumi.set(__self__, "bucket", bucket)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)

    @property
    @pulumi.getter
    def bucket(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the bucket to which to apply the policy.
        """
        return pulumi.get(self, "bucket")

    @bucket.setter
    def bucket(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "bucket", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        Text of the policy. Although this is a bucket policy rather than an IAM policy, the `iam_get_policy_document` data source may be used, so long as it specifies a principal. For more information about building AWS IAM policy documents, see the AWS IAM Policy Document Guide. Note: Bucket policies are limited to 20 KB in size.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)


class BucketPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Attaches a policy to an S3 bucket resource.

        > Policies can be attached to both S3 general purpose buckets and S3 directory buckets.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="my-tf-test-bucket")
        allow_access_from_another_account = aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="AWS",
                identifiers=["123456789012"],
            )],
            actions=[
                "s3:GetObject",
                "s3:ListBucket",
            ],
            resources=[
                example.arn,
                example.arn.apply(lambda arn: f"{arn}/*"),
            ],
        )])
        allow_access_from_another_account_bucket_policy = aws.s3.BucketPolicy("allow_access_from_another_account",
            bucket=example.id,
            policy=allow_access_from_another_account.json)
        ```

        ## Import

        Using `pulumi import`, import S3 bucket policies using the bucket name. For example:

        ```sh
        $ pulumi import aws:s3/bucketPolicy:BucketPolicy allow_access_from_another_account my-tf-test-bucket
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the bucket to which to apply the policy.
        :param pulumi.Input[str] policy: Text of the policy. Although this is a bucket policy rather than an IAM policy, the `iam_get_policy_document` data source may be used, so long as it specifies a principal. For more information about building AWS IAM policy documents, see the AWS IAM Policy Document Guide. Note: Bucket policies are limited to 20 KB in size.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BucketPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Attaches a policy to an S3 bucket resource.

        > Policies can be attached to both S3 general purpose buckets and S3 directory buckets.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.s3.BucketV2("example", bucket="my-tf-test-bucket")
        allow_access_from_another_account = aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="AWS",
                identifiers=["123456789012"],
            )],
            actions=[
                "s3:GetObject",
                "s3:ListBucket",
            ],
            resources=[
                example.arn,
                example.arn.apply(lambda arn: f"{arn}/*"),
            ],
        )])
        allow_access_from_another_account_bucket_policy = aws.s3.BucketPolicy("allow_access_from_another_account",
            bucket=example.id,
            policy=allow_access_from_another_account.json)
        ```

        ## Import

        Using `pulumi import`, import S3 bucket policies using the bucket name. For example:

        ```sh
        $ pulumi import aws:s3/bucketPolicy:BucketPolicy allow_access_from_another_account my-tf-test-bucket
        ```

        :param str resource_name: The name of the resource.
        :param BucketPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BucketPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BucketPolicyArgs.__new__(BucketPolicyArgs)

            if bucket is None and not opts.urn:
                raise TypeError("Missing required property 'bucket'")
            __props__.__dict__["bucket"] = bucket
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__.__dict__["policy"] = policy
        super(BucketPolicy, __self__).__init__(
            'aws:s3/bucketPolicy:BucketPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None) -> 'BucketPolicy':
        """
        Get an existing BucketPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: Name of the bucket to which to apply the policy.
        :param pulumi.Input[str] policy: Text of the policy. Although this is a bucket policy rather than an IAM policy, the `iam_get_policy_document` data source may be used, so long as it specifies a principal. For more information about building AWS IAM policy documents, see the AWS IAM Policy Document Guide. Note: Bucket policies are limited to 20 KB in size.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BucketPolicyState.__new__(_BucketPolicyState)

        __props__.__dict__["bucket"] = bucket
        __props__.__dict__["policy"] = policy
        return BucketPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        Name of the bucket to which to apply the policy.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        Text of the policy. Although this is a bucket policy rather than an IAM policy, the `iam_get_policy_document` data source may be used, so long as it specifies a principal. For more information about building AWS IAM policy documents, see the AWS IAM Policy Document Guide. Note: Bucket policies are limited to 20 KB in size.
        """
        return pulumi.get(self, "policy")

