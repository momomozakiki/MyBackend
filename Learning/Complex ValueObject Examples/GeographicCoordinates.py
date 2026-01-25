from dataclasses import dataclass
from typing import Optional

from valueobject import ValueObject

@dataclass(frozen=True)
class GeographicCoordinate(ValueObject):
    latitude: float
    longitude: float
    altitude: Optional[float] = None

    def __post_init__(self):
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        if self.altitude is not None and self.altitude < 0:
            raise ValueError("Altitude cannot be negative")


# Usage
coord = GeographicCoordinate(40.7128, -74.0060, 10.5)
print(repr(coord))  # GeographicCoordinate(latitude=40.7128, longitude=-74.006, altitude=10.5)