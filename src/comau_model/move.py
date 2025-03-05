# comau robot move class
from dataclasses import dataclass
from enum import Enum, auto


class Move_type(Enum):
    JOINT = auto()
    LINEAR = auto()
    CIRCULAR = auto()


class Pos_type(Enum):
    jnt = auto()
    pnt = auto()
    xtn = auto()


@dataclass(slots=True)
class ComauMove:
    line_index: int
    name: str
    fly: bool
    move_type: Move_type
    pos_type: Pos_type
    condition: list[str]
    coordinates: dict[str, float]
    cnfg: str
    via_point: str = ""

    # cod presentation
    def __repr__(self) -> str:
        name_str: str = self.name
        move_str: str = "MOVE"
        conditions_str: str = ""

        if self.move_type == Move_type.CIRCULAR:
            name_str = f"{self.name} VIA {self.via_point}"

        if self.fly:
            move_str += "FLY"
            name_str += " ADVANCE"

        if self.condition:
            conditions_str = f", \n    {'\n   '.join(self.condition)} \n  ENDMOVE"

        return f"  {move_str} {self.move_type.name} TO {name_str} {conditions_str}"

    # var presentation
    @property
    def var_string(self) -> str:
        if self.name == "$HOME":
            return ""

        match self.pos_type:
            case Pos_type.jnt:
                return f"{self.name} JNTP Arm: 1 AX: {len(self.coordinates)} Priv \n {self.coordinates_str}"
            case Pos_type.pnt:
                return f"{self.name} POS  Priv \n {self.coordinates_str}\n {self.cnfg}"
            case Pos_type.xtn:
                return f"{self.name} XTND Arm: 1 Ax: {len(self.coordinates) - 6} Priv \n {self.coordinates_str}\n {self.cnfg}"

    # coordinates presentation
    @property
    def coordinates_str(self) -> str:
        if not self.coordinates:
            return f"{self.name} has no position var data"
        return " ".join(f"{key}:{var}" for key, var in self.coordinates.items())

    def rename(self, name_index: int, name_pattern: str = "") -> None:
        if not name_pattern:
            match self.pos_type:
                case Pos_type.jnt:
                    self.name = f"jnt{name_index}J"
                case Pos_type.pnt:
                    self.name = f"pnt{name_index}P"
                case Pos_type.xtn:
                    self.name = f"xtn{name_index}X"
        else:
            self.name = name_pattern.format(name_index)
