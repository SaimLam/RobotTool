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
    coordinates: dict = field(default_factory=dict)
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

    def extract_cod(self, cod_lines: list, via_point: bool = False) -> None:
        if cod_lines:
            first_cod_line = cod_lines[0].strip()
            self._check_home(first_cod_line)
            self._check_movefly(first_cod_line)
            self._check_condition(cod_lines, first_cod_line)
            self._check_name_and_move_type(first_cod_line, via_point)

    def _check_movefly(self, first_cod_line: str) -> None:
        if first_cod_line.startswith("MOVEFLY"):
            self.fly = True

    def _check_condition(self, cod_lines: list, first_cod_line: str) -> None:
        if first_cod_line.endswith(",") and len(cod_lines) > 1:
            self._extract_condition(cod_lines)

    def _check_home(self, first_cod_line: str) -> None:
        if "$HOME" in first_cod_line:
            self.name = "$HOME"
            self.move_type = Move_type.JOINT
            self.pos_type = Pos_type.jnt

    def _check_name_and_move_type(self, first_cod_line: str, via_point: bool) -> None:
        if "$HOME" not in first_cod_line:
            cod_elements = first_cod_line.split()
            self.name = cod_elements[3] if not via_point else cod_elements[5]
            self._extract_move_type(cod_elements[1])

    def _extract_condition(self, condition_cod_lines: list) -> None:
        self.condition = []
        # Check if the condition_cod_lines list is not empty
        if condition_cod_lines:
            for condition_cod_line in condition_cod_lines:
                # Check if the condition_cod_line contains the string "WITH CONDITION"
                if condition_cod_line.strip().startswith("WITH"):
                    self.condition.append(condition_cod_line.strip())

    def _extract_move_type(self, cod_element: str) -> None:
        if cod_element:
            match cod_element:
                case "JOINT":
                    self.move_type = Move_type.JOINT
                case "LINEAR":
                    self.move_type = Move_type.LINEAR
                case "CIRCULAR":
                    self.move_type = Move_type.CIRCULAR

    def extract_var(self, var_lines: list) -> None:
        # Check if the var_lines list is not empty
        if var_lines:
            first_var_line = var_lines[0].strip()
            pos_var_line = var_lines[1].strip()
            # extract move position type
            self.pos_type = self._position_type(first_var_line)
            # extract move coordinates
            self.coordinates = self._move_coordinates(pos_var_line)
            # Check if the var_lines list has more than two lines
            if len(var_lines) > 2:
                self.cnfg = var_lines[2].strip()

    def _position_type(self, position_type_string: str) -> Pos_type:
        # Check the line for the presence of the strings 'XTND', 'JNTP' or 'POS'
        if "XTND" in position_type_string:
            return Pos_type.xtn
        elif "JNTP" in position_type_string:
            return Pos_type.jnt
        else:
            return Pos_type.pnt

    def _move_coordinates(self, position_var_line: str) -> dict:
        # Split the position_var_line into a list
        position_vars = position_var_line.split()
        # Create a dictionary with the position variables
        return {
            position_vars[i].strip(":"): position_vars[i + 1]
            for i in range(0, len(position_vars), 2)
        }


@dataclass(slots=True)
class WeldSpot(ComauMove):
    spot_index: int = 0

    def __repr__(self) -> str:
        return f"  MOVE {self.move_type.name} TO {self.name}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"

    def set_spot_index(self, weld_string: str) -> None:
        index_str = weld_string.split("(")[1]
        if "," in index_str:
            self.spot_index = int(index_str.split(",")[0])
        else:
            self.spot_index = int(index_str.split(")")[0])
