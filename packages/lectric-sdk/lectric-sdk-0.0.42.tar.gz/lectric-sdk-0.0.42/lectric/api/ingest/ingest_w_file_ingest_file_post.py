from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_ingest_w_file_ingest_file_post import BodyIngestWFileIngestFilePost
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response


def _get_kwargs(
    *,
    body: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    params: Dict[str, Any] = {}

    params["collection_name"] = collection_name

    params["json_input_data"] = json_input_data

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/ingest/file",
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
    *,
    client: AuthenticatedClient,
    body: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        body (BodyIngestWFileIngestFilePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_name=collection_name,
        json_input_data=json_input_data,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        body (BodyIngestWFileIngestFilePost):

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
        json_input_data=json_input_data,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Response[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        body (BodyIngestWFileIngestFilePost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
        collection_name=collection_name,
        json_input_data=json_input_data,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: BodyIngestWFileIngestFilePost,
    collection_name: str,
    json_input_data: str,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Ingest W File

     Ingest one element with a file to be stored into a collection

    Args:
        collection_name (str):
        json_input_data (str):
        body (BodyIngestWFileIngestFilePost):

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
            json_input_data=json_input_data,
        )
    ).parsed
