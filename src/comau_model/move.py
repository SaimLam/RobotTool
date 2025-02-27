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
        if self.move_type == Move_type.CIRCULAR:
            return self._circular_string()

        if self.fly:
            return (
                f"  MOVEFLY {self.move_type.name} TO {self.name} ADVANCE, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"
                if self.condition
                else f"  MOVEFLY {self.move_type.name} TO {self.name} ADVANCE"
            )
        else:
            return (
                f"  MOVE {self.move_type.name} TO {self.name}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"
                if self.condition
                else f"  MOVE {self.move_type.name} TO {self.name}"
            )

    def _circular_string(self) -> str:
        if not self.via_point:
            return f" --  MOVE LINEAR TO {self.name}"

        if self.fly:
            return (
                f"  MOVEFLY {self.move_type.name} TO {self.name} VIA {self.via_point} ADVANCE, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"
                if self.condition
                else f"  MOVEFLY {self.move_type.name} TO {self.name} VIA {self.via_point} ADVANCE"
            )
        else:
            return (
                f"  MOVE {self.move_type.name} TO {self.name} VIA {self.via_point}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"
                if self.condition
                else f"  MOVE {self.move_type.name} TO {self.name} VIA {self.via_point}"
            )

    # var presentation
    def var_string(self) -> str:
        coord_str: str = self._coordinates_string()

        match self.pos_type:
            case Pos_type.jnt:
                return f"{self.name} JNTP Arm: 1 AX: {len(self.coordinates)} Priv \n{coord_str}"
            case Pos_type.pnt:
                return f"{self.name} POS  Priv \n{coord_str}\n {self.cnfg}"
            case Pos_type.xtn:
                return f"{self.name} XTND Arm: 1 Ax: {len(self.coordinates) - 6} Priv \n{coord_str}\n {self.cnfg}"

    # coordinates presentation
    def _coordinates_string(self) -> str:
        if not self.coordinates:
            return f"{self.name} has no position var data"
        return " ".join(f"{key}: {var}" for key, var in self.coordinates.items())

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
