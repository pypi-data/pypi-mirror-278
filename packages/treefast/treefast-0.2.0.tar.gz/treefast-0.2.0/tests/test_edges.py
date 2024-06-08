import pytest
from treefast.node import Node
from treefast.edge import Edge

def test_edge_getters():
    start = Node(1, "start")
    end = Node(2, "end")
    edge = Edge(start, end, weight=3.5)
    assert edge.getStart() == start
    assert edge.getEnd() == end
    assert edge.getWeight() == 3.5


def test_edge_serialize():
    start = Node(1, "start")
    end = Node(2, "end")
    edge = Edge(start, end, weight=3.5)
    serialized = edge.serialize()
    expected = {
        'start': 1,
        'end': 2,
        'weight': 3.5
    }
    assert serialized == expected


def test_edge_deserialize():
    start = Node(1, "start")
    end = Node(2, "end")
    nodes = {1: start, 2: end}
    data = {
        'start': 1,
        'end': 2,
        'weight': 3.5
    }
    edge = Edge.deserialize(data, nodes)
    assert edge.getStart() == start
    assert edge.getEnd() == end
    assert edge.getWeight() == 3.5
