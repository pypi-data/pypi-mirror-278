"""
Type annotations for apptest service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_apptest.client import MainframeModernizationApplicationTestingClient

    session = Session()
    client: MainframeModernizationApplicationTestingClient = session.client("apptest")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .paginator import (
    ListTestCasesPaginator,
    ListTestConfigurationsPaginator,
    ListTestRunsPaginator,
    ListTestRunStepsPaginator,
    ListTestRunTestCasesPaginator,
    ListTestSuitesPaginator,
)
from .type_defs import (
    CreateTestCaseResponseTypeDef,
    CreateTestConfigurationResponseTypeDef,
    CreateTestSuiteResponseTypeDef,
    GetTestCaseResponseTypeDef,
    GetTestConfigurationResponseTypeDef,
    GetTestRunStepResponseTypeDef,
    GetTestSuiteResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTestCasesResponseTypeDef,
    ListTestConfigurationsResponseTypeDef,
    ListTestRunsResponseTypeDef,
    ListTestRunStepsResponseTypeDef,
    ListTestRunTestCasesResponseTypeDef,
    ListTestSuitesResponseTypeDef,
    ResourceUnionTypeDef,
    ServiceSettingsTypeDef,
    StartTestRunResponseTypeDef,
    StepUnionTypeDef,
    TestCasesUnionTypeDef,
    UpdateTestCaseResponseTypeDef,
    UpdateTestConfigurationResponseTypeDef,
    UpdateTestSuiteResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("MainframeModernizationApplicationTestingClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class MainframeModernizationApplicationTestingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MainframeModernizationApplicationTestingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#close)
        """

    def create_test_case(
        self,
        *,
        name: str,
        steps: Sequence[StepUnionTypeDef],
        description: str = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateTestCaseResponseTypeDef:
        """
        Creates a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.create_test_case)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#create_test_case)
        """

    def create_test_configuration(
        self,
        *,
        name: str,
        resources: Sequence[ResourceUnionTypeDef],
        description: str = ...,
        properties: Mapping[str, str] = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
        serviceSettings: ServiceSettingsTypeDef = ...,
    ) -> CreateTestConfigurationResponseTypeDef:
        """
        Creates a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.create_test_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#create_test_configuration)
        """

    def create_test_suite(
        self,
        *,
        name: str,
        testCases: TestCasesUnionTypeDef,
        description: str = ...,
        beforeSteps: Sequence[StepUnionTypeDef] = ...,
        afterSteps: Sequence[StepUnionTypeDef] = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreateTestSuiteResponseTypeDef:
        """
        Creates a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.create_test_suite)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#create_test_suite)
        """

    def delete_test_case(self, *, testCaseId: str) -> Dict[str, Any]:
        """
        Deletes a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.delete_test_case)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#delete_test_case)
        """

    def delete_test_configuration(self, *, testConfigurationId: str) -> Dict[str, Any]:
        """
        Deletes a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.delete_test_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#delete_test_configuration)
        """

    def delete_test_run(self, *, testRunId: str) -> Dict[str, Any]:
        """
        Deletes a test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.delete_test_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#delete_test_run)
        """

    def delete_test_suite(self, *, testSuiteId: str) -> Dict[str, Any]:
        """
        Deletes a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.delete_test_suite)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#delete_test_suite)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#generate_presigned_url)
        """

    def get_test_case(
        self, *, testCaseId: str, testCaseVersion: int = ...
    ) -> GetTestCaseResponseTypeDef:
        """
        Gets a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_test_case)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_test_case)
        """

    def get_test_configuration(
        self, *, testConfigurationId: str, testConfigurationVersion: int = ...
    ) -> GetTestConfigurationResponseTypeDef:
        """
        Gets a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_test_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_test_configuration)
        """

    def get_test_run_step(
        self, *, testRunId: str, stepName: str, testCaseId: str = ..., testSuiteId: str = ...
    ) -> GetTestRunStepResponseTypeDef:
        """
        Gets a test run step.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_test_run_step)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_test_run_step)
        """

    def get_test_suite(
        self, *, testSuiteId: str, testSuiteVersion: int = ...
    ) -> GetTestSuiteResponseTypeDef:
        """
        Gets a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_test_suite)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_test_suite)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#list_tags_for_resource)
        """

    def list_test_cases(
        self, *, testCaseIds: Sequence[str] = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListTestCasesResponseTypeDef:
        """
        Lists test cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.list_test_cases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#list_test_cases)
        """

    def list_test_configurations(
        self,
        *,
        testConfigurationIds: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListTestConfigurationsResponseTypeDef:
        """
        Lists test configurations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.list_test_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#list_test_configurations)
        """

    def list_test_run_steps(
        self,
        *,
        testRunId: str,
        testCaseId: str = ...,
        testSuiteId: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListTestRunStepsResponseTypeDef:
        """
        Lists test run steps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.list_test_run_steps)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#list_test_run_steps)
        """

    def list_test_run_test_cases(
        self, *, testRunId: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListTestRunTestCasesResponseTypeDef:
        """
        Lists test run test cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.list_test_run_test_cases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#list_test_run_test_cases)
        """

    def list_test_runs(
        self,
        *,
        testSuiteId: str = ...,
        testRunIds: Sequence[str] = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListTestRunsResponseTypeDef:
        """
        Lists test runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.list_test_runs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#list_test_runs)
        """

    def list_test_suites(
        self, *, testSuiteIds: Sequence[str] = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListTestSuitesResponseTypeDef:
        """
        Lists test suites.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.list_test_suites)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#list_test_suites)
        """

    def start_test_run(
        self,
        *,
        testSuiteId: str,
        testConfigurationId: str = ...,
        clientToken: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> StartTestRunResponseTypeDef:
        """
        Starts a test run.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.start_test_run)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#start_test_run)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Specifies tags of a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Untags a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#untag_resource)
        """

    def update_test_case(
        self, *, testCaseId: str, description: str = ..., steps: Sequence[StepUnionTypeDef] = ...
    ) -> UpdateTestCaseResponseTypeDef:
        """
        Updates a test case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.update_test_case)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#update_test_case)
        """

    def update_test_configuration(
        self,
        *,
        testConfigurationId: str,
        description: str = ...,
        resources: Sequence[ResourceUnionTypeDef] = ...,
        properties: Mapping[str, str] = ...,
        serviceSettings: ServiceSettingsTypeDef = ...,
    ) -> UpdateTestConfigurationResponseTypeDef:
        """
        Updates a test configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.update_test_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#update_test_configuration)
        """

    def update_test_suite(
        self,
        *,
        testSuiteId: str,
        description: str = ...,
        beforeSteps: Sequence[StepUnionTypeDef] = ...,
        afterSteps: Sequence[StepUnionTypeDef] = ...,
        testCases: TestCasesUnionTypeDef = ...,
    ) -> UpdateTestSuiteResponseTypeDef:
        """
        Updates a test suite.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.update_test_suite)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#update_test_suite)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_test_cases"]) -> ListTestCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_test_configurations"]
    ) -> ListTestConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_test_run_steps"]
    ) -> ListTestRunStepsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_test_run_test_cases"]
    ) -> ListTestRunTestCasesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_test_runs"]) -> ListTestRunsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_test_suites"]) -> ListTestSuitesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest.html#MainframeModernizationApplicationTesting.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_apptest/client/#get_paginator)
        """
