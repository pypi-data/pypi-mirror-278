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
    'GetBucketResult',
    'AwaitableGetBucketResult',
    'get_bucket',
    'get_bucket_output',
]

@pulumi.output_type
class GetBucketResult:
    """
    A collection of values returned by getBucket.
    """
    def __init__(__self__, arn=None, bucket=None, bucket_domain_name=None, bucket_regional_domain_name=None, hosted_zone_id=None, id=None, region=None, website_domain=None, website_endpoint=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if bucket and not isinstance(bucket, str):
            raise TypeError("Expected argument 'bucket' to be a str")
        pulumi.set(__self__, "bucket", bucket)
        if bucket_domain_name and not isinstance(bucket_domain_name, str):
            raise TypeError("Expected argument 'bucket_domain_name' to be a str")
        pulumi.set(__self__, "bucket_domain_name", bucket_domain_name)
        if bucket_regional_domain_name and not isinstance(bucket_regional_domain_name, str):
            raise TypeError("Expected argument 'bucket_regional_domain_name' to be a str")
        pulumi.set(__self__, "bucket_regional_domain_name", bucket_regional_domain_name)
        if hosted_zone_id and not isinstance(hosted_zone_id, str):
            raise TypeError("Expected argument 'hosted_zone_id' to be a str")
        pulumi.set(__self__, "hosted_zone_id", hosted_zone_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if website_domain and not isinstance(website_domain, str):
            raise TypeError("Expected argument 'website_domain' to be a str")
        pulumi.set(__self__, "website_domain", website_domain)
        if website_endpoint and not isinstance(website_endpoint, str):
            raise TypeError("Expected argument 'website_endpoint' to be a str")
        pulumi.set(__self__, "website_endpoint", website_endpoint)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the bucket. Will be of format `arn:aws:s3:::bucketname`.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def bucket(self) -> str:
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="bucketDomainName")
    def bucket_domain_name(self) -> str:
        """
        Bucket domain name. Will be of format `bucketname.s3.amazonaws.com`.
        """
        return pulumi.get(self, "bucket_domain_name")

    @property
    @pulumi.getter(name="bucketRegionalDomainName")
    def bucket_regional_domain_name(self) -> str:
        """
        The bucket region-specific domain name. The bucket domain name including the region name. Please refer to the [S3 endpoints reference](https://docs.aws.amazon.com/general/latest/gr/s3.html#s3_region) for format. Note: AWS CloudFront allows specifying an S3 region-specific endpoint when creating an S3 origin. This will prevent redirect issues from CloudFront to the S3 Origin URL. For more information, see the [Virtual Hosted-Style Requests for Other Regions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/VirtualHosting.html#deprecated-global-endpoint) section in the AWS S3 User Guide.
        """
        return pulumi.get(self, "bucket_regional_domain_name")

    @property
    @pulumi.getter(name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """
        The [Route 53 Hosted Zone ID](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_website_region_endpoints) for this bucket's region.
        """
        return pulumi.get(self, "hosted_zone_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def region(self) -> str:
        """
        AWS region this bucket resides in.
        """
        return pulumi.get(self, "region")

    @property
    @pulumi.getter(name="websiteDomain")
    def website_domain(self) -> str:
        """
        Domain of the website endpoint, if the bucket is configured with a website. If not, this will be an empty string. This is used to create Route 53 alias records.
        """
        return pulumi.get(self, "website_domain")

    @property
    @pulumi.getter(name="websiteEndpoint")
    def website_endpoint(self) -> str:
        """
        Website endpoint, if the bucket is configured with a website. If not, this will be an empty string.
        """
        return pulumi.get(self, "website_endpoint")


class AwaitableGetBucketResult(GetBucketResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBucketResult(
            arn=self.arn,
            bucket=self.bucket,
            bucket_domain_name=self.bucket_domain_name,
            bucket_regional_domain_name=self.bucket_regional_domain_name,
            hosted_zone_id=self.hosted_zone_id,
            id=self.id,
            region=self.region,
            website_domain=self.website_domain,
            website_endpoint=self.website_endpoint)


def get_bucket(bucket: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBucketResult:
    """
    Provides details about a specific S3 bucket.

    This resource may prove useful when setting up a Route53 record, or an origin for a CloudFront
    Distribution.

    ## Example Usage

    ### Route53 Record

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.s3.get_bucket(bucket="bucket.test.com")
    test_zone = aws.route53.get_zone(name="test.com.")
    example = aws.route53.Record("example",
        zone_id=test_zone.id,
        name="bucket",
        type=aws.route53.RecordType.A,
        aliases=[aws.route53.RecordAliasArgs(
            name=selected.website_domain,
            zone_id=selected.hosted_zone_id,
        )])
    ```

    ### CloudFront Origin

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.s3.get_bucket(bucket="a-test-bucket")
    test = aws.cloudfront.Distribution("test", origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=selected.bucket_domain_name,
        origin_id="s3-selected-bucket",
    )])
    ```


    :param str bucket: Name of the bucket
    """
    __args__ = dict()
    __args__['bucket'] = bucket
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:s3/getBucket:getBucket', __args__, opts=opts, typ=GetBucketResult).value

    return AwaitableGetBucketResult(
        arn=pulumi.get(__ret__, 'arn'),
        bucket=pulumi.get(__ret__, 'bucket'),
        bucket_domain_name=pulumi.get(__ret__, 'bucket_domain_name'),
        bucket_regional_domain_name=pulumi.get(__ret__, 'bucket_regional_domain_name'),
        hosted_zone_id=pulumi.get(__ret__, 'hosted_zone_id'),
        id=pulumi.get(__ret__, 'id'),
        region=pulumi.get(__ret__, 'region'),
        website_domain=pulumi.get(__ret__, 'website_domain'),
        website_endpoint=pulumi.get(__ret__, 'website_endpoint'))


@_utilities.lift_output_func(get_bucket)
def get_bucket_output(bucket: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBucketResult]:
    """
    Provides details about a specific S3 bucket.

    This resource may prove useful when setting up a Route53 record, or an origin for a CloudFront
    Distribution.

    ## Example Usage

    ### Route53 Record

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.s3.get_bucket(bucket="bucket.test.com")
    test_zone = aws.route53.get_zone(name="test.com.")
    example = aws.route53.Record("example",
        zone_id=test_zone.id,
        name="bucket",
        type=aws.route53.RecordType.A,
        aliases=[aws.route53.RecordAliasArgs(
            name=selected.website_domain,
            zone_id=selected.hosted_zone_id,
        )])
    ```

    ### CloudFront Origin

    ```python
    import pulumi
    import pulumi_aws as aws

    selected = aws.s3.get_bucket(bucket="a-test-bucket")
    test = aws.cloudfront.Distribution("test", origins=[aws.cloudfront.DistributionOriginArgs(
        domain_name=selected.bucket_domain_name,
        origin_id="s3-selected-bucket",
    )])
    ```


    :param str bucket: Name of the bucket
    """
    ...
