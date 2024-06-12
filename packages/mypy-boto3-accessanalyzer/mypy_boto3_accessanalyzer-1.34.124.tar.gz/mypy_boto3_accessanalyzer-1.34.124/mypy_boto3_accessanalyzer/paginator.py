"""
Type annotations for accessanalyzer service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_accessanalyzer.client import AccessAnalyzerClient
    from mypy_boto3_accessanalyzer.paginator import (
        GetFindingRecommendationPaginator,
        GetFindingV2Paginator,
        ListAccessPreviewFindingsPaginator,
        ListAccessPreviewsPaginator,
        ListAnalyzedResourcesPaginator,
        ListAnalyzersPaginator,
        ListArchiveRulesPaginator,
        ListFindingsPaginator,
        ListFindingsV2Paginator,
        ListPolicyGenerationsPaginator,
        ValidatePolicyPaginator,
    )

    session = Session()
    client: AccessAnalyzerClient = session.client("accessanalyzer")

    get_finding_recommendation_paginator: GetFindingRecommendationPaginator = client.get_paginator("get_finding_recommendation")
    get_finding_v2_paginator: GetFindingV2Paginator = client.get_paginator("get_finding_v2")
    list_access_preview_findings_paginator: ListAccessPreviewFindingsPaginator = client.get_paginator("list_access_preview_findings")
    list_access_previews_paginator: ListAccessPreviewsPaginator = client.get_paginator("list_access_previews")
    list_analyzed_resources_paginator: ListAnalyzedResourcesPaginator = client.get_paginator("list_analyzed_resources")
    list_analyzers_paginator: ListAnalyzersPaginator = client.get_paginator("list_analyzers")
    list_archive_rules_paginator: ListArchiveRulesPaginator = client.get_paginator("list_archive_rules")
    list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
    list_findings_v2_paginator: ListFindingsV2Paginator = client.get_paginator("list_findings_v2")
    list_policy_generations_paginator: ListPolicyGenerationsPaginator = client.get_paginator("list_policy_generations")
    validate_policy_paginator: ValidatePolicyPaginator = client.get_paginator("validate_policy")
    ```
"""

from typing import Generic, Iterator, Mapping, TypeVar

from botocore.paginate import PageIterator, Paginator

from .literals import (
    LocaleType,
    PolicyTypeType,
    ResourceTypeType,
    TypeType,
    ValidatePolicyResourceTypeType,
)
from .type_defs import (
    CriterionUnionTypeDef,
    GetFindingRecommendationResponseTypeDef,
    GetFindingV2ResponseTypeDef,
    ListAccessPreviewFindingsResponseTypeDef,
    ListAccessPreviewsResponseTypeDef,
    ListAnalyzedResourcesResponseTypeDef,
    ListAnalyzersResponseTypeDef,
    ListArchiveRulesResponseTypeDef,
    ListFindingsResponseTypeDef,
    ListFindingsV2ResponseTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    PaginatorConfigTypeDef,
    SortCriteriaTypeDef,
    ValidatePolicyResponseTypeDef,
)

__all__ = (
    "GetFindingRecommendationPaginator",
    "GetFindingV2Paginator",
    "ListAccessPreviewFindingsPaginator",
    "ListAccessPreviewsPaginator",
    "ListAnalyzedResourcesPaginator",
    "ListAnalyzersPaginator",
    "ListArchiveRulesPaginator",
    "ListFindingsPaginator",
    "ListFindingsV2Paginator",
    "ListPolicyGenerationsPaginator",
    "ValidatePolicyPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class GetFindingRecommendationPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.GetFindingRecommendation)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#getfindingrecommendationpaginator)
    """

    def paginate(
        self, *, analyzerArn: str, id: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetFindingRecommendationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.GetFindingRecommendation.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#getfindingrecommendationpaginator)
        """


class GetFindingV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.GetFindingV2)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#getfindingv2paginator)
    """

    def paginate(
        self, *, analyzerArn: str, id: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[GetFindingV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.GetFindingV2.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#getfindingv2paginator)
        """


class ListAccessPreviewFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listaccesspreviewfindingspaginator)
    """

    def paginate(
        self,
        *,
        accessPreviewId: str,
        analyzerArn: str,
        filter: Mapping[str, CriterionUnionTypeDef] = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListAccessPreviewFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviewFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listaccesspreviewfindingspaginator)
        """


class ListAccessPreviewsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listaccesspreviewspaginator)
    """

    def paginate(
        self, *, analyzerArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAccessPreviewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAccessPreviews.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listaccesspreviewspaginator)
        """


class ListAnalyzedResourcesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listanalyzedresourcespaginator)
    """

    def paginate(
        self,
        *,
        analyzerArn: str,
        resourceType: ResourceTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListAnalyzedResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzedResources.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listanalyzedresourcespaginator)
        """


class ListAnalyzersPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listanalyzerspaginator)
    """

    def paginate(
        self, *, type: TypeType = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListAnalyzersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListAnalyzers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listanalyzerspaginator)
        """


class ListArchiveRulesPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listarchiverulespaginator)
    """

    def paginate(
        self, *, analyzerName: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListArchiveRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListArchiveRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listarchiverulespaginator)
        """


class ListFindingsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listfindingspaginator)
    """

    def paginate(
        self,
        *,
        analyzerArn: str,
        filter: Mapping[str, CriterionUnionTypeDef] = ...,
        sort: SortCriteriaTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindings.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listfindingspaginator)
        """


class ListFindingsV2Paginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindingsV2)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listfindingsv2paginator)
    """

    def paginate(
        self,
        *,
        analyzerArn: str,
        filter: Mapping[str, CriterionUnionTypeDef] = ...,
        sort: SortCriteriaTypeDef = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ListFindingsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListFindingsV2.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listfindingsv2paginator)
        """


class ListPolicyGenerationsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listpolicygenerationspaginator)
    """

    def paginate(
        self, *, principalArn: str = ..., PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListPolicyGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ListPolicyGenerations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#listpolicygenerationspaginator)
        """


class ValidatePolicyPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#validatepolicypaginator)
    """

    def paginate(
        self,
        *,
        policyDocument: str,
        policyType: PolicyTypeType,
        locale: LocaleType = ...,
        validatePolicyResourceType: ValidatePolicyResourceTypeType = ...,
        PaginationConfig: PaginatorConfigTypeDef = ...,
    ) -> _PageIterator[ValidatePolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer.html#AccessAnalyzer.Paginator.ValidatePolicy.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/paginators/#validatepolicypaginator)
        """
