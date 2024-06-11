from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    name: str,
    *,
    exact: Union[None, Unset, bool] = False,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    json_exact: Union[None, Unset, bool]
    if isinstance(exact, Unset):
        json_exact = UNSET
    else:
        json_exact = exact
    params["exact"] = json_exact

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "get",
        "url": f"/collection/size/{name}",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, int]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(int, response.json())
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
) -> Response[Union[Any, HTTPValidationError, int]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[None, Unset, bool] = False,
) -> Response[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, int]]
    """

    kwargs = _get_kwargs(
        name=name,
        exact=exact,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[None, Unset, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, int]
    """

    return sync_detailed(
        name=name,
        client=client,
        exact=exact,
    ).parsed


async def asyncio_detailed(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[None, Unset, bool] = False,
) -> Response[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, int]]
    """

    kwargs = _get_kwargs(
        name=name,
        exact=exact,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    name: str,
    *,
    client: AuthenticatedClient,
    exact: Union[None, Unset, bool] = False,
) -> Optional[Union[Any, HTTPValidationError, int]]:
    """Sizeof Collection

     Get the number of entities in a collection

    Args:
        name (str):
        exact (Union[None, Unset, bool]):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, int]
    """

    return (
        await asyncio_detailed(
            name=name,
            client=client,
            exact=exact,
        )
    ).parsed
