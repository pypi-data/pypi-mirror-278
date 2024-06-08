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
    'SearchResult',
    'AwaitableSearchResult',
    'search',
    'search_output',
]

@pulumi.output_type
class SearchResult:
    """
    A collection of values returned by Search.
    """
    def __init__(__self__, id=None, query_string=None, resource_counts=None, resources=None, view_arn=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if query_string and not isinstance(query_string, str):
            raise TypeError("Expected argument 'query_string' to be a str")
        pulumi.set(__self__, "query_string", query_string)
        if resource_counts and not isinstance(resource_counts, list):
            raise TypeError("Expected argument 'resource_counts' to be a list")
        pulumi.set(__self__, "resource_counts", resource_counts)
        if resources and not isinstance(resources, list):
            raise TypeError("Expected argument 'resources' to be a list")
        pulumi.set(__self__, "resources", resources)
        if view_arn and not isinstance(view_arn, str):
            raise TypeError("Expected argument 'view_arn' to be a str")
        pulumi.set(__self__, "view_arn", view_arn)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Query String.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="queryString")
    def query_string(self) -> str:
        return pulumi.get(self, "query_string")

    @property
    @pulumi.getter(name="resourceCounts")
    def resource_counts(self) -> Sequence['outputs.SearchResourceCountResult']:
        """
        Number of resources that match the query. See `resource_count` below.
        """
        return pulumi.get(self, "resource_counts")

    @property
    @pulumi.getter
    def resources(self) -> Sequence['outputs.SearchResourceResult']:
        """
        List of structures that describe the resources that match the query. See `resources` below.
        """
        return pulumi.get(self, "resources")

    @property
    @pulumi.getter(name="viewArn")
    def view_arn(self) -> str:
        return pulumi.get(self, "view_arn")


class AwaitableSearchResult(SearchResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return SearchResult(
            id=self.id,
            query_string=self.query_string,
            resource_counts=self.resource_counts,
            resources=self.resources,
            view_arn=self.view_arn)


def search(query_string: Optional[str] = None,
           view_arn: Optional[str] = None,
           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableSearchResult:
    """
    Data source for managing an AWS Resource Explorer Search.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.resourceexplorer.search(query_string="region:us-west-2",
        view_arn=test["arn"])
    ```


    :param str query_string: String that includes keywords and filters that specify the resources that you want to include in the results. For the complete syntax supported by the QueryString parameter, see Search query syntax reference for [Resource Explorer](https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html). The search is completely case insensitive. You can specify an empty string to return all results up to the limit of 1,000 total results. The operation can return only the first 1,000 results. If the resource you want is not included, then use a different value for QueryString to refine the results.
           
           The following arguments are optional:
    :param str view_arn: Specifies the Amazon resource name (ARN) of the view to use for the query. If you don't specify a value for this parameter, then the operation automatically uses the default view for the AWS Region in which you called this operation. If the Region either doesn't have a default view or if you don't have permission to use the default view, then the operation fails with a `401 Unauthorized` exception.
    """
    __args__ = dict()
    __args__['queryString'] = query_string
    __args__['viewArn'] = view_arn
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:resourceexplorer/search:Search', __args__, opts=opts, typ=SearchResult).value

    return AwaitableSearchResult(
        id=pulumi.get(__ret__, 'id'),
        query_string=pulumi.get(__ret__, 'query_string'),
        resource_counts=pulumi.get(__ret__, 'resource_counts'),
        resources=pulumi.get(__ret__, 'resources'),
        view_arn=pulumi.get(__ret__, 'view_arn'))


@_utilities.lift_output_func(search)
def search_output(query_string: Optional[pulumi.Input[str]] = None,
                  view_arn: Optional[pulumi.Input[Optional[str]]] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[SearchResult]:
    """
    Data source for managing an AWS Resource Explorer Search.

    ## Example Usage

    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.resourceexplorer.search(query_string="region:us-west-2",
        view_arn=test["arn"])
    ```


    :param str query_string: String that includes keywords and filters that specify the resources that you want to include in the results. For the complete syntax supported by the QueryString parameter, see Search query syntax reference for [Resource Explorer](https://docs.aws.amazon.com/resource-explorer/latest/userguide/using-search-query-syntax.html). The search is completely case insensitive. You can specify an empty string to return all results up to the limit of 1,000 total results. The operation can return only the first 1,000 results. If the resource you want is not included, then use a different value for QueryString to refine the results.
           
           The following arguments are optional:
    :param str view_arn: Specifies the Amazon resource name (ARN) of the view to use for the query. If you don't specify a value for this parameter, then the operation automatically uses the default view for the AWS Region in which you called this operation. If the Region either doesn't have a default view or if you don't have permission to use the default view, then the operation fails with a `401 Unauthorized` exception.
    """
    ...
