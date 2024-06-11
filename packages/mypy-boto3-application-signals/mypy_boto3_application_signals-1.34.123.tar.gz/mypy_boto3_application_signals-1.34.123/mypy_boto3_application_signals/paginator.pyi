"""
Type annotations for application-signals service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_application_signals.client import CloudWatchApplicationSignalsClient
    from mypy_boto3_application_signals.paginator import (
        ListServiceDependenciesPaginator,
        ListServiceDependentsPaginator,
        ListServiceLevelObjectivesPaginator,
        ListServiceOperationsPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: CloudWatchApplicationSignalsClient = session.client("application-signals")

    list_service_dependencies_paginator: ListServiceDependenciesPaginator = client.get_paginator("list_service_dependencies")
    list_service_dependents_paginator: ListServiceDependentsPaginator = client.get_paginator("list_service_dependents")
    list_service_level_objectives_paginator: ListServiceLevelObjectivesPaginator = client.get_paginator("list_service_level_objectives")
    list_service_operations_paginator: ListServiceOperationsPaginator = client.get_paginator("list_service_operations")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from typing import Generic, Iterator, Mapping, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListServiceDependenciesOutputTypeDef,
    ListServiceDependentsOutputTypeDef,
    ListServiceLevelObjectivesOutputTypeDef,
    ListServiceOperationsOutputTypeDef,
    ListServicesOutputTypeDef,
    PaginatorConfigTypeDef,
    TimestampTypeDef,
)

__all__ = (
    "ListServiceDependenciesPaginator",
    "ListServiceDependentsPaginator",
    "ListServiceLevelObjectivesPaginator",
    "ListServiceOperationsPaginator",
    "ListServicesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListServiceDependenciesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependenciespaginator)
    """

    def paginate(
        self,
        *,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        KeyAttributes: Mapping[str, str],
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListServiceDependenciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependenciespaginator)
        """

class ListServiceDependentsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependentspaginator)
    """

    def paginate(
        self,
        *,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        KeyAttributes: Mapping[str, str],
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListServiceDependentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependentspaginator)
        """

class ListServiceLevelObjectivesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectivespaginator)
    """

    def paginate(
        self,
        *,
        KeyAttributes: Mapping[str, str] = ...,
        OperationName: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListServiceLevelObjectivesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectivespaginator)
        """

class ListServiceOperationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listserviceoperationspaginator)
    """

    def paginate(
        self,
        *,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        KeyAttributes: Mapping[str, str],
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListServiceOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listserviceoperationspaginator)
        """

class ListServicesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicespaginator)
    """

    def paginate(
        self,
        *,
        StartTime: TimestampTypeDef,
        EndTime: TimestampTypeDef,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals.html#CloudWatchApplicationSignals.Paginator.ListServices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicespaginator)
        """
