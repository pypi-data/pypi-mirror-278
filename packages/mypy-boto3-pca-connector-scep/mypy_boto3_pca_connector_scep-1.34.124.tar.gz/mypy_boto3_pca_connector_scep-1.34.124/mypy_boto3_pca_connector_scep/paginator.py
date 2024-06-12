"""
Type annotations for pca-connector-scep service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_scep/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_pca_connector_scep.client import PrivateCAConnectorforSCEPClient
    from mypy_boto3_pca_connector_scep.paginator import (
        ListChallengeMetadataPaginator,
        ListConnectorsPaginator,
    )

    session = Session()
    client: PrivateCAConnectorforSCEPClient = session.client("pca-connector-scep")

    list_challenge_metadata_paginator: ListChallengeMetadataPaginator = client.get_paginator("list_challenge_metadata")
    list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    ```
"""

from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListChallengeMetadataResponseTypeDef,
    ListConnectorsResponseTypeDef,
    PaginatorConfigTypeDef,
)

__all__ = ("ListChallengeMetadataPaginator", "ListConnectorsPaginator")

_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListChallengeMetadataPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep.html#PrivateCAConnectorforSCEP.Paginator.ListChallengeMetadata)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_scep/paginators/#listchallengemetadatapaginator)
    """

    def paginate(
        self, *, ConnectorArn: str, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListChallengeMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep.html#PrivateCAConnectorforSCEP.Paginator.ListChallengeMetadata.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_scep/paginators/#listchallengemetadatapaginator)
        """


class ListConnectorsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep.html#PrivateCAConnectorforSCEP.Paginator.ListConnectors)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_scep/paginators/#listconnectorspaginator)
    """

    def paginate(
        self, *, PaginationConfig: PaginatorConfigTypeDef = ...
    ) -> _PageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep.html#PrivateCAConnectorforSCEP.Paginator.ListConnectors.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_pca_connector_scep/paginators/#listconnectorspaginator)
        """
