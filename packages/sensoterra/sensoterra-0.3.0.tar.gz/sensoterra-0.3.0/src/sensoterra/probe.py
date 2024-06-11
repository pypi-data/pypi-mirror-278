from datetime import datetime
from typing import Any


class Sensor:
    def __init__(self, id: str):
        self.id = id

    def __repr__(self) -> str:
        return self.id

    def __str__(self) -> str:
        parts = [str(self.timestamp), f"{self.value:2.0f} {self.unit:2}"]
        if self.soil is not None:
            parts.append(f"in {self.soil}")
        return " ".join(parts)

    def update(self, reading: dict[str, Any], soil: str | None) -> None:
        self.type = reading["type"]  # Typically MOISTURE or TEMPERATURE
        self.depth = reading["depth"] if "depth" in reading else None
        self.value = reading["value"]
        self.unit = reading["unit"]  # Typically % or °C
        self.timestamp = datetime.fromisoformat(reading["timestamp"])
        self.soil = soil


class Probe:
    serial = "<None>"
    name = "<None>"

    def __find_soil(
        self,
        soils: dict[str, str],
        profile: list[dict[str, Any]],
        reading: dict[str, Any],
    ) -> str | None:
        """Find the soil at depth based on the soil profile

        We can safely assume profile is sorted on depth.
        """
        soil = None
        if reading["type"] == "MOISTURE" and "depth" in reading:
            for layer in profile:
                if layer["depth"] > reading["depth"]:
                    break
                soil = soils.get(layer["soil"])
        return soil

    def update(
        self, soils: dict[str, str], locations: dict[int, str], probe: dict[str, Any]
    ) -> None:
        if self.serial != probe["serial"]:
            self.__sensors: dict[str, Sensor] = {}
            self.timestamp = None
        self.id = probe["id"]
        self.serial = probe["serial"]
        self.name = probe["name"]
        self.sku = probe["sku"]
        self.state = probe["state"]
        self.location_id = probe["state"]
        self.latitude = probe.get("latitude")
        self.longitude = probe.get("longitude")
        if "location_id" in probe:
            self.location = locations.get(probe["location_id"])
        else:
            self.location = None

        if "last_readings" in probe["status"]:
            for reading in probe["status"]["last_readings"]:
                id = probe["serial"] + "-" + reading["type"]
                if "depth" in reading and reading["depth"] > 0:
                    id += "-" + str(reading["depth"])
                soil = self.__find_soil(soils, probe["soil_profile"], reading)
                if id not in self.__sensors:
                    self.__sensors[id] = Sensor(id)
                self.__sensors[id].update(reading, soil)
            self.timestamp = datetime.fromisoformat(probe["status"]["last_update"])

    def sensors(self) -> list[Sensor]:
        """Get the list of sensors of a probe"""
        return list(self.__sensors.values())

    def __str__(self) -> str:
        parts = [f"{self.serial}"]
        if self.name != self.serial:
            parts.append(f"({self.name})")
        if self.location is not None:
            parts.append(f"@ {self.location}")
        return " ".join(parts)

    def __repr__(self) -> str:
        return self.serial
