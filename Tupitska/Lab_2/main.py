import json
from uuid import UUID
from port import Port
from container import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from ship import ConfigShip, Ship

def create_container(container_type, count, weight):
    return [container_type(weight=weight) for _ in range(count)]

with open('input.json', 'r') as file:
    data = json.load(file)

ports = {}
containers = []
ships = {}

for port_data in data:
    port_id = UUID(port_data['port_id'])
    latitude = port_data.get('latitude', 0.0)
    longitude = port_data.get('longitude', 0.0)
    port = Port(port_id, latitude, longitude)
    ports[port_id] = port

    containers.extend(create_container(BasicContainer, port_data['basic'], 500.0))
    containers.extend(create_container(HeavyContainer, port_data['heavy'], 1000.0))
    containers.extend(create_container(RefrigeratedContainer, port_data['refrigerated'], 800.0))
    containers.extend(create_container(LiquidContainer, port_data['liquid'], 700.0))

    for ship_data in port_data['ships']:
        ship_id = UUID(ship_data['ship_id'])
        port_id = UUID(ship_data['port_id'])
        port = ports[port_id]

        ship_config = ConfigShip(**ship_data)
        ship = Ship(port, ship_config)
        ships[ship_id] = ship

for port_data in data:
    for ship_data in port_data['ships']:
        ship_id = UUID(ship_data['ship_id'])
        port_id = UUID(ship_data['port_id'])
        port = ports[port_id]
        ship = ships[ship_id]

        ship.load(containers)
        ship.refuel(40.0)
        next_port_id = UUID(ship_data['ports_deliver'])
        next_port = ports[next_port_id]

        if port.incoming_ship(ship) and ship.sail_to(next_port) and port.outgoing_ship(ship):
            ship.unload(containers)

updated_data = []
for port_id, port in ports.items():
    port_data = {
        'port_id': str(port_id),
        'longitude': port.longitude,
        'latitude': port.latitude,
        'ships': [],
        'basic': port_data['basic'],
        'heavy': port_data['heavy'],
        'refrigerated': port_data['refrigerated'],
        'liquid': port_data['liquid']
    }
    for ship in port.current_ships:
        ship_data = {
            'ship_id': str(ship.id),
            'port_id': str(ship.port.id),
            'ports_deliver': str(next_port_id),
            **ship.configs._asdict()
        }
        port_data['ships'].append(ship_data)

    updated_data.append(port_data)

data = updated_data

with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)
