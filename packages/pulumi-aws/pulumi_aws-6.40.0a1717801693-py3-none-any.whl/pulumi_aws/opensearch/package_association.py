# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PackageAssociationArgs', 'PackageAssociation']

@pulumi.input_type
class PackageAssociationArgs:
    def __init__(__self__, *,
                 domain_name: pulumi.Input[str],
                 package_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a PackageAssociation resource.
        :param pulumi.Input[str] domain_name: Name of the domain to associate the package with.
        :param pulumi.Input[str] package_id: Internal ID of the package to associate with a domain.
        """
        pulumi.set(__self__, "domain_name", domain_name)
        pulumi.set(__self__, "package_id", package_id)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Input[str]:
        """
        Name of the domain to associate the package with.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> pulumi.Input[str]:
        """
        Internal ID of the package to associate with a domain.
        """
        return pulumi.get(self, "package_id")

    @package_id.setter
    def package_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "package_id", value)


@pulumi.input_type
class _PackageAssociationState:
    def __init__(__self__, *,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 package_id: Optional[pulumi.Input[str]] = None,
                 reference_path: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering PackageAssociation resources.
        :param pulumi.Input[str] domain_name: Name of the domain to associate the package with.
        :param pulumi.Input[str] package_id: Internal ID of the package to associate with a domain.
        """
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if package_id is not None:
            pulumi.set(__self__, "package_id", package_id)
        if reference_path is not None:
            pulumi.set(__self__, "reference_path", reference_path)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the domain to associate the package with.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> Optional[pulumi.Input[str]]:
        """
        Internal ID of the package to associate with a domain.
        """
        return pulumi.get(self, "package_id")

    @package_id.setter
    def package_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "package_id", value)

    @property
    @pulumi.getter(name="referencePath")
    def reference_path(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "reference_path")

    @reference_path.setter
    def reference_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "reference_path", value)


class PackageAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 package_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages an AWS Opensearch Package Association.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        my_domain = aws.opensearch.Domain("my_domain",
            domain_name="my-opensearch-domain",
            engine_version="Elasticsearch_7.10",
            cluster_config=aws.opensearch.DomainClusterConfigArgs(
                instance_type="r4.large.search",
            ))
        example = aws.opensearch.Package("example",
            package_name="example-txt",
            package_source=aws.opensearch.PackagePackageSourceArgs(
                s3_bucket_name=my_opensearch_packages["bucket"],
                s3_key=example_aws_s3_object["key"],
            ),
            package_type="TXT-DICTIONARY")
        example_package_association = aws.opensearch.PackageAssociation("example",
            package_id=example.id,
            domain_name=my_domain.domain_name)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_name: Name of the domain to associate the package with.
        :param pulumi.Input[str] package_id: Internal ID of the package to associate with a domain.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PackageAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AWS Opensearch Package Association.

        ## Example Usage

        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        my_domain = aws.opensearch.Domain("my_domain",
            domain_name="my-opensearch-domain",
            engine_version="Elasticsearch_7.10",
            cluster_config=aws.opensearch.DomainClusterConfigArgs(
                instance_type="r4.large.search",
            ))
        example = aws.opensearch.Package("example",
            package_name="example-txt",
            package_source=aws.opensearch.PackagePackageSourceArgs(
                s3_bucket_name=my_opensearch_packages["bucket"],
                s3_key=example_aws_s3_object["key"],
            ),
            package_type="TXT-DICTIONARY")
        example_package_association = aws.opensearch.PackageAssociation("example",
            package_id=example.id,
            domain_name=my_domain.domain_name)
        ```

        :param str resource_name: The name of the resource.
        :param PackageAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PackageAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 package_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PackageAssociationArgs.__new__(PackageAssociationArgs)

            if domain_name is None and not opts.urn:
                raise TypeError("Missing required property 'domain_name'")
            __props__.__dict__["domain_name"] = domain_name
            if package_id is None and not opts.urn:
                raise TypeError("Missing required property 'package_id'")
            __props__.__dict__["package_id"] = package_id
            __props__.__dict__["reference_path"] = None
        super(PackageAssociation, __self__).__init__(
            'aws:opensearch/packageAssociation:PackageAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            domain_name: Optional[pulumi.Input[str]] = None,
            package_id: Optional[pulumi.Input[str]] = None,
            reference_path: Optional[pulumi.Input[str]] = None) -> 'PackageAssociation':
        """
        Get an existing PackageAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] domain_name: Name of the domain to associate the package with.
        :param pulumi.Input[str] package_id: Internal ID of the package to associate with a domain.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PackageAssociationState.__new__(_PackageAssociationState)

        __props__.__dict__["domain_name"] = domain_name
        __props__.__dict__["package_id"] = package_id
        __props__.__dict__["reference_path"] = reference_path
        return PackageAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> pulumi.Output[str]:
        """
        Name of the domain to associate the package with.
        """
        return pulumi.get(self, "domain_name")

    @property
    @pulumi.getter(name="packageId")
    def package_id(self) -> pulumi.Output[str]:
        """
        Internal ID of the package to associate with a domain.
        """
        return pulumi.get(self, "package_id")

    @property
    @pulumi.getter(name="referencePath")
    def reference_path(self) -> pulumi.Output[str]:
        return pulumi.get(self, "reference_path")

