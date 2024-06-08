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
    'AppMonitorAppMonitorConfiguration',
    'AppMonitorCustomEvents',
]

@pulumi.output_type
class AppMonitorAppMonitorConfiguration(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "allowCookies":
            suggest = "allow_cookies"
        elif key == "enableXray":
            suggest = "enable_xray"
        elif key == "excludedPages":
            suggest = "excluded_pages"
        elif key == "favoritePages":
            suggest = "favorite_pages"
        elif key == "guestRoleArn":
            suggest = "guest_role_arn"
        elif key == "identityPoolId":
            suggest = "identity_pool_id"
        elif key == "includedPages":
            suggest = "included_pages"
        elif key == "sessionSampleRate":
            suggest = "session_sample_rate"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AppMonitorAppMonitorConfiguration. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AppMonitorAppMonitorConfiguration.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AppMonitorAppMonitorConfiguration.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 allow_cookies: Optional[bool] = None,
                 enable_xray: Optional[bool] = None,
                 excluded_pages: Optional[Sequence[str]] = None,
                 favorite_pages: Optional[Sequence[str]] = None,
                 guest_role_arn: Optional[str] = None,
                 identity_pool_id: Optional[str] = None,
                 included_pages: Optional[Sequence[str]] = None,
                 session_sample_rate: Optional[float] = None,
                 telemetries: Optional[Sequence[str]] = None):
        """
        :param bool allow_cookies: If you set this to `true`, RUM web client sets two cookies, a session cookie  and a user cookie. The cookies allow the RUM web client to collect data relating to the number of users an application has and the behavior of the application across a sequence of events. Cookies are stored in the top-level domain of the current page.
        :param bool enable_xray: If you set this to `true`, RUM enables X-Ray tracing for the user sessions  that RUM samples. RUM adds an X-Ray trace header to allowed HTTP requests. It also records an X-Ray segment for allowed HTTP requests.
        :param Sequence[str] excluded_pages: A list of URLs in your website or application to exclude from RUM data collection.
        :param Sequence[str] favorite_pages: A list of pages in the CloudWatch RUM console that are to be displayed with a "favorite" icon.
        :param str guest_role_arn: The ARN of the guest IAM role that is attached to the Amazon Cognito identity pool that is used to authorize the sending of data to RUM.
        :param str identity_pool_id: The ID of the Amazon Cognito identity pool that is used to authorize the sending of data to RUM.
        :param Sequence[str] included_pages: If this app monitor is to collect data from only certain pages in your application, this structure lists those pages.
        :param float session_sample_rate: Specifies the percentage of user sessions to use for RUM data collection. Choosing a higher percentage gives you more data but also incurs more costs. The number you specify is the percentage of user sessions that will be used. Default value is `0.1`.
        :param Sequence[str] telemetries: An array that lists the types of telemetry data that this app monitor is to collect. Valid values are `errors`, `performance`, and `http`.
        """
        if allow_cookies is not None:
            pulumi.set(__self__, "allow_cookies", allow_cookies)
        if enable_xray is not None:
            pulumi.set(__self__, "enable_xray", enable_xray)
        if excluded_pages is not None:
            pulumi.set(__self__, "excluded_pages", excluded_pages)
        if favorite_pages is not None:
            pulumi.set(__self__, "favorite_pages", favorite_pages)
        if guest_role_arn is not None:
            pulumi.set(__self__, "guest_role_arn", guest_role_arn)
        if identity_pool_id is not None:
            pulumi.set(__self__, "identity_pool_id", identity_pool_id)
        if included_pages is not None:
            pulumi.set(__self__, "included_pages", included_pages)
        if session_sample_rate is not None:
            pulumi.set(__self__, "session_sample_rate", session_sample_rate)
        if telemetries is not None:
            pulumi.set(__self__, "telemetries", telemetries)

    @property
    @pulumi.getter(name="allowCookies")
    def allow_cookies(self) -> Optional[bool]:
        """
        If you set this to `true`, RUM web client sets two cookies, a session cookie  and a user cookie. The cookies allow the RUM web client to collect data relating to the number of users an application has and the behavior of the application across a sequence of events. Cookies are stored in the top-level domain of the current page.
        """
        return pulumi.get(self, "allow_cookies")

    @property
    @pulumi.getter(name="enableXray")
    def enable_xray(self) -> Optional[bool]:
        """
        If you set this to `true`, RUM enables X-Ray tracing for the user sessions  that RUM samples. RUM adds an X-Ray trace header to allowed HTTP requests. It also records an X-Ray segment for allowed HTTP requests.
        """
        return pulumi.get(self, "enable_xray")

    @property
    @pulumi.getter(name="excludedPages")
    def excluded_pages(self) -> Optional[Sequence[str]]:
        """
        A list of URLs in your website or application to exclude from RUM data collection.
        """
        return pulumi.get(self, "excluded_pages")

    @property
    @pulumi.getter(name="favoritePages")
    def favorite_pages(self) -> Optional[Sequence[str]]:
        """
        A list of pages in the CloudWatch RUM console that are to be displayed with a "favorite" icon.
        """
        return pulumi.get(self, "favorite_pages")

    @property
    @pulumi.getter(name="guestRoleArn")
    def guest_role_arn(self) -> Optional[str]:
        """
        The ARN of the guest IAM role that is attached to the Amazon Cognito identity pool that is used to authorize the sending of data to RUM.
        """
        return pulumi.get(self, "guest_role_arn")

    @property
    @pulumi.getter(name="identityPoolId")
    def identity_pool_id(self) -> Optional[str]:
        """
        The ID of the Amazon Cognito identity pool that is used to authorize the sending of data to RUM.
        """
        return pulumi.get(self, "identity_pool_id")

    @property
    @pulumi.getter(name="includedPages")
    def included_pages(self) -> Optional[Sequence[str]]:
        """
        If this app monitor is to collect data from only certain pages in your application, this structure lists those pages.
        """
        return pulumi.get(self, "included_pages")

    @property
    @pulumi.getter(name="sessionSampleRate")
    def session_sample_rate(self) -> Optional[float]:
        """
        Specifies the percentage of user sessions to use for RUM data collection. Choosing a higher percentage gives you more data but also incurs more costs. The number you specify is the percentage of user sessions that will be used. Default value is `0.1`.
        """
        return pulumi.get(self, "session_sample_rate")

    @property
    @pulumi.getter
    def telemetries(self) -> Optional[Sequence[str]]:
        """
        An array that lists the types of telemetry data that this app monitor is to collect. Valid values are `errors`, `performance`, and `http`.
        """
        return pulumi.get(self, "telemetries")


@pulumi.output_type
class AppMonitorCustomEvents(dict):
    def __init__(__self__, *,
                 status: Optional[str] = None):
        """
        :param str status: Specifies whether this app monitor allows the web client to define and send custom events. The default is for custom events to be `DISABLED`. Valid values are `DISABLED` and `ENABLED`.
        """
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        Specifies whether this app monitor allows the web client to define and send custom events. The default is for custom events to be `DISABLED`. Valid values are `DISABLED` and `ENABLED`.
        """
        return pulumi.get(self, "status")


