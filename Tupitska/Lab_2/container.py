from abc import ABC, abstractmethod
from uuid import uuid4
from typing import Type

class Container(ABC):
    def __init__(self, weight: float) -> None:
        self.id = uuid4()
        self.weight = weight

    @abstractmethod
    def consumption(self) -> float:
        pass

    def __eq__(self, other: 'Container') -> bool:
        return (
            self.id == other.id
            and self.weight == other.weight
            and self.__class__ is other.__class__
        )

class BasicContainer(Container):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        return self.weight * 2.5

class HeavyContainer(Container):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        return self.weight * 3.0

class RefrigeratedContainer(HeavyContainer):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        return self.weight * 5.0

class LiquidContainer(HeavyContainer):
    def __init__(self, weight: float) -> None:
        super().__init__(weight=weight)

    def consumption(self) -> float:
        return self.weight * 4.0
