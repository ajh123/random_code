from typing import List


class Transport:
    def deliver(self):
        pass


class Truck(Transport):
    def __init__(self, wheels: int):
        self._wheels = wheels

    def deliver(self):
        print("Going on a road")

    def numberOfWheels(self):
        return self._wheels


class Ship(Transport):
    def deliver(self):
        print("Travelling the waves")


class TrasnsportFactory:
    @staticmethod
    def get_instance(name: str, *args, **kwargs) -> Transport | None:
        for subC in Transport.__subclasses__():
            if name == subC.__name__:
                return subC(*args, **kwargs)
        return None

    @staticmethod
    def get_types() -> List[str]:
        res = []
        for subC in Transport.__subclasses__():
            res.append(subC.__name__)
        return res


print("====")

truck: Truck = TrasnsportFactory.get_instance("Truck", 8)
print(truck)
truck.deliver()
print(f"The truck has {truck.numberOfWheels()} wheels")

print("====")

ship: Ship = TrasnsportFactory.get_instance("Ship")
print(ship)
ship.deliver()

print("====")

print(TrasnsportFactory.get_types())

print("====")