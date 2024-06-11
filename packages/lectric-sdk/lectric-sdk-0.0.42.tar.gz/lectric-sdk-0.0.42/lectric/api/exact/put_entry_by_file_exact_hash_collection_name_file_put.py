from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_put_entry_by_file_exact_hash_collection_name_file_put import (
    BodyPutEntryByFileExactHashCollectionNameFilePut,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    collection_name: str,
    *,
    body: BodyPutEntryByFileExactHashCollectionNameFilePut,
    foreign_key: Union[None, Unset, int, str] = UNSET,
    metadata: Union[None, Unset, str] = UNSET,
    upsert: Union[None, Unset, bool] = False,
    timestamp: Union[None, Unset, str] = UNSET,
    store_raw_data: Union[None, Unset, bool] = True,
    ingestor: Union[None, Unset, str] = UNSET,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    json_foreign_key: Union[None, Unset, int, str]
    if isinstance(foreign_key, Unset):
        json_foreign_key = UNSET
    else:
        json_foreign_key = foreign_key
    params["foreign_key"] = json_foreign_key

    json_metadata: Union[None, Unset, str]
    if isinstance(metadata, Unset):
        json_metadata = UNSET
    else:
        json_metadata = metadata
    params["metadata"] = json_metadata

    json_upsert: Union[None, Unset, bool]
    if isinstance(upsert, Unset):
        json_upsert = UNSET
    else:
        json_upsert = upsert
    params["upsert"] = json_upsert

    json_timestamp: Union[None, Unset, str]
    if isinstance(timestamp, Unset):
        json_timestamp = UNSET
    else:
        json_timestamp = timestamp
    params["timestamp"] = json_timestamp

    json_store_raw_data: Union[None, Unset, bool]
    if isinstance(store_raw_data, Unset):
        json_store_raw_data = UNSET
    else:
        json_store_raw_data = store_raw_data
    params["store_raw_data"] = json_store_raw_data

    json_ingestor: Union[None, Unset, str]
    if isinstance(ingestor, Unset):
        json_ingestor = UNSET
    else:
        json_ingestor = ingestor
    params["ingestor"] = json_ingestor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "put",
        "url": f"/exact/hash/{collection_name}/file",
        "params": params,
    }

    _body = body.to_multipart()

    _kwargs["files"] = _body

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
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyPutEntryByFileExactHashCollectionNameFilePut,
    foreign_key: Union[None, Unset, int, str] = UNSET,
    metadata: Union[None, Unset, str] = UNSET,
    upsert: Union[None, Unset, bool] = False,
    timestamp: Union[None, Unset, str] = UNSET,
    store_raw_data: Union[None, Unset, bool] = True,
    ingestor: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Put Entry By File

    Args:
        collection_name (str):
        foreign_key (Union[None, Unset, int, str]):
        metadata (Union[None, Unset, str]):
        upsert (Union[None, Unset, bool]):  Default: False.
        timestamp (Union[None, Unset, str]):
        store_raw_data (Union[None, Unset, bool]):  Default: True.
        ingestor (Union[None, Unset, str]):
        body (BodyPutEntryByFileExactHashCollectionNameFilePut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        body=body,
        foreign_key=foreign_key,
        metadata=metadata,
        upsert=upsert,
        timestamp=timestamp,
        store_raw_data=store_raw_data,
        ingestor=ingestor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyPutEntryByFileExactHashCollectionNameFilePut,
    foreign_key: Union[None, Unset, int, str] = UNSET,
    metadata: Union[None, Unset, str] = UNSET,
    upsert: Union[None, Unset, bool] = False,
    timestamp: Union[None, Unset, str] = UNSET,
    store_raw_data: Union[None, Unset, bool] = True,
    ingestor: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Put Entry By File

    Args:
        collection_name (str):
        foreign_key (Union[None, Unset, int, str]):
        metadata (Union[None, Unset, str]):
        upsert (Union[None, Unset, bool]):  Default: False.
        timestamp (Union[None, Unset, str]):
        store_raw_data (Union[None, Unset, bool]):  Default: True.
        ingestor (Union[None, Unset, str]):
        body (BodyPutEntryByFileExactHashCollectionNameFilePut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return sync_detailed(
        collection_name=collection_name,
        client=client,
        body=body,
        foreign_key=foreign_key,
        metadata=metadata,
        upsert=upsert,
        timestamp=timestamp,
        store_raw_data=store_raw_data,
        ingestor=ingestor,
    ).parsed


async def asyncio_detailed(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyPutEntryByFileExactHashCollectionNameFilePut,
    foreign_key: Union[None, Unset, int, str] = UNSET,
    metadata: Union[None, Unset, str] = UNSET,
    upsert: Union[None, Unset, bool] = False,
    timestamp: Union[None, Unset, str] = UNSET,
    store_raw_data: Union[None, Unset, bool] = True,
    ingestor: Union[None, Unset, str] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Put Entry By File

    Args:
        collection_name (str):
        foreign_key (Union[None, Unset, int, str]):
        metadata (Union[None, Unset, str]):
        upsert (Union[None, Unset, bool]):  Default: False.
        timestamp (Union[None, Unset, str]):
        store_raw_data (Union[None, Unset, bool]):  Default: True.
        ingestor (Union[None, Unset, str]):
        body (BodyPutEntryByFileExactHashCollectionNameFilePut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        collection_name=collection_name,
        body=body,
        foreign_key=foreign_key,
        metadata=metadata,
        upsert=upsert,
        timestamp=timestamp,
        store_raw_data=store_raw_data,
        ingestor=ingestor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    collection_name: str,
    *,
    client: AuthenticatedClient,
    body: BodyPutEntryByFileExactHashCollectionNameFilePut,
    foreign_key: Union[None, Unset, int, str] = UNSET,
    metadata: Union[None, Unset, str] = UNSET,
    upsert: Union[None, Unset, bool] = False,
    timestamp: Union[None, Unset, str] = UNSET,
    store_raw_data: Union[None, Unset, bool] = True,
    ingestor: Union[None, Unset, str] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Put Entry By File

    Args:
        collection_name (str):
        foreign_key (Union[None, Unset, int, str]):
        metadata (Union[None, Unset, str]):
        upsert (Union[None, Unset, bool]):  Default: False.
        timestamp (Union[None, Unset, str]):
        store_raw_data (Union[None, Unset, bool]):  Default: True.
        ingestor (Union[None, Unset, str]):
        body (BodyPutEntryByFileExactHashCollectionNameFilePut):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            collection_name=collection_name,
            client=client,
            body=body,
            foreign_key=foreign_key,
            metadata=metadata,
            upsert=upsert,
            timestamp=timestamp,
            store_raw_data=store_raw_data,
            ingestor=ingestor,
        )
    ).parsed
