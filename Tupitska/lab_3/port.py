"""Holds details about port objects"""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import haversine as hs
from containers import Container
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from ship import Ship


@dataclass(kw_only=True)
class IPort(ABC):

    @abstractmethod
    def incoming_ship(self, ship: Ship) -> bool:
        pass

    @abstractmethod
    def outgoing_ship(self, ship: Ship) -> bool:
        pass


@dataclass(kw_only=True)
class Port(IPort):
    """Implements port logic"""

    port_id: int
    latitude: float
    longitude: float
    containers: List[Container] = field(default_factory=list)
    ship_history: List[Ship] = field(default_factory=list)
    current_ships: List[Ship] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "port_id": self.port_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "containers": [container.to_dict() for container in self.containers],
            "ship_history": [ship.to_dict() for ship in self.ship_history],
            "current_ships": [ship.to_dict() for ship in self.current_ships]
        }

    def get_distance(self, port) -> float:
        dist = hs.haversine((self.latitude, self.longitude), (port.latitude, port.longitude))
        return dist

    def incoming_ship(self, ship: Ship) -> bool:
        if isinstance(ship, Ship) and ship not in self.current_ships:
            self.current_ships.append(ship)
            return True
        return False

    def outgoing_ship(self, ship: Ship) -> bool:
        if isinstance(ship, Ship) and ship in self.current_ships:
            self.ship_history.append(ship)
            self.current_ships.remove(ship)
            return True
        return False
