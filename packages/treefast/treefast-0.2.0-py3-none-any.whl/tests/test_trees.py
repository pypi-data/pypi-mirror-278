import pytest
from treefast.node import Node
from treefast.graph import Tree

def test_tree_add_child_and_get_root():
    tree = Tree()
    root = Node(1, "root")
    child = Node(2, "child")
    tree.addChild(root, child)
    assert tree.getRoot() == root
    assert child in root.children


def test_tree_remove_child():
    tree = Tree()
    root = Node(1, "root")
    child = Node(2, "child")
    tree.addChild(root, child)
    tree.removeChild(child)
    assert child not in root.children


def test_tree_find_node():
    tree = Tree()
    node1 = Node(1, "node1")
    node2 = Node(2, "node2")
    tree.addNode(node1)
    tree.addNode(node2)
    assert tree.findNode(1) == node1
    assert tree.findNode(2) == node2


def test_tree_traverse_depth_first():
    tree = Tree()
    root = Node(1, "root")
    child1 = Node(2, "child1")
    child2 = Node(3, "child2")
    tree.addChild(root, child1)
    tree.addChild(root, child2)
    dfs_result = tree.traverseDepthFirst()
    assert [node.getId() for node in dfs_result] == [1, 3, 2]


def test_tree_traverse_breadth_first():
    tree = Tree()
    root = Node(1, "root")
    child1 = Node(2, "child1")
    child2 = Node(3, "child2")
    tree.addChild(root, child1)
    tree.addChild(root, child2)
    bfs_result = tree.traverseBreadthFirst()
    assert [node.getId() for node in bfs_result] == [1, 2, 3]


def test_tree_serialize():
    tree = Tree()
    root = Node(1, "root")
    child1 = Node(2, "child1")
    child2 = Node(3, "child2")
    tree.addChild(root, child1)
    tree.addChild(root, child2)
    serialized = tree.serialize()
    expected = '{"root": {"id": 1, "data": "root", "children": [{"id": 2, "data": "child1", "children": []}, {"id": 3, "data": "child2", "children": []}]}}'
    assert serialized == expected


def test_tree_deserialize():
    tree = Tree()
    data = '{"root": {"id": 1, "data": "root", "children": [{"id": 2, "data": "child1", "children": []}, {"id": 3, "data": "child2", "children": []}]}}'
    tree.deserialize(data)
    root = tree.getRoot()
    assert root.getId() == 1
    assert root.getData() == 'root'
    children_ids = [child.getId() for child in root.children]
    assert set(children_ids) == {2, 3}


def test_tree_display(capsys):
    tree = Tree()
    root = Node(1, "root")
    child1 = Node(2, "child1")
    child2 = Node(3, "child2")
    child1_1 = Node(4, "child1_1")
    child2_1 = Node(5, "child2_1")
    tree.addChild(root, child1)
    tree.addChild(root, child2)
    tree.addChild(child1, child1_1)
    tree.addChild(child2, child2_1)
    tree.display()
    captured = capsys.readouterr()
    expected_output = (
        '- Node(1): root\n'
        '    - Node(2): child1\n'
        '        - Node(4): child1_1\n'
        '    - Node(3): child2\n'
        '        - Node(5): child2_1\n'
    )
    assert captured.out == expected_output