from re import I
from regex import P
from rich import print
import os
from typing import TypedDict, Any, get_type_hints, Annotated, get_origin
import operator
from pydantic import BaseModel
from typing import (
    Awaitable,
    Callable,
    Literal,
    get_args,
    TypeVar,
    Any,
    Annotated,
)
import asyncio
import networkx as nx
from IPython.display import display, HTML, Javascript, Image
import base64
from . import utils


T = TypeVar("T", bound=BaseModel)


class Node(BaseModel):
    """
    A node is a state in the state graph. Basically it's a function that can mutate the state.
    """

    name: str
    color: str = "blue"
    static_context: BaseModel | None = None
    _stream_token: list[Callable[[str], Awaitable]] = []

    class Config:
        frozen = True

    @property
    def stream_token(self):
        assert len(self._stream_token) == 1, "stream_token must be set."
        return self._stream_token[0]

    def _set_stream_token(self, value: Callable[[str], Awaitable]):
        if len(self._stream_token) > 0:
            # replace it
            self._stream_token[0] = value
        else:
            self._stream_token.append(value)

    async def run(self, context: T) -> dict | T:
        return {}

    def __init__(self, static_context: BaseModel | None = None, **kwargs):
        super().__init__(**kwargs, static_context=static_context)
        if static_context is not None:
            # check that it is frozen
            assert not utils.is_mutable(
                static_context.__class__
            ), "Static context must be frozen"


class WaitingNode(Node):
    """
    A node that causes the `run` method to finish. The context however is saved. So the next time the graph is run, the context is restored.
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__(name=name, color="orange", _is_waiting=True)


class StartNode(Node):
    """
    The start node is the first node in the graph. It has no incoming edges.
    """

    def __init__(self) -> None:
        super().__init__(name="start", color="green")


class EndNode(Node):
    """
    The end node is the last node in the graph. It has no outgoing edges.
    This node is optional.
    """

    def __init__(self, name="end") -> None:
        super().__init__(name=name, color="red")


def node(fn: Callable):
    """
    Decorator to turn a function into a node. This works well for relatively simple nodes.
    """

    class _Node(Node):
        def __init__(self, name: str) -> None:
            super().__init__(name=name)

        async def run(self, context: dict) -> dict:
            return await fn(context)

    return _Node(name=fn.__name__)
