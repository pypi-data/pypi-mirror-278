import pytest
from treefast.node import Node
from treefast.edge import Edge
from treefast.graph import Graph

def test_graph_add_remove_node():
    graph = Graph()
    node = Node(1, "data")
    graph.addNode(node)
    assert node in graph.nodes
    graph.removeNode(node)
    assert node not in graph.nodes


def test_graph_add_remove_edge():
    graph = Graph()
    start = Node(1, "start")
    end = Node(2, "end")
    edge = Edge(start, end)
    graph.addNode(start)
    graph.addNode(end)
    graph.addEdge(edge)
    assert edge in graph.edges
    graph.removeEdge(edge)
    assert edge not in graph.edges
