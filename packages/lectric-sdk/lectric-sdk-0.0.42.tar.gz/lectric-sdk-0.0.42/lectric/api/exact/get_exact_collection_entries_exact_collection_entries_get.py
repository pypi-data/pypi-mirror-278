import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.exact_collection_entry import ExactCollectionEntry
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collection_name: str,
    ingestor: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    ingest_source: Union[None, Unset, str] = UNSET,
    traits: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["collection_name"] = collection_name

    params["ingestor"] = ingestor

    json_start_date: Union[None, Unset, str]
    if isinstance(start_date, Unset):
        json_start_date = UNSET
    elif isinstance(start_date, datetime.date):
        json_start_date = start_date.isoformat()
    else:
        json_start_date = start_date
    params["start_date"] = json_start_date

    json_end_date: Union[None, Unset, str]
    if isinstance(end_date, Unset):
        json_end_date = UNSET
    elif isinstance(end_date, datetime.date):
        json_end_date = end_date.isoformat()
    else:
        json_end_date = end_date
    params["end_date"] = json_end_date

    json_ingest_source: Union[None, Unset, str]
    if isinstance(ingest_source, Unset):
        json_ingest_source = UNSET
    else:
        json_ingest_source = ingest_source
    params["ingest_source"] = json_ingest_source

    json_traits: Union[None, Unset, str]
    if isinstance(traits, Unset):
        json_traits = UNSET
    else:
        json_traits = traits
    params["traits"] = json_traits

    json_order_by: Union[None, Unset, str]
    if isinstance(order_by, Unset):
        json_order_by = UNSET
    else:
        json_order_by = order_by
    params["order_by"] = json_order_by

    params["desc"] = desc

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": "/exact/collection_entries",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, List["ExactCollectionEntry"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExactCollectionEntry.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, List["ExactCollectionEntry"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    ingestor: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    ingest_source: Union[None, Unset, str] = UNSET,
    traits: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[Any, HTTPValidationError, List["ExactCollectionEntry"]]]:
    """Get Exact Collection Entries

     Get entries from the collection

    Args:
        collection_name (str):
        ingestor (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        ingest_source (Union[None, Unset, str]):
        traits (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['ExactCollectionEntry']]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        ingestor=ingestor,
        start_date=start_date,
        end_date=end_date,
        ingest_source=ingest_source,
        traits=traits,
        order_by=order_by,
        desc=desc,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    ingestor: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    ingest_source: Union[None, Unset, str] = UNSET,
    traits: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[Any, HTTPValidationError, List["ExactCollectionEntry"]]]:
    """Get Exact Collection Entries

     Get entries from the collection

    Args:
        collection_name (str):
        ingestor (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        ingest_source (Union[None, Unset, str]):
        traits (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['ExactCollectionEntry']]
    """

    return sync_detailed(
        client=client,
        collection_name=collection_name,
        ingestor=ingestor,
        start_date=start_date,
        end_date=end_date,
        ingest_source=ingest_source,
        traits=traits,
        order_by=order_by,
        desc=desc,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    ingestor: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    ingest_source: Union[None, Unset, str] = UNSET,
    traits: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[Any, HTTPValidationError, List["ExactCollectionEntry"]]]:
    """Get Exact Collection Entries

     Get entries from the collection

    Args:
        collection_name (str):
        ingestor (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        ingest_source (Union[None, Unset, str]):
        traits (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['ExactCollectionEntry']]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        ingestor=ingestor,
        start_date=start_date,
        end_date=end_date,
        ingest_source=ingest_source,
        traits=traits,
        order_by=order_by,
        desc=desc,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    ingestor: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    ingest_source: Union[None, Unset, str] = UNSET,
    traits: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[Any, HTTPValidationError, List["ExactCollectionEntry"]]]:
    """Get Exact Collection Entries

     Get entries from the collection

    Args:
        collection_name (str):
        ingestor (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        ingest_source (Union[None, Unset, str]):
        traits (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['ExactCollectionEntry']]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection_name=collection_name,
            ingestor=ingestor,
            start_date=start_date,
            end_date=end_date,
            ingest_source=ingest_source,
            traits=traits,
            order_by=order_by,
            desc=desc,
            limit=limit,
        )
    ).parsed
