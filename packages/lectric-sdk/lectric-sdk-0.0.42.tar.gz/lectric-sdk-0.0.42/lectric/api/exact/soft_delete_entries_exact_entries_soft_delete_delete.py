from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_soft_delete_entries_exact_entries_soft_delete_delete import (
    BodySoftDeleteEntriesExactEntriesSoftDeleteDelete,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodySoftDeleteEntriesExactEntriesSoftDeleteDelete,
    collection_name: str,
    deleter: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["collection_name"] = collection_name

    json_deleter: Union[None, Unset, str]
    if isinstance(deleter, Unset):
        json_deleter = UNSET
    else:
        json_deleter = deleter
    params["deleter"] = json_deleter

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "delete",
        "url": "/exact/entries/soft-delete",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = response.json()
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
) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: BodySoftDeleteEntriesExactEntriesSoftDeleteDelete,
    collection_name: str,
    deleter: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Soft Delete Entries

     Soft-delete entries in exact collections

    Args:
        collection_name (str):
        deleter (Union[None, Unset, str]):
        body (BodySoftDeleteEntriesExactEntriesSoftDeleteDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_name=collection_name,
        deleter=deleter,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: BodySoftDeleteEntriesExactEntriesSoftDeleteDelete,
    collection_name: str,
    deleter: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Soft Delete Entries

     Soft-delete entries in exact collections

    Args:
        collection_name (str):
        deleter (Union[None, Unset, str]):
        body (BodySoftDeleteEntriesExactEntriesSoftDeleteDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
        collection_name=collection_name,
        deleter=deleter,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodySoftDeleteEntriesExactEntriesSoftDeleteDelete,
    collection_name: str,
    deleter: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Soft Delete Entries

     Soft-delete entries in exact collections

    Args:
        collection_name (str):
        deleter (Union[None, Unset, str]):
        body (BodySoftDeleteEntriesExactEntriesSoftDeleteDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_name=collection_name,
        deleter=deleter,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BodySoftDeleteEntriesExactEntriesSoftDeleteDelete,
    collection_name: str,
    deleter: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Soft Delete Entries

     Soft-delete entries in exact collections

    Args:
        collection_name (str):
        deleter (Union[None, Unset, str]):
        body (BodySoftDeleteEntriesExactEntriesSoftDeleteDelete):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            collection_name=collection_name,
            deleter=deleter,
        )
    ).parsed
