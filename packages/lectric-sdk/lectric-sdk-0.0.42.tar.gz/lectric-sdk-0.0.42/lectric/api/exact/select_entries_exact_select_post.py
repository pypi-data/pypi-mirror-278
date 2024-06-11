from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.select_entries_exact_select_post_response_200_item import SelectEntriesExactSelectPostResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    collection_name: str,
    what: Union[None, Unset, str] = "*",
    where: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 10000,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["collection_name"] = collection_name

    json_what: Union[None, Unset, str]
    if isinstance(what, Unset):
        json_what = UNSET
    else:
        json_what = what
    params["what"] = json_what

    json_where: Union[None, Unset, str]
    if isinstance(where, Unset):
        json_where = UNSET
    else:
        json_where = where
    params["where"] = json_where

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
        "method": "post",
        "url": "/exact/select/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, List["SelectEntriesExactSelectPostResponse200Item"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SelectEntriesExactSelectPostResponse200Item.from_dict(response_200_item_data)

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
) -> Response[Union[Any, HTTPValidationError, List["SelectEntriesExactSelectPostResponse200Item"]]]:
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
    what: Union[None, Unset, str] = "*",
    where: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 10000,
) -> Response[Union[Any, HTTPValidationError, List["SelectEntriesExactSelectPostResponse200Item"]]]:
    """Select Entries

    Args:
        collection_name (str):
        what (Union[None, Unset, str]):  Default: '*'.
        where (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 10000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['SelectEntriesExactSelectPostResponse200Item']]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        what=what,
        where=where,
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
    what: Union[None, Unset, str] = "*",
    where: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 10000,
) -> Optional[Union[Any, HTTPValidationError, List["SelectEntriesExactSelectPostResponse200Item"]]]:
    """Select Entries

    Args:
        collection_name (str):
        what (Union[None, Unset, str]):  Default: '*'.
        where (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 10000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['SelectEntriesExactSelectPostResponse200Item']]
    """

    return sync_detailed(
        client=client,
        collection_name=collection_name,
        what=what,
        where=where,
        order_by=order_by,
        desc=desc,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    collection_name: str,
    what: Union[None, Unset, str] = "*",
    where: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 10000,
) -> Response[Union[Any, HTTPValidationError, List["SelectEntriesExactSelectPostResponse200Item"]]]:
    """Select Entries

    Args:
        collection_name (str):
        what (Union[None, Unset, str]):  Default: '*'.
        where (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 10000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['SelectEntriesExactSelectPostResponse200Item']]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        what=what,
        where=where,
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
    what: Union[None, Unset, str] = "*",
    where: Union[None, Unset, str] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 10000,
) -> Optional[Union[Any, HTTPValidationError, List["SelectEntriesExactSelectPostResponse200Item"]]]:
    """Select Entries

    Args:
        collection_name (str):
        what (Union[None, Unset, str]):  Default: '*'.
        where (Union[None, Unset, str]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 10000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['SelectEntriesExactSelectPostResponse200Item']]
    """

    return (
        await asyncio_detailed(
            client=client,
            collection_name=collection_name,
            what=what,
            where=where,
            order_by=order_by,
            desc=desc,
            limit=limit,
        )
    ).parsed
