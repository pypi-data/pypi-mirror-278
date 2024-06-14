from re import I
from regex import P
from rich import print
import os
import traceback
import uuid
import json
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
from .node import Node, EndNode, WaitingNode, StartNode
from .edge import Edge, SimpleEdge


# beartype_this_package()


T = TypeVar("T", bound=BaseModel)


class Event(BaseModel):
    run_id: str
    context: BaseModel
    name: str
    event_type: Literal[
        "node_execution_error",
        "edge_execution_error",
        "state_enter",
    ]
    message: str | None = None


class Graph:
    """
    A graph represents the workflow of the app. It has a dynamic context that can be changed by the nodes and an optional
    static context that is not changed by the nodes.
    """

    nodes: dict[str, Node]
    edges: dict[str, Edge]
    graph: nx.MultiDiGraph
    current_node: Node
    context: BaseModel
    __initial_context: BaseModel
    __on_state_enter_callbacks: dict[str, Callable[[BaseModel], Awaitable] | None]
    __on_state_exit_callbacks: dict[str, Callable[[BaseModel], Awaitable] | None]
    on_event: Callable[[Event], Awaitable] | None = None
    id: str

    @property
    def stream_token(self):
        return self.__stream_token

    @stream_token.setter
    def stream_token(self, value: Callable[[str], Awaitable]):
        self.__stream_token = value
        for node in self.nodes.values():
            node._set_stream_token(value)

    def compile(self) -> None:
        """
        Check that the graph looks right.
        Using the already built MultiDiGraph object, check the following:
            - node start has exactly one edge going out
            - node end has exactly zero edges going in
            - the end node, if present, has zero edges going out
            - no node has zero edges going in, except for the start node.
            - check that the nodes that each edge points to exist
            - check that the nodes that each edge comes from exist
            - check that all nodes, except for the end node, have at least one edge goin out
        Raises an exception if any of these conditions are not met.
        """
        start_node_out_edges = self.graph.out_edges("start")
        if len(start_node_out_edges) != 1:
            raise ValueError(
                f"'start' node must have exactly one edge going out, found {len(start_node_out_edges)}"
            )
        end_node_out_edges = self.graph.out_edges("end")
        if len(end_node_out_edges) != 0:
            raise ValueError(
                f"'end' node must have zero edges going out, found {len(end_node_out_edges)}"
            )

        for node in self.graph.nodes:
            if node != "start" and self.graph.in_degree(node) == 0:
                raise ValueError(
                    f"Node '{node}' has zero edges going in, which is not allowed except for the start node."
                )

        for edge in self.edges.values():
            target_nodes = edge.out_nodes
            for target_node in target_nodes:
                if target_node not in self.nodes:
                    raise ValueError(
                        f"Edge '{edge.name}' points to non-existent node '{target_node}'"
                    )
            if edge.start_node not in self.nodes:
                raise ValueError(
                    f"Edge '{edge.name}' points to non-existent node '{edge.start_node}'"
                )

        for node in self.nodes.values():
            if node.name != "end" and self.graph.out_degree(node.name) == 0:
                raise ValueError(
                    f"Node '{node.name}' has zero edges going out, which is not allowed except for the end node."
                )

        self.__is_compiled = True

    def reset(
        self, new_state: dict[str, Any] | None = None, id: str | None = None
    ) -> "Graph":
        new_state = new_state or {}
        dump = self.__initial_context.model_copy().model_dump() | new_state
        initial_context = self.__initial_context.__class__(**dump)
        new_graph = Graph(
            context=initial_context,
            name=self.graph.name,
            nodes=self.nodes.copy(),
            edges=self.edges.copy(),
            stream_token=self.__stream_token,
            _is_compiled=self.__is_compiled,
            id=id,
        )
        return new_graph

    __stream_token: Callable[[str], Awaitable]

    def __init__(
        self,
        *,
        context: BaseModel,
        name: str = "graph",
        nodes: dict[str, Node] | None = None,
        edges: dict[str, Edge] | None = None,
        stream_token: Callable[[str], Awaitable] | None = None,
        on_state_enter: (
            dict[str, Callable[[BaseModel], Awaitable] | None] | None
        ) = None,
        on_state_exit: dict[str, Callable[[BaseModel], Awaitable] | None] | None = None,
        _is_compiled: bool = False,
        id: str | None = None,
    ) -> None:
        nodes = nodes if nodes is not None else {}
        edges = edges if edges is not None else {}
        self.nodes = {}
        self.edges = {}
        self.name = name
        self.graph = nx.MultiDiGraph(name=name)
        self.__initial_context = context
        self.context = context.copy()
        self.__is_compiled = _is_compiled
        self.id = id or str(uuid.uuid4())

        async def _stream_token(token: str):
            pass

        self.__stream_token = (
            stream_token if stream_token is not None else _stream_token
        )
        if "start" not in nodes:
            # self.add_node(StartNode())
            self.nodes["start"] = StartNode()

        for node in nodes.values():
            self.add_node(node)

        for edge in edges.values():
            self.add_edge(edge)

        self.current_node = self.nodes["start"]

        self.__on_state_enter_callbacks = (
            on_state_enter if on_state_enter is not None else {}
        )
        self.__on_state_exit_callbacks = (
            on_state_exit if on_state_exit is not None else {}
        )

    def on_state_enter(self, state: str, callback: Callable):
        assert state in self.nodes, f"Node {state} does not exist."
        self.__on_state_enter_callbacks[state] = callback

    def on_state_exit(self, state: str, callback: Callable):
        assert state in self.nodes, f"Node {state} does not exist."
        self.__on_state_exit_callbacks[state] = callback

    def add_node(self, node: Node):
        assert node.name not in self.nodes, f"Node {node.name} already exists"
        self.nodes[node.name] = node
        self.graph.add_node(node.name, color=node.color)
        node._set_stream_token(self.__stream_token)

    def add_edge(self, edge: Edge):
        assert edge.name not in self.edges, f"Edge {edge.name} already exists"
        assert (
            edge.start_node in self.nodes
        ), f"Edge {edge.name} points to non-existent node {edge.start_node}"
        assert all(
            out_node in self.nodes for out_node in edge.out_nodes
        ), f"Edge {edge.name} points to non-existent node(s)"
        self.edges[edge.name] = edge
        for out_node in edge.out_nodes:
            self.graph.add_edge(
                edge.start_node, out_node, label=edge.name, directed=True
            )

    def add_simple_edge(
        self,
        start_node: str | Node,
        out_node: str | Node,
        name: str | None = None,
        label: str | None = None,
    ):
        self.add_edge(SimpleEdge(start_node, out_node, name, label))

    def __log_event(self, event: Event):
        if self.on_event is not None:
            on_event = self.on_event(event)
            asyncio.create_task(on_event)

    async def run(self, input: dict[str, Any] | None = None) -> tuple[BaseModel, bool]:
        assert self.__is_compiled, "Graph must be compiled before running"
        input = input or {}
        self.context = utils.merge_context(self.context, input)
        is_end = False
        while True:
            if self.current_node.name in self.__on_state_exit_callbacks:
                callback = self.__on_state_exit_callbacks[self.current_node.name]
                if callback is not None:
                    await callback(self.context)

            self.current_node = self.get_next_node(self.current_node.name, self.context)
            print(
                f"\n[red bold underline] {self.current_node.name} [/red bold underline]"
            )
            if self.current_node.name in self.__on_state_enter_callbacks:
                callback = self.__on_state_enter_callbacks[self.current_node.name]
                if callback is not None:
                    await callback(self.context)

            if isinstance(self.current_node, EndNode):
                is_end = True
                self.__log_event(
                    Event(
                        context=self.context,
                        event_type="state_enter",
                        name=self.current_node.name,
                        run_id=self.id,
                    )
                )
                break

            if isinstance(self.current_node, WaitingNode):
                self.__log_event(
                    Event(
                        context=self.context,
                        event_type="state_enter",
                        name=self.current_node.name,
                        run_id=self.id,
                    )
                )
                return self.context, False

            try:
                context_update = await self.current_node.run(self.context)
            except Exception as e:
                error_msg: str = str(e)
                traceback_details: str = traceback.format_exc()
                self.__log_event(
                    Event(
                        context=self.context,
                        event_type="node_execution_error",
                        name=self.current_node.name,
                        run_id=self.id,
                        message=f"{error_msg}\nTraceback: {traceback_details}",
                    )
                )
                await asyncio.sleep(1)
                raise e

            self.context = utils.update_context(self.context, context_update)

            self.__log_event(
                Event(
                    context=self.context,
                    event_type="state_enter",
                    name=self.current_node.name,
                    run_id=self.id,
                )
            )

        return self.context, is_end

    def get_next_node(self, current_node_name: str, context: BaseModel) -> Node:
        matching_edges = [
            e for e in self.edges.values() if e.start_node == current_node_name
        ]
        assert len(matching_edges) != 0, f"No edges found for node {current_node_name}"
        assert (
            len(matching_edges) == 1
        ), f"Multiple edges found for node {current_node_name}"
        for edge in matching_edges:
            try:
                next_node_name = edge.fn(context)
            except Exception as e:
                self.__log_event(
                    Event(
                        context=context,
                        event_type="edge_execution_error",
                        name=edge.name,
                        run_id=self.id,
                        message=str(e),
                    )
                )
                raise e
            assert (
                next_node_name in edge.out_nodes
            ), f"Edge {edge.name} does not have a valid out node"
            return self.nodes[next_node_name]

        raise RuntimeError("No next node found")

    def plot(self, destination: str | None = None):
        print("plotting")
        assert self.__is_compiled, "Graph must be compiled before plotting"
        # Start of the Mermaid.js diagram
        mermaid_diagram = f"""
---        
title: {self.name}
---
stateDiagram-v2
"""
        # Unique color tracking for class definition
        color_classes = {}
        class_counter = 1

        # Collect all unique colors and define class styles
        for node in self.nodes.values():
            if hasattr(node, "color") and node.color not in color_classes:
                class_name = f"class{class_counter}"
                color_classes[node.color] = class_name
                mermaid_diagram += (
                    f"    classDef {class_name} fill:{node.color}, stroke:#333\n"
                )
                class_counter += 1

        # Adding all transitions
        for edge in self.edges.values():
            for i, out_node in enumerate(edge.out_nodes):
                transition = (
                    f"    {edge.start_node} --> {out_node} : {edge.labels[i]}\n"
                )
                mermaid_diagram += transition

        # Assigning classes to nodes based on their colors
        for node_name, node in self.nodes.items():
            if hasattr(node, "color"):
                mermaid_diagram += (
                    f"    class {node_name} {color_classes[node.color]}\n"
                )

        def get_img_url(graph) -> str:
            graphbytes = graph.encode("ascii")
            base64_bytes = base64.b64encode(graphbytes)
            base64_string = base64_bytes.decode("ascii")
            return "https://mermaid.ink/img/" + base64_string

        img_url = get_img_url(mermaid_diagram)
        if destination is not None:
            utils.save_mermaid_to_html(
                mermaid_diagram, os.path.join(destination, "graph.html")
            )
        else:
            print("here")
            # get_img_url(mermaid_diagram)
            display(Image(url=img_url))
        #     display(HTML(out_html))
        #     # show_mermaid(mermaid_diagram)
