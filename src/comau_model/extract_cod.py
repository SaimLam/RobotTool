from typing import List

from src.comau_model.extract_move import extract_move
from src.comau_model.move import ComauMove, Move_type
from src.comau_model.weld_spot import WeldSpot

# This file contains the functions to parse a Comau code file. The code file is divided into a header, declarations, and body.
# The header contains the program name, the declarations contain the constants, routines, and variables, and the body contains the code instructions.
# The functions in this file extract the header, declarations, constants, routines, and variables from the Comau code file.


def extract_cod_declarations(text: str) -> list[str]:
    declarations: list[str] = []
    if "BEGIN" in text:
        for line in text.split("BEGIN")[0].split("\n"):
            line: str = line.strip()
            if line and not line.startswith("--"):
                if "VAR" in line:
                    line = line.replace("VAR", "")
                if "CONST" in line:
                    line = line.replace("CONST", "")
                declarations.append(line)
    return declarations


def extract_cod_header(declarations: list[str]) -> str:
    if declarations:
        for line in declarations:
            if line.startswith("PROGRAM"):
                return line
    return ""


def extract_name(header: str) -> str:
    # Returns the name of the program.
    return header.split()[1] if header else ""


def extract_cod_body(text: str) -> str:
    return text.split("BEGIN")[1] if "BEGIN" in text and "END" in text else ""


def extract_constants(declarations: list[str]) -> list[str]:
    if declarations:
        return [
            line
            for line in declarations
            if "=" in line and not line.startswith("ROUTINE")
        ]
    return []


def extract_routines(declarations: list[str], body: str) -> List[str]:
    routines: List[str] = []
    for line in declarations:
        if line.startswith("ROUTINE"):
            if "(" in line and line.split("ROUTINE ")[1].split("(")[0].strip() in body:
                routines.append(line)
            elif line.split("ROUTINE ")[1].split("EXPORTED FROM")[0].strip() in body:
                routines.append(line)
    return routines


def extract_var_declarations(declarations: list[str], body: str) -> list[str]:
    variable_lines: List[str] = []
    if declarations:
        for line in declarations:
            if ":" in line and not (
                line.startswith("ROUTINE") or line.startswith("PROGRAM")
            ):
                used_vars = _extract_used_vars(line, body)
                variable_lines.append(
                    _compose_var_declaration(used_vars, line.split(":")[1].strip())
                )
    return variable_lines


def _extract_used_vars(variable_line: str, body: str) -> list[str]:
    used_variables: List[str] = [
        var.strip()
        for var in variable_line.split(":")[0].split(",")
        if var.strip() in body
    ]
    return used_variables


def _compose_var_declaration(variables: list[str], variable_type: str) -> str:
    var_line = ", ".join(variables)
    return f"{var_line} : {variable_type}"


def extract_moves_from_cod(cod_text: str) -> List[ComauMove]:
    lines: List[str] = cod_text.split("\n")
    movements: List[ComauMove | WeldSpot] = []
    _move_lines_buffer: List[str] = []
    # text iteration
    for _current_line in lines:
        _current_line: str = _current_line.strip()
        # find move line
        if _current_line.startswith(("MOVE", "MOVEFLY")):
            if _move_lines_buffer:
                new_movement: ComauMove = extract_move(_move_lines_buffer)
                assert isinstance(new_movement, ComauMove), (
                    "extract_move did not return a ComauMove object"
                )
                movements.append(new_movement)
                # check if circular in order to get the via point
                if new_movement.move_type == Move_type.CIRCULAR:
                    via_point: ComauMove = extract_move(_move_lines_buffer, True)
                    movements.append(via_point)
                _move_lines_buffer = []
            # insert first line in move buffer
            _move_lines_buffer.append(_current_line)
        # fill the move buffer lines
        if _current_line.startswith(("WITH", "ENDMOVE")):
            _move_lines_buffer.append(_current_line)

    return movements


def extract_move_var_lines(name: str, text: str) -> list[str]:
    var_lines: list[str] = []
    for line in text.split("\n"):
        if line.strip() and not line.startswith("--"):
            stripped_line: str = line.strip()
            split_name: str = stripped_line.split()[0]
            if split_name == name and not var_lines:
                var_lines.append(line)
            elif len(var_lines) == 1 and stripped_line.startswith("X"):
                var_lines.append(line)
            elif len(var_lines) == 2 and stripped_line.startswith("CNFG:"):
                var_lines.append(line)
    return var_lines
