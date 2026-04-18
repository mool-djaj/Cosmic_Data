from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2026, 4, 17, 12, 0, tzinfo=timezone.utc),
            is_operational=True,
        )

        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        if valid_station.is_operational:
            print("Status: Operational")
        else:
            print("Status: Offline")

    except ValidationError as error:
        print(f"Unexpected error creating valid station: {error}")

    print("========================================")
    print("Expected validation error:")

    try:
        SpaceStation(
            station_id="ISS002",
            name="Alpha Base",
            crew_size=25,
            power_level=90.0,
            oxygen_level=95.0,
            last_maintenance=datetime(2026, 4, 16, 10, 0, tzinfo=timezone.utc),
        )
    except ValidationError as error:
        for item in error.errors():
            print(item["msg"])


if __name__ == "__main__":
    main()
