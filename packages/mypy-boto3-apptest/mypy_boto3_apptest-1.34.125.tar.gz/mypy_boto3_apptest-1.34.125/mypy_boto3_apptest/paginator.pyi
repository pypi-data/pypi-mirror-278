"""
Type annotations for apptest service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_apptest.client import MainframeModernizationApplicationTestingClient
    from mypy_boto3_apptest.paginator import (
        ListTestCasesPaginator,
        ListTestConfigurationsPaginator,
        ListTestRunStepsPaginator,
        ListTestRunTestCasesPaginator,
        ListTestRunsPaginator,
        ListTestSuitesPaginator,
    )

    session = Session()
    client: MainframeModernizationApplicationTestingClient = session.client("apptest")

    list_test_cases_paginator: ListTestCasesPaginator = client.get_paginator("list_test_cases")
    list_test_configurations_paginator: ListTestConfigurationsPaginator = client.get_paginator("list_test_configurations")
    list_test_run_steps_paginator: ListTestRunStepsPaginator = client.get_paginator("list_test_run_steps")
    list_test_run_test_cases_paginator: ListTestRunTestCasesPaginator = client.get_paginator("list_test_run_test_cases")
    list_test_runs_paginator: ListTestRunsPaginator = client.get_paginator("list_test_runs")
    list_test_suites_paginator: ListTestSuitesPaginator = client.get_paginator("list_test_suites")
    ```
"""

from typing import Generic, Iterator, Sequence, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListTestCasesResponseTypeDef,
    ListTestConfigurationsResponseTypeDef,
    ListTestRunsResponseTypeDef,
    ListTestRunStepsResponseTypeDef,
    ListTestRunTestCasesResponseTypeDef,
    ListTestSuitesResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = (
    "ListTestCasesPaginator",
    "ListTestConfigurationsPaginator",
    "ListTestRunStepsPaginator",
    "ListTestRunTestCasesPaginator",
    "ListTestRunsPaginator",
    "ListTestSuitesPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListTestCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestCases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestcasespaginator)
    """

    def paginate(
        self, *, testCaseIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTestCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestCases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestcasespaginator)
        """

class ListTestConfigurationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestConfigurations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestconfigurationspaginator)
    """

    def paginate(
        self,
        *,
        testConfigurationIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListTestConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestConfigurations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestconfigurationspaginator)
        """

class ListTestRunStepsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunSteps)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestrunstepspaginator)
    """

    def paginate(
        self,
        *,
        testRunId: str,
        testCaseId: str = ...,
        testSuiteId: str = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListTestRunStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunSteps.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestrunstepspaginator)
        """

class ListTestRunTestCasesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunTestCases)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestruntestcasespaginator)
    """

    def paginate(
        self, *, testRunId: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTestRunTestCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunTestCases.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestruntestcasespaginator)
        """

class ListTestRunsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestRuns)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestrunspaginator)
    """

    def paginate(
        self,
        *,
        testSuiteId: str = ...,
        testRunIds: Sequence[str] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListTestRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestRuns.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestrunspaginator)
        """

class ListTestSuitesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestSuites)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestsuitespaginator)
    """

    def paginate(
        self, *, testSuiteIds: Sequence[str] = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListTestSuitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Paginator.ListTestSuites.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/paginators/#listtestsuitespaginator)
        """
