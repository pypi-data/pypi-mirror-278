from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict, Type, TypeVar
import json

T = TypeVar('T', bound='Serializable')


class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> Dict:
        pass

    @abstractmethod
    def deserialize(cls: Type[T], data: Dict) -> T:
        pass


class INode(Serializable, ABC):
    @abstractmethod
    def getId(self) -> int:
        pass

    @abstractmethod
    def getData(self) -> Any:
        pass


class IEdge(Serializable, ABC):
    @abstractmethod
    def getStart(self) -> INode:
        pass

    @abstractmethod
    def getEnd(self) -> INode:
        pass

    @abstractmethod
    def getWeight(self) -> float:
        pass


class IGraph(Serializable, ABC):
    @abstractmethod
    def addNode(self, node: INode) -> None:
        pass

    @abstractmethod
    def removeNode(self, node: INode) -> None:
        pass

    @abstractmethod
    def addEdge(self, edge: IEdge) -> None:
        pass

    @abstractmethod
    def removeEdge(self, edge: IEdge) -> None:
        pass

    @abstractmethod
    def findShortestPath(self, start: INode, end: INode) -> List[IEdge]:
        pass

    @abstractmethod
    def depthFirstSearch(self, start: INode) -> List[INode]:
        pass

    @abstractmethod
    def breadthFirstSearch(self, start: INode) -> List[INode]:
        pass


class ITree(IGraph):
    @abstractmethod
    def getRoot(self) -> Optional[INode]:
        pass

    @abstractmethod
    def addChild(self, parent: INode, child: INode) -> None:
        pass

    @abstractmethod
    def removeChild(self, child: INode) -> None:
        pass

    @abstractmethod
    def findNode(self, id: int) -> Optional[INode]:
        pass

    @abstractmethod
    def traverseDepthFirst(self) -> List[INode]:
        pass

    @abstractmethod
    def traverseBreadthFirst(self) -> List[INode]:
        pass


class Node(INode):
    def __init__(self, id: int, data: Any):
        self.id = id
        self.data = data
        self.parent = None
        self.children = []

    def getId(self) -> int:
        return self.id

    def getData(self) -> Any:
        return self.data

    def addChild(self, node: 'Node') -> None:
        self.children.append(node)
        node.parent = self

    def removeChild(self, node: 'Node') -> None:
        self.children.remove(node)
        node.parent = None

    def serialize(self) -> Dict:
        return {
            'id': self.id,
            'data': self.data,
            'children': [child.serialize() for child in self.children]
        }

    @classmethod
    def deserialize(cls, data: Dict) -> 'Node':
        node = cls(data['id'], data['data'])
        node.children = [cls.deserialize(child_data) for child_data in data['children']]
        for child in node.children:
            child.parent = node
        return node


class Edge(IEdge):
    def __init__(self, start: Node, end: Node, weight: float = 1.0):
        self.start = start
        self.end = end
        self.weight = weight

    def getStart(self) -> INode:
        return self.start

    def getEnd(self) -> INode:
        return self.end

    def getWeight(self) -> float:
        return self.weight

    def serialize(self) -> Dict:
        return {
            'start': self.start.getId(),
            'end': self.end.getId(),
            'weight': self.weight
        }

    @classmethod
    def deserialize(cls, data: Dict, nodes: Dict[int, Node]) -> 'Edge':
        start = nodes[data['start']]
        end = nodes[data['end']]
        return cls(start, end, data['weight'])


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


class BinaryTree(Tree):
    def __init__(self):
        super().__init__()
        self.root = None

    # Custom methods and attributes for binary tree can be added here


if __name__ == "__main__":
    bt = BinaryTree()

    root = Node(1, "root")
    child1 = Node(2, "child1")
    child1_1 = Node(3, "child1_1")
    child1_2 = Node(4, "child1_2")
    child2 = Node(5, "child2")
    child2_1 = Node(6, "child2_1")
    child2_2 = Node(7, "child2_2")

    bt.addNode(root)
    bt.addChild(root, child1)
    bt.addChild(root, child2)
    bt.addChild(child1, child1_1)
    bt.addChild(child1, child1_2)
    bt.addChild(child2, child2_1)
    bt.addChild(child2, child2_2)
    print("Tree Visualization:")
    bt.display()

    traversed_nodes_dfs = bt.traverseDepthFirst()
    print("DFS Traversal:", [node.getId() for node in traversed_nodes_dfs])

    traversed_nodes_bfs = bt.traverseBreadthFirst()
    print("BFS Traversal:", [node.getId() for node in traversed_nodes_bfs])

    serialized_tree = bt.serialize()
    print("Serialized Tree:", serialized_tree)

    new_tree = BinaryTree()
    new_tree.deserialize(serialized_tree)

    print("Tree Visualization (new tree):")
    new_tree.display()

    traversed_nodes_dfs_new = new_tree.traverseDepthFirst()
    print("DFS Traversal (new tree):", [node.getId() for node in traversed_nodes_dfs_new])

    traversed_nodes_bfs_new = new_tree.traverseBreadthFirst()
    print("BFS Traversal (new tree):", [node.getId() for node in traversed_nodes_bfs_new])