from __future__ import annotations

import typing as t
from unittest import mock

import pytest
from pytest import MonkeyPatch  # noqa: PT013

from neos_common import error
from neos_common.client.keycloak_client import KeycloakClient

if t.TYPE_CHECKING:  # pragma: no cover
    import httpx

    from neos_common.authorization.base import AccessValidator, SignatureValidator


class CustomWebClient:
    """Wrapper for httpx.AsyncClient to inject required headers for unit tests."""

    def __init__(self: t.Self, web_client: httpx.AsyncClient) -> None:
        self._client = web_client

    def _augment_headers(self: t.Self, kwargs):  # noqa: ANN001, ANN202
        _headers = {"authorization": "bearer token"}
        _headers.update({k.lower(): v for k, v in kwargs.get("headers", {}).items()})
        kwargs["headers"] = _headers
        return kwargs

    async def get(self: t.Self, *args: t.ParamsArgsSpec, **kwargs: t.ParamsKwargsSpec) -> httpx.Response:
        kwargs = self._augment_headers(kwargs)
        return await self._client.get(*args, **kwargs)

    async def put(self: t.Self, *args: t.ParamsArgsSpec, **kwargs: t.ParamsKwargsSpec) -> httpx.Response:
        kwargs = self._augment_headers(kwargs)
        return await self._client.put(*args, **kwargs)

    async def post(self: t.Self, *args: t.ParamsArgsSpec, **kwargs: t.ParamsKwargsSpec) -> httpx.Response:
        kwargs = self._augment_headers(kwargs)
        return await self._client.post(*args, **kwargs)

    async def delete(self: t.Self, *args: t.ParamsArgsSpec, **kwargs: t.ParamsKwargsSpec) -> httpx.Response:
        kwargs = self._augment_headers(kwargs)
        return await self._client.delete(*args, **kwargs)

    async def request(self: t.Self, *args: t.ParamsArgsSpec, **kwargs: t.ParamsKwargsSpec) -> httpx.Response:
        kwargs = self._augment_headers(kwargs)
        return await self._client.request(*args, **kwargs)


class BearerWebClient(CustomWebClient): ...


class GlobalWebClient(CustomWebClient):
    def _augment_headers(self: t.Self, kwargs):  # noqa: ANN001, ANN202
        _headers = {"authorization": "bearer token", "x-account": "root", "x-partition": "ksa"}
        _headers.update({k.lower(): v for k, v in kwargs.get("headers", {}).items()})
        kwargs["headers"] = _headers
        return kwargs


@pytest.fixture()
def _auth_patch_factory(  # noqa: PT005
    monkeypatch: MonkeyPatch,
) -> t.Callable[
    [
        str,
        SignatureValidator | None,
        AccessValidator | None,
        list[str] | None,
    ],
    None,
]:
    """Mock token validation checks.

    Mock the keycloak calls required to validate authorization.
    * if provided mock the AccessValidator.validate method to return required resources.
    * if provided mock the SignatureValidator.validate method to return required resources.
    """

    def factory(
        user: str,
        signature_validator: SignatureValidator | None = None,
        access_validator: AccessValidator | None = None,
        resources: list[str] | None = None,
    ) -> None:
        monkeypatch.setattr(KeycloakClient, "introspect_token", mock.Mock(return_value={"active": True, "sub": user}))

        # Ignore initial arg (user_id/request) dependent on validator being mocked.
        async def validate(self: t.Self, _ignore, actions_, resources_, **kwargs):  # noqa: ANN001, ANN202, ANN003, ARG001
            if resources is None and actions_ != []:
                m = f"The principal <{user}> must have <{actions_[0].value}> action for the resource <{resources_[0].urn}>."  # noqa: E501
                raise error.InsufficientPermissionsError(m)
            return user, resources

        if access_validator:
            monkeypatch.setattr(access_validator, "validate", validate)
        if signature_validator:
            monkeypatch.setattr(signature_validator, "validate", validate)

    return factory
