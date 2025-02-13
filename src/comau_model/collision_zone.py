from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    ENGAGE = "engage_zone"
    RELEASE = "release_zone"


@dataclass
class CollisionZone:
    nr: int
    robot_name: str
    action: ActionType

    def __repr__(self) -> str:
        return f"{self.action.value}({self.nr}, '{self.robot_name}')"
