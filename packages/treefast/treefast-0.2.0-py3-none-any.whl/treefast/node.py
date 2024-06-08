from treefast.abc_module import INode
from typing import Any, Dict


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