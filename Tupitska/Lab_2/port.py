from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import haversine as hs
from ship import Ship

if TYPE_CHECKING:
    from ship import Ship

class IPort(ABC):

    @abstractmethod
    def incoming_ship(self, ship: 'Ship') -> bool:
        pass

    @abstractmethod
    def outgoing_ship(self, ship: 'Ship') -> bool:
        pass

class Port(IPort):
    """Implements port logic"""

    def __init__(self, port_id: str, latitude: float, longitude: float) -> None:
        self.id = port_id
        self.containers = []
        self.ship_history = []
        self.current_ships = []
        self.latitude = latitude
        self.longitude = longitude

    def get_distance(self, other_port: 'Port') -> float:
        dist = hs.haversine((self.latitude, self.longitude), (other_port.latitude, other_port.longitude))
        return dist

    def incoming_ship(self, ship: 'Ship') -> bool:
        if isinstance(ship, Ship) and ship not in self.current_ships:
            self.current_ships.append(ship)
            return True
        return False

    def outgoing_ship(self, ship: 'Ship') -> bool:
        if isinstance(ship, Ship) and ship in self.current_ships:
            self.current_ships.remove(ship)
            self.ship_history.append(ship)
            return True
        return False
