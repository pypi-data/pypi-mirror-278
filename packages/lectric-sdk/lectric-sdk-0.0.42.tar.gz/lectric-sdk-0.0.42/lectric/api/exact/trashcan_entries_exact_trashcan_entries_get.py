import datetime
from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.trash_can_entry import TrashCanEntry
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    deleter: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}

    params["deleter"] = deleter

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
        "url": "/exact/trashcan_entries",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, List["TrashCanEntry"]]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = TrashCanEntry.from_dict(response_200_item_data)

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
) -> Response[Union[Any, HTTPValidationError, List["TrashCanEntry"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    deleter: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[Any, HTTPValidationError, List["TrashCanEntry"]]]:
    """Trashcan Entries

     Get entries from trash can

    Args:
        deleter (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['TrashCanEntry']]]
    """

    kwargs = _get_kwargs(
        deleter=deleter,
        start_date=start_date,
        end_date=end_date,
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
    deleter: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[Any, HTTPValidationError, List["TrashCanEntry"]]]:
    """Trashcan Entries

     Get entries from trash can

    Args:
        deleter (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['TrashCanEntry']]
    """

    return sync_detailed(
        client=client,
        deleter=deleter,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by,
        desc=desc,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    deleter: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Response[Union[Any, HTTPValidationError, List["TrashCanEntry"]]]:
    """Trashcan Entries

     Get entries from trash can

    Args:
        deleter (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError, List['TrashCanEntry']]]
    """

    kwargs = _get_kwargs(
        deleter=deleter,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by,
        desc=desc,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    deleter: Union[Unset, str] = UNSET,
    start_date: Union[None, Unset, datetime.date] = UNSET,
    end_date: Union[None, Unset, datetime.date] = UNSET,
    order_by: Union[None, Unset, str] = UNSET,
    desc: Union[Unset, bool] = True,
    limit: Union[Unset, int] = 1000,
) -> Optional[Union[Any, HTTPValidationError, List["TrashCanEntry"]]]:
    """Trashcan Entries

     Get entries from trash can

    Args:
        deleter (Union[Unset, str]):
        start_date (Union[None, Unset, datetime.date]):
        end_date (Union[None, Unset, datetime.date]):
        order_by (Union[None, Unset, str]):
        desc (Union[Unset, bool]):  Default: True.
        limit (Union[Unset, int]):  Default: 1000.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError, List['TrashCanEntry']]
    """

    return (
        await asyncio_detailed(
            client=client,
            deleter=deleter,
            start_date=start_date,
            end_date=end_date,
            order_by=order_by,
            desc=desc,
            limit=limit,
        )
    ).parsed
