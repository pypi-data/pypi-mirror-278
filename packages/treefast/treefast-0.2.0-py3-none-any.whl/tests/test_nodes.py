import pytest
from treefast.node import Node

def test_node_getters():
    node = Node(1, "data")
    assert node.getId() == 1
    assert node.getData() == "data"


def test_node_add_remove_child():
    parent = Node(1, "parent")
    child = Node(2, "child")
    parent.addChild(child)
    assert child in parent.children
    parent.removeChild(child)
    assert child not in parent.children


def test_node_serialize():
    node = Node(1, "data")
    child = Node(2, "child")
    node.addChild(child)
    serialized = node.serialize()
    expected = {
        'id': 1,
        'data': 'data',
        'children': [
            {
                'id': 2,
                'data': 'child',
                'children': []
            }
        ]
    }
    assert serialized == expected


def test_node_deserialize():
    data = {
        'id': 1,
        'data': 'data',
        'children': [
            {
                'id': 2,
                'data': 'child',
                'children': []
            }
        ]
    }

    node = Node.deserialize(data)
    assert node.getId() == 1
    assert node.getData() == 'data'
    assert len(node.children) == 1
    assert node.children[0].getId() == 2
    assert node.children[0].getData() == 'child'
