from enum import Enum
from datetime import datetime

# Define the size of the vehicle
class VehicleSize(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

# Base Vehicle class
class Vehicle:
    def __init__(self, license_plate, size):
        self.license_plate = license_plate
        self.size = size

# Derived classes for different vehicle types
class Bike(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleSize.SMALL)

class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleSize.MEDIUM)

class Bus(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleSize.LARGE)

# ParkingSpot class
class ParkingSpot:
    def __init__(self, spot_id, size):
        self.spot_id = spot_id
        self.size = size
        self.vehicle = None  # Initially, the spot is empty

    def can_fit_vehicle(self, vehicle):
        return self.vehicle is None and vehicle.size.value <= self.size.value

    def park_vehicle(self, vehicle):
        if self.can_fit_vehicle(vehicle):
            self.vehicle = vehicle
            return True
        return False

    def remove_vehicle(self):
        self.vehicle = None

# ParkingLot class
class ParkingLot:
    def __init__(self):
        self.spots = []  # List of all parking spots
        self.available_spots = {
            VehicleSize.SMALL: [],
            VehicleSize.MEDIUM: [],
            VehicleSize.LARGE: []
        }

    def add_parking_spot(self, spot):
        self.spots.append(spot)
        self.available_spots[spot.size].append(spot)

    def park_vehicle(self, vehicle):
        for size in VehicleSize:
            if vehicle.size == size and self.available_spots[size]:
                for spot in self.available_spots[size]:
                    if spot.park_vehicle(vehicle):
                        self.available_spots[size].remove(spot)
                        print(f"Vehicle with license plate {vehicle.license_plate} parked at spot {spot.spot_id}")
                        return True
        print(f"No available spot for vehicle {vehicle.license_plate}")
        return False

    def remove_vehicle(self, vehicle):
        for spot in self.spots:
            if spot.vehicle == vehicle:
                spot.remove_vehicle()
                self.available_spots[spot.size].append(spot)
                print(f"Vehicle with license plate {vehicle.license_plate} left the spot {spot.spot_id}")
                return True
        print(f"Vehicle {vehicle.license_plate} not found")
        return False

# Parking Ticket class
class ParkingTicket:
    def __init__(self, vehicle, spot):
        self.vehicle = vehicle
        self.spot = spot
        self.issued_at = datetime.now()

    def __str__(self):
        return f"Ticket issued for vehicle {self.vehicle.license_plate} at spot {self.spot.spot_id} on {self.issued_at}"

# MAIN CODE
if __name__ == "__main__":
    # Create a parking lot
    parking_lot = ParkingLot()

    # Add parking spots (3 small, 2 medium, 1 large)
    for i in range(3):
        parking_lot.add_parking_spot(ParkingSpot(i, VehicleSize.SMALL))
    for i in range(3, 5):
        parking_lot.add_parking_spot(ParkingSpot(i, VehicleSize.MEDIUM))
    parking_lot.add_parking_spot(ParkingSpot(5, VehicleSize.LARGE))

    # Park vehicles
    bike = Bike("BIKE123")
    car = Car("CAR456")
    bus = Bus("BUS789")

    parking_lot.park_vehicle(bike)  # Should park in a small spot
    parking_lot.park_vehicle(car)   # Should park in a medium spot
    parking_lot.park_vehicle(bus)   # Should park in a large spot

    # Remove vehicles
    parking_lot.remove_vehicle(bike)  # Bike leaves the parking lot
    parking_lot.remove_vehicle(car)   # Car leaves the parking lot
    parking_lot.remove_vehicle(bus)   # Bus leaves the parking lot
