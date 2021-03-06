from guillotina.component import get_utility
from guillotina.exceptions import ConflictError
from guillotina.factory.app import close_utilities
from guillotina.test_package import ITestAsyncUtility
from guillotina.traversal import TraversalRouter
from unittest import mock

import asyncio


def test_make_app(dummy_guillotina):
    assert dummy_guillotina is not None
    assert type(dummy_guillotina.router) == TraversalRouter


async def test_trns_retries_with_app(dummy_guillotina, dummy_request):
    with mock.patch('aiohttp.web.Application._handle') as handle_mock:  # noqa
        f = asyncio.Future()
        f.set_result(None)
        handle_mock.return_value = f
        handle_mock.side_effect = ConflictError()
        resp = await dummy_guillotina._handle(dummy_request)
        assert resp.status_code == 409


async def test_async_util_started_and_stopped(dummy_guillotina):
    util = get_utility(ITestAsyncUtility)
    assert util.state == 'initialize'
    await close_utilities(dummy_guillotina)
    assert util.state == 'finalize'
