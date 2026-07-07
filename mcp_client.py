# mcp_client.py
# Bridge between Flask (sync) and MCP server (async).

import asyncio
import json
import os
import sys
import threading
from contextlib import AsyncExitStack
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER_SCRIPT = os.path.join(PROJECT_ROOT, "server.py")
PYTHON_EXECUTABLE = sys.executable


_loop = None
_loop_thread = None
_session = None
_exit_stack = None
_ready = threading.Event()


def _run_loop_forever(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


async def _startup():
    global _session, _exit_stack

    params = StdioServerParameters(
        command=PYTHON_EXECUTABLE,
        args=[SERVER_SCRIPT],
        env=os.environ.copy(),
    )

    _exit_stack = AsyncExitStack()
    read, write = await _exit_stack.enter_async_context(stdio_client(params))
    _session = await _exit_stack.enter_async_context(ClientSession(read, write))
    await _session.initialize()


async def _shutdown():
    global _session, _exit_stack
    if _exit_stack is not None:
        await _exit_stack.aclose()
    _session = None
    _exit_stack = None


def start():
    global _loop, _loop_thread

    if _loop is not None:
        return

    _loop = asyncio.new_event_loop()
    _loop_thread = threading.Thread(target=_run_loop_forever, args=(_loop,), daemon=True)
    _loop_thread.start()

    fut = asyncio.run_coroutine_threadsafe(_startup(), _loop)
    fut.result()
    _ready.set()


def stop():
    global _loop, _loop_thread
    if _loop is None:
        return

    fut = asyncio.run_coroutine_threadsafe(_shutdown(), _loop)
    try:
        fut.result(timeout=10)
    except Exception:
        pass

    _loop.call_soon_threadsafe(_loop.stop)
    if _loop_thread is not None:
        _loop_thread.join(timeout=5)

    _loop = None
    _loop_thread = None
    _ready.clear()


def _extract_tool_output(result):
    parts = []
    for item in getattr(result, "content", []) or []:
        text = getattr(item, "text", None)
        if text is not None:
            parts.append(text)
    raw = "".join(parts).strip()

    if not raw:
        return None

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def call_tool(name, arguments):
    if not _ready.is_set() or _session is None or _loop is None:
        raise RuntimeError("MCP client is not started. Call mcp_client.start() first.")

    async def _do_call():
        return await _session.call_tool(name, arguments=arguments)

    fut = asyncio.run_coroutine_threadsafe(_do_call(), _loop)
    result = fut.result(timeout=120)
    return _extract_tool_output(result)