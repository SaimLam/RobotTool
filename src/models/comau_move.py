# comau robot move class
from enum import Enum, auto


class Move_type(Enum):
    JOINT = auto()
    LINEAR = auto()
    CIRCULAR = auto()


class Pos_type(Enum):
    jnt = auto()
    pnt = auto()
    xtn = auto()


class ComauMove:
    def __init__(self, cod_lines: list) -> None:
        self.fly = False
        self.conditioned = False
        self.condition = []
        self.move_type = Move_type.JOINT
        self.pos_type = Pos_type.jnt
        self.name = ""
        self.name_index = 0
        self.joint_var = []
        self.pos_var = []
        self.cnfg = ""
        self._extract_cod(cod_lines)

    def __repr__(self) -> str:
        if self.fly:
            if self.conditioned:
                return f"  MOVEFLY {self.move_type.name} TO {self.name} ADVANCE, \n    {',\n   '.join(self.condition)} \n  ENDMOVE"
            return f"  MOVEFLY {self.move_type.name} TO {self.name} ADVANCE"
        else:
            if self.conditioned:
                return f"  MOVE {self.move_type.name} TO {self.name}, \n    {',\n   '.join(self.condition)} \n  ENDMOVE"
            return f"  MOVE {self.move_type.name} TO {self.name}"

    def var_string(self) -> str:
        var_str = ""

        if self.pos_type == Pos_type.jnt:
            for var in self.joint_var:
                var_str += f" {var}"

            return f"{self.name} JNTP Arm: 1 AX: {len(self.joint_var)} Priv \n{var_str}"
        else:
            for var in self.pos_var:
                var_str += f" {var}"

            if self.pos_type == Pos_type.pnt:
                return f"{self.name} POS  Priv \n{var_str}\n {self.cnfg}"
            else:
                return f"{self.name} XTND Arm: 1 Ax: {len(self.pos_var) - 6} Priv \n{var_str}\n {self.cnfg}"

    def rename(self, unconventional: str = "") -> None:
        if not unconventional:
            match self.pos_type:
                case Pos_type.jnt:
                    self.name = f"jnt{self.name_index}J"
                case Pos_type.pnt:
                    self.name = f"pnt{self.name_index}P"
                case Pos_type.xtn:
                    self.name = f"xtn{self.name_index}X"
        else:
            self.name = unconventional

    def _extract_cod(self, cod_lines: list) -> None:
        # Check if the cod_lines list is not empty
        if cod_lines:
            # Extract the first line of the cod_lines list
            first_cod_line = cod_lines[0].strip()
            # Check if the first line of the cod_lines list is a MOVEFLY command
            if first_cod_line.startswith("MOVEFLY"):
                self.fly = True
            # Check if cod_lines list are more than one line and the first line ends with a comma
            if first_cod_line.endswith(",") and len(cod_lines) > 1:
                self._extract_condition(cod_lines)
            # Check if the first line of the cod_lines list contains the string '$HOME'
            if "$HOME" in first_cod_line:
                self.name = "$HOME"
                self.move_type = Move_type.JOINT
                self.pos_type = Pos_type.jnt
            else:
                cod_elements = first_cod_line.split()
                self.name = cod_elements[3]
                self._extract_move_type_from_string(cod_elements[1])

    def _extract_condition(self, condition_cod_lines: list) -> None:
        # Check if the condition_cod_lines list is not empty
        if condition_cod_lines:
            for condition_cod_line in condition_cod_lines:
                # Check if the condition_cod_line contains the string "WITH CONDITION"
                if condition_cod_line.strip().startswith("WITH"):
                    self.conditioned = True
                    self.condition.append(condition_cod_line.strip())

    def _extract_move_type_from_string(self, cod_element: str) -> None:
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
            # Extract the first and second line of the var_lines list
            first_var_line = var_lines[0].strip()
            pos_var_line = var_lines[1].strip()

            # Check the first line for the presence of the strings 'XTND', 'JNTP' or 'POS'
            if "XTND" in first_var_line:
                self.pos_type = Pos_type.xtn
            elif "JNTP" in first_var_line:
                self.pos_type = Pos_type.jnt
            else:
                self.pos_type = Pos_type.pnt

            # Check if the var_lines list is more than two lines
            # The third line contains the position configuration
            if len(var_lines) > 2:
                self.pos_var = pos_var_line.split()
                self.cnfg = var_lines[2].strip()
            else:
                self.joint_var = pos_var_line.split()


class WeldSpot(ComauMove):
    def __init__(self, cod_lines: list) -> None:
        super().__init__(cod_lines)
        self.spot_name = ""
        self.spot_index = 0

    def change_spot_index(self, new_index: int) -> None:
        self.spot_index = new_index
