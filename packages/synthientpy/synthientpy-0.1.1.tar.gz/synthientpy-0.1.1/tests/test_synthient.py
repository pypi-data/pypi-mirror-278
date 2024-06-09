#!/usr/bin/env python
"""Tests for `synthientpy` package."""

import asyncio

# pylint: disable=redefined-outer-name
import os

from dotenv import load_dotenv

import synthientpy as synthient

load_dotenv()


# https://stackoverflow.com/questions/23033939/how-to-test-python-3-4-asyncio-code
def async_test(coro):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro(*args, **kwargs))
        finally:
            loop.close()

    return wrapper


def test_sync_lookup():
    client = synthient.Client(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = client.lookup("4cda81270ec3dc9f1546118dc48d22bc")
    assert response.token == "4cda81270ec3dc9f1546118dc48d22bc"
    assert response.success is True


@async_test
async def test_async_lookup():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    response = await client.lookup("4cda81270ec3dc9f1546118dc48d22bc")

    assert response.token == "4cda81270ec3dc9f1546118dc48d22bc"
    assert response.success is True


def test_sync_404():
    client = synthient.Client(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    try:
        client.lookup("NONEXISTENT_TOKEN")
    except synthient.ErrorResponse as e:
        assert e.message == "Visitor not found"


@async_test
async def test_async_404():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    try:
        await client.lookup("NONEXISTENT_TOKEN")
    except synthient.ErrorResponse as e:
        assert e.message == "Visitor not found"


def test_sync_401():
    client = synthient.Client(
        api_key="INVALID_API_KEY",
    )
    try:
        client.lookup("4cda81270ec3dc9f1546118dc48d22bc")
    except synthient.ErrorResponse as e:
        assert e.message == "Unauthorized"


@async_test
async def test_async_401():
    client = synthient.AsyncClient(
        api_key="INVALID_API_KEY",
    )
    try:
        await client.lookup("4cda81270ec3dc9f1546118dc48d22bc")
    except synthient.ErrorResponse as e:
        assert e.message == "Unauthorized"
