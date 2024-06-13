"""
Type annotations for securitylake service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_securitylake.client import SecurityLakeClient

    session = Session()
    client: SecurityLakeClient = session.client("securitylake")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import AccessTypeType
from .paginator import (
    GetDataLakeSourcesPaginator,
    ListDataLakeExceptionsPaginator,
    ListLogSourcesPaginator,
    ListSubscribersPaginator,
)
from .type_defs import (
    AwsIdentityTypeDef,
    AwsLogSourceConfigurationTypeDef,
    CreateAwsLogSourceResponseTypeDef,
    CreateCustomLogSourceResponseTypeDef,
    CreateDataLakeResponseTypeDef,
    CreateSubscriberNotificationResponseTypeDef,
    CreateSubscriberResponseTypeDef,
    CustomLogSourceConfigurationTypeDef,
    DataLakeAutoEnableNewAccountConfigurationUnionTypeDef,
    DataLakeConfigurationTypeDef,
    DeleteAwsLogSourceResponseTypeDef,
    GetDataLakeExceptionSubscriptionResponseTypeDef,
    GetDataLakeOrganizationConfigurationResponseTypeDef,
    GetDataLakeSourcesResponseTypeDef,
    GetSubscriberResponseTypeDef,
    ListDataLakeExceptionsResponseTypeDef,
    ListDataLakesResponseTypeDef,
    ListLogSourcesResponseTypeDef,
    ListSubscribersResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    LogSourceResourceTypeDef,
    NotificationConfigurationTypeDef,
    TagTypeDef,
    UpdateDataLakeResponseTypeDef,
    UpdateSubscriberNotificationResponseTypeDef,
    UpdateSubscriberResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("SecurityLakeClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]

class SecurityLakeClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecurityLakeClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#close)
        """

    def create_aws_log_source(
        self, *, sources: Sequence[AwsLogSourceConfigurationTypeDef]
    ) -> CreateAwsLogSourceResponseTypeDef:
        """
        Adds a natively supported Amazon Web Service as an Amazon Security Lake source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_aws_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_aws_log_source)
        """

    def create_custom_log_source(
        self,
        *,
        configuration: CustomLogSourceConfigurationTypeDef,
        sourceName: str,
        eventClasses: Sequence[str] = ...,
        sourceVersion: str = ...,
    ) -> CreateCustomLogSourceResponseTypeDef:
        """
        Adds a third-party custom source in Amazon Security Lake, from the Amazon Web
        Services Region where you want to create a custom
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_custom_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_custom_log_source)
        """

    def create_data_lake(
        self,
        *,
        configurations: Sequence[DataLakeConfigurationTypeDef],
        metaStoreManagerRoleArn: str,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreateDataLakeResponseTypeDef:
        """
        Initializes an Amazon Security Lake instance with the provided (or default)
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_data_lake)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_data_lake)
        """

    def create_data_lake_exception_subscription(
        self,
        *,
        notificationEndpoint: str,
        subscriptionProtocol: str,
        exceptionTimeToLive: int = ...,
    ) -> Dict[str, Any]:
        """
        Creates the specified notification subscription in Amazon Security Lake for the
        organization you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_data_lake_exception_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_data_lake_exception_subscription)
        """

    def create_data_lake_organization_configuration(
        self,
        *,
        autoEnableNewAccount: Sequence[DataLakeAutoEnableNewAccountConfigurationUnionTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Automatically enables Amazon Security Lake for new member accounts in your
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_data_lake_organization_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_data_lake_organization_configuration)
        """

    def create_subscriber(
        self,
        *,
        sources: Sequence[LogSourceResourceTypeDef],
        subscriberIdentity: AwsIdentityTypeDef,
        subscriberName: str,
        accessTypes: Sequence[AccessTypeType] = ...,
        subscriberDescription: str = ...,
        tags: Sequence[TagTypeDef] = ...,
    ) -> CreateSubscriberResponseTypeDef:
        """
        Creates a subscription permission for accounts that are already enabled in
        Amazon Security
        Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_subscriber)
        """

    def create_subscriber_notification(
        self, *, configuration: NotificationConfigurationTypeDef, subscriberId: str
    ) -> CreateSubscriberNotificationResponseTypeDef:
        """
        Notifies the subscriber when new data is written to the data lake for the
        sources that the subscriber consumes in Security
        Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.create_subscriber_notification)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#create_subscriber_notification)
        """

    def delete_aws_log_source(
        self, *, sources: Sequence[AwsLogSourceConfigurationTypeDef]
    ) -> DeleteAwsLogSourceResponseTypeDef:
        """
        Removes a natively supported Amazon Web Service as an Amazon Security Lake
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_aws_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_aws_log_source)
        """

    def delete_custom_log_source(
        self, *, sourceName: str, sourceVersion: str = ...
    ) -> Dict[str, Any]:
        """
        Removes a custom log source from Amazon Security Lake, to stop sending data
        from the custom source to Security
        Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_custom_log_source)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_custom_log_source)
        """

    def delete_data_lake(self, *, regions: Sequence[str]) -> Dict[str, Any]:
        """
        When you disable Amazon Security Lake from your account, Security Lake is
        disabled in all Amazon Web Services Regions and it stops collecting data from
        your
        sources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_data_lake)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_data_lake)
        """

    def delete_data_lake_exception_subscription(self) -> Dict[str, Any]:
        """
        Deletes the specified notification subscription in Amazon Security Lake for the
        organization you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_data_lake_exception_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_data_lake_exception_subscription)
        """

    def delete_data_lake_organization_configuration(
        self,
        *,
        autoEnableNewAccount: Sequence[DataLakeAutoEnableNewAccountConfigurationUnionTypeDef] = ...,
    ) -> Dict[str, Any]:
        """
        Turns off automatic enablement of Amazon Security Lake for member accounts that
        are added to an organization in
        Organizations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_data_lake_organization_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_data_lake_organization_configuration)
        """

    def delete_subscriber(self, *, subscriberId: str) -> Dict[str, Any]:
        """
        Deletes the subscription permission and all notification settings for accounts
        that are already enabled in Amazon Security
        Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_subscriber)
        """

    def delete_subscriber_notification(self, *, subscriberId: str) -> Dict[str, Any]:
        """
        Deletes the specified notification subscription in Amazon Security Lake for the
        organization you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.delete_subscriber_notification)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#delete_subscriber_notification)
        """

    def deregister_data_lake_delegated_administrator(self) -> Dict[str, Any]:
        """
        Deletes the Amazon Security Lake delegated administrator account for the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.deregister_data_lake_delegated_administrator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#deregister_data_lake_delegated_administrator)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#generate_presigned_url)
        """

    def get_data_lake_exception_subscription(
        self,
    ) -> GetDataLakeExceptionSubscriptionResponseTypeDef:
        """
        Retrieves the details of exception notifications for the account in Amazon
        Security
        Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_data_lake_exception_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_data_lake_exception_subscription)
        """

    def get_data_lake_organization_configuration(
        self,
    ) -> GetDataLakeOrganizationConfigurationResponseTypeDef:
        """
        Retrieves the configuration that will be automatically set up for accounts
        added to the organization after the organization has onboarded to Amazon
        Security
        Lake.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_data_lake_organization_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_data_lake_organization_configuration)
        """

    def get_data_lake_sources(
        self, *, accounts: Sequence[str] = ..., maxResults: int = ..., nextToken: str = ...
    ) -> GetDataLakeSourcesResponseTypeDef:
        """
        Retrieves a snapshot of the current Region, including whether Amazon Security
        Lake is enabled for those accounts and which sources Security Lake is
        collecting data
        from.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_data_lake_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_data_lake_sources)
        """

    def get_subscriber(self, *, subscriberId: str) -> GetSubscriberResponseTypeDef:
        """
        Retrieves the subscription information for the specified subscription ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_subscriber)
        """

    def list_data_lake_exceptions(
        self, *, maxResults: int = ..., nextToken: str = ..., regions: Sequence[str] = ...
    ) -> ListDataLakeExceptionsResponseTypeDef:
        """
        Lists the Amazon Security Lake exceptions that you can use to find the source
        of problems and fix
        them.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_data_lake_exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_data_lake_exceptions)
        """

    def list_data_lakes(self, *, regions: Sequence[str] = ...) -> ListDataLakesResponseTypeDef:
        """
        Retrieves the Amazon Security Lake configuration object for the specified
        Amazon Web Services
        Regions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_data_lakes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_data_lakes)
        """

    def list_log_sources(
        self,
        *,
        accounts: Sequence[str] = ...,
        maxResults: int = ...,
        nextToken: str = ...,
        regions: Sequence[str] = ...,
        sources: Sequence[LogSourceResourceTypeDef] = ...,
    ) -> ListLogSourcesResponseTypeDef:
        """
        Retrieves the log sources in the current Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_log_sources)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_log_sources)
        """

    def list_subscribers(
        self, *, maxResults: int = ..., nextToken: str = ...
    ) -> ListSubscribersResponseTypeDef:
        """
        List all subscribers for the specific Amazon Security Lake account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_subscribers)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_subscribers)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the tags (keys and values) that are associated with an Amazon
        Security Lake resource: a subscriber, or the data lake configuration for your
        Amazon Web Services account in a particular Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#list_tags_for_resource)
        """

    def register_data_lake_delegated_administrator(self, *, accountId: str) -> Dict[str, Any]:
        """
        Designates the Amazon Security Lake delegated administrator account for the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.register_data_lake_delegated_administrator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#register_data_lake_delegated_administrator)
        """

    def tag_resource(self, *, resourceArn: str, tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Adds or updates one or more tags that are associated with an Amazon Security
        Lake resource: a subscriber, or the data lake configuration for your Amazon Web
        Services account in a particular Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes one or more tags (keys and values) from an Amazon Security Lake
        resource: a subscriber, or the data lake configuration for your Amazon Web
        Services account in a particular Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#untag_resource)
        """

    def update_data_lake(
        self,
        *,
        configurations: Sequence[DataLakeConfigurationTypeDef],
        metaStoreManagerRoleArn: str = ...,
    ) -> UpdateDataLakeResponseTypeDef:
        """
        Specifies where to store your security data and for how long.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_data_lake)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_data_lake)
        """

    def update_data_lake_exception_subscription(
        self,
        *,
        notificationEndpoint: str,
        subscriptionProtocol: str,
        exceptionTimeToLive: int = ...,
    ) -> Dict[str, Any]:
        """
        Updates the specified notification subscription in Amazon Security Lake for the
        organization you
        specify.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_data_lake_exception_subscription)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_data_lake_exception_subscription)
        """

    def update_subscriber(
        self,
        *,
        subscriberId: str,
        sources: Sequence[LogSourceResourceTypeDef] = ...,
        subscriberDescription: str = ...,
        subscriberIdentity: AwsIdentityTypeDef = ...,
        subscriberName: str = ...,
    ) -> UpdateSubscriberResponseTypeDef:
        """
        Updates an existing subscription for the given Amazon Security Lake account ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_subscriber)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_subscriber)
        """

    def update_subscriber_notification(
        self, *, configuration: NotificationConfigurationTypeDef, subscriberId: str
    ) -> UpdateSubscriberNotificationResponseTypeDef:
        """
        Updates an existing notification method for the subscription (SQS or HTTPs
        endpoint) or switches the notification subscription endpoint for a
        subscriber.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.update_subscriber_notification)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#update_subscriber_notification)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["get_data_lake_sources"]
    ) -> GetDataLakeSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_data_lake_exceptions"]
    ) -> ListDataLakeExceptionsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_log_sources"]) -> ListLogSourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_subscribers"]
    ) -> ListSubscribersPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securitylake.html#SecurityLake.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securitylake/client/#get_paginator)
        """
