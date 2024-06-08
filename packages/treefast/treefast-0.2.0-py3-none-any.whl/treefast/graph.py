from treefast.abc_module import IGraph, ITree, INode, IEdge
from treefast.node import Node
from treefast.edge import Edge
from typing import List, Optional, Dict, Any
import json


class Graph(IGraph):
    def __init__(self):
        self.nodes = []
        self.edges = []

    def addNode(self, node: INode) -> None:
        self.nodes.append(node)

    def removeNode(self, node: INode) -> None:
        self.nodes.remove(node)

    def addEdge(self, edge: IEdge) -> None:
        self.edges.append(edge)

    def removeEdge(self, edge: IEdge) -> None:
        self.edges.remove(edge)

    def findShortestPath(self, start: INode, end: INode) -> List[IEdge]:
        # Placeholder for shortest path algorithm (e.g., Dijkstra's)
        pass

    def depthFirstSearch(self, start: INode) -> List[INode]:
        if start is None:
            return []

        visited = []
        stack = [start]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                # Add each child node to stack
                for child in node.children:
                    stack.append(child)

        return visited

    def breadthFirstSearch(self, start: INode) -> List[INode]:
        if start is None:
            return []

        visited = []
        queue = [start]

        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                # Add each child node to queue
                for child in node.children:
                    queue.append(child)

        return visited

    def serialize(self) -> str:
        graph_data = {
            'nodes': [node.serialize() for node in self.nodes],
            'edges': [edge.serialize() for edge in self.edges]
        }
        return json.dumps(graph_data)

    def deserialize(self, data: str) -> None:
        graph_data = json.loads(data)
        node_dict = {}

        for node_data in graph_data['nodes']:
            node = Node.deserialize(node_data)
            self.addNode(node)
            node_dict[node.getId()] = node

        for edge_data in graph_data['edges']:
            edge = Edge.deserialize(edge_data, node_dict)
            self.addEdge(edge)


class Tree(Graph, ITree):
    def __init__(self):
        super().__init__()
        self.root = None

    def getRoot(self) -> Optional[INode]:
        return self.root

    def addChild(self, parent: Node, child: Node) -> None:
        parent.addChild(child)
        self.addNode(child)
        if self.root is None:
            self.root = parent

    def removeChild(self, child: Node) -> None:
        if child.parent:
            child.parent.removeChild(child)
            self.removeNode(child)

    def findNode(self, id: int) -> Optional[INode]:
        for node in self.nodes:
            if node.getId() == id:
                return node
        return None

    def traverseDepthFirst(self) -> List[INode]:
        return self.depthFirstSearch(self.getRoot())

    def traverseBreadthFirst(self) -> List[INode]:
        return self.breadthFirstSearch(self.getRoot())

    def serialize(self) -> str:
        tree_data = {
            'root': self.root.serialize() if self.root else None
        }
        return json.dumps(tree_data)

    def deserialize(self, data: str) -> None:
        tree_data = json.loads(data)
        if tree_data['root']:
            self.root = Node.deserialize(tree_data['root'])
            self.nodes = self.depthFirstSearch(self.root)

    def display(self, node: Optional[Node] = None, level: int = 0) -> None:
        if node is None:
            node = self.root
        if node is None:
            return
        print(' ' * (level * 4) + f'- Node({node.getId()}): {node.getData()}')
        for child in node.children:
            self.display(child, level + 1)