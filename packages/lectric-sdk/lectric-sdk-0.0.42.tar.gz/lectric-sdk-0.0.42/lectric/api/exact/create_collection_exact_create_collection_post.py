from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.collection import Collection
from ...models.collection_in_spec import CollectionInSpec
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, bool] = False,
    with_dupe_counter: Union[Unset, bool] = False,
    hash_algo: Union[Unset, str] = "md5",
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["with_reverse_lookup"] = with_reverse_lookup

    params["with_dupe_counter"] = with_dupe_counter

    params["hash_algo"] = hash_algo

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/exact/create/collection",
        "params": params,
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Collection.from_dict(response.json())

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
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, bool] = False,
    with_dupe_counter: Union[Unset, bool] = False,
    hash_algo: Union[Unset, str] = "md5",
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, bool]):  Default: False.
        with_dupe_counter (Union[Unset, bool]):  Default: False.
        hash_algo (Union[Unset, str]):  Default: 'md5'.
        body (CollectionInSpec):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        with_reverse_lookup=with_reverse_lookup,
        with_dupe_counter=with_dupe_counter,
        hash_algo=hash_algo,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, bool] = False,
    with_dupe_counter: Union[Unset, bool] = False,
    hash_algo: Union[Unset, str] = "md5",
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, bool]):  Default: False.
        with_dupe_counter (Union[Unset, bool]):  Default: False.
        hash_algo (Union[Unset, str]):  Default: 'md5'.
        body (CollectionInSpec):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Collection, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
        with_reverse_lookup=with_reverse_lookup,
        with_dupe_counter=with_dupe_counter,
        hash_algo=hash_algo,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, bool] = False,
    with_dupe_counter: Union[Unset, bool] = False,
    hash_algo: Union[Unset, str] = "md5",
) -> Response[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, bool]):  Default: False.
        with_dupe_counter (Union[Unset, bool]):  Default: False.
        hash_algo (Union[Unset, str]):  Default: 'md5'.
        body (CollectionInSpec):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, Collection, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        with_reverse_lookup=with_reverse_lookup,
        with_dupe_counter=with_dupe_counter,
        hash_algo=hash_algo,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CollectionInSpec,
    with_reverse_lookup: Union[Unset, bool] = False,
    with_dupe_counter: Union[Unset, bool] = False,
    hash_algo: Union[Unset, str] = "md5",
) -> Optional[Union[Any, Collection, HTTPValidationError]]:
    """Create Collection

     Create a collection by name with a specific schema

    Args:
        with_reverse_lookup (Union[Unset, bool]):  Default: False.
        with_dupe_counter (Union[Unset, bool]):  Default: False.
        hash_algo (Union[Unset, str]):  Default: 'md5'.
        body (CollectionInSpec):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, Collection, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            with_reverse_lookup=with_reverse_lookup,
            with_dupe_counter=with_dupe_counter,
            hash_algo=hash_algo,
        )
    ).parsed
