from treefast.abc_module import IEdge, INode
from treefast.node import Node
from typing import Dict


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