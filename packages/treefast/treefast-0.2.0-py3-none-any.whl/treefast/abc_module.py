from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeVar

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