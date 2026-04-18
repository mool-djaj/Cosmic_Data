from datetime import datetime, timezone
from enum import Enum
from math import ceil
from typing import List, Self
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission_rules(self) -> Self:
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        if not any(
            member.rank in {Rank.COMMANDER, Rank.CAPTAIN}
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        if self.duration_days > 365:
            experienced_members = sum(
                member.years_experience >= 5 for member in self.crew
            )
            if experienced_members < ceil(len(self.crew) / 2):
                raise ValueError(
                    "Long missions require at least 50% experienced crew"
                )

        return self


def display_mission_details(mission: SpaceMission) -> None:
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")

    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
        )


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================")

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2026, 4, 17, 12, 0, tzinfo=timezone.utc),
            duration_days=900,
            crew=[
                CrewMember(
                    member_id="CM001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=42,
                    specialization="Mission Command",
                    years_experience=12,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=35,
                    specialization="Navigation",
                    years_experience=6,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=31,
                    specialization="Engineering",
                    years_experience=4,
                    is_active=True,
                ),
            ],
            mission_status="planned",
            budget_millions=2500.0,
        )

        print("Valid mission created:")
        display_mission_details(valid_mission)
    except ValidationError as error:
        print(f"Unexpected error: {error}")

    print("========================================")
    print("Expected validation error:")

    try:
        SpaceMission(
            mission_id="M2024_TEST",
            mission_name="Survey Mission",
            destination="Europa",
            launch_date=datetime(2026, 4, 18, 8, 0, tzinfo=timezone.utc),
            duration_days=120,
            crew=[
                CrewMember(
                    member_id="CM010",
                    name="Nora Vega",
                    rank=Rank.OFFICER,
                    age=28,
                    specialization="Science",
                    years_experience=4,
                    is_active=True,
                ),
                CrewMember(
                    member_id="CM011",
                    name="Eli Park",
                    rank=Rank.CADET,
                    age=24,
                    specialization="Support",
                    years_experience=1,
                    is_active=True,
                ),
            ],
            budget_millions=80.0,
        )
    except ValidationError as error:
        for item in error.errors():
            message = item["msg"].replace("Value error, ", "")
            print(message)


if __name__ == "__main__":
    main()
