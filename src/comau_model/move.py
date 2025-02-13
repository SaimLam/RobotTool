# comau robot move class
from dataclasses import dataclass, field
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
    name: str = ""
    fly: bool = False
    move_type: Move_type = Move_type.JOINT
    pos_type: Pos_type = Pos_type.pnt
    condition: list[str] = field(default_factory=list)
    coordinates: dict[str, float] = field(default_factory=dict)
    cnfg: str = ""

    # cod represantation
    def __repr__(self) -> str:
        if self.fly:
            if self.condition:
                return f"  MOVEFLY {self.move_type.name} TO {self.name} ADVANCE, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"
            return f"  MOVEFLY {self.move_type.name} TO {self.name} ADVANCE"
        else:
            if self.condition:
                return f"  MOVE {self.move_type.name} TO {self.name}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"
            return f"  MOVE {self.move_type.name} TO {self.name}"

    # var represantation
    def var_string(self) -> str:
        coord_str = self.coordinates_string()

        match self.pos_type:
            case Pos_type.jnt:
                return f"{self.name} JNTP Arm: 1 AX: {len(self.coordinates)} Priv \n{coord_str}"
            case Pos_type.pnt:
                return f"{self.name} POS  Priv \n{coord_str}\n {self.cnfg}"
            case Pos_type.xtn:
                return f"{self.name} XTND Arm: 1 Ax: {len(self.coordinates) - 6} Priv \n{coord_str}\n {self.cnfg}"

    # coodinates represantation
    def coordinates_string(self) -> str:
        if not self.coordinates:
            return f"{self.name} POS  has no coordinate data"
        coord_str = ""
        for key, var in self.coordinates.items():
            coord_str += f" {key}: {var}"
        return coord_str

    def rename(self, name_index: int, unconventional: str = "") -> None:
        if not unconventional:
            match self.pos_type:
                case Pos_type.jnt:
                    self.name = f"jnt{name_index}J"
                case Pos_type.pnt:
                    self.name = f"pnt{name_index}P"
                case Pos_type.xtn:
                    self.name = f"xtn{name_index}X"
        else:
            self.name = unconventional


@dataclass(slots=True)
class WeldSpot(ComauMove):
    spot_index: int = 0

    def __repr__(self) -> str:
        return f"  MOVE {self.move_type.name} TO {self.name}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"

    def extract_spot_index(self, weld_string: str) -> None:
        index_str = weld_string.split("(")[1]
        if "," in index_str:
            self.spot_index = int(index_str.split(",")[0])
        else:
            self.spot_index = int(index_str.split(")")[0])
