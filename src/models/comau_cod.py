from typing import List

from src.models.comau_move import ComauMove, Move_type, WeldSpot

# This file contains the functions to parse a Comau code file. The code file is divided into a header, declarations, and body.
# The header contains the program name, the declarations contain the constants, routines, and variables, and the body contains the code instructions.
# The functions in this file extract the header, declarations, constants, routines, and variables from the Comau code file.


def cod_declarations(text: str) -> list:
    declarations = []
    if "BEGIN" in text:
        for line in text.split("BEGIN")[0].split("\n"):
            line = line.strip()
            if line and not line.startswith("--"):
                if "VAR" in line:
                    line = line.replace("VAR", "")
                if "CONST" in line:
                    line = line.replace("CONST", "")
                declarations.append(line)
    return declarations


def cod_header(declarations: list) -> str:
    if declarations:
        for line in declarations:
            if line.startswith("PROGRAM"):
                return line
    return ""


def get_name(header: str) -> str:
    # Returns the name of the program.
    if header:
        return header.split()[1]
    return ""


def cod_body(text: str) -> str:
    if "BEGIN" in text and "END" in text:
        return text.split("BEGIN")[1]
    return ""


def constants(declarations: list) -> list:
    if declarations:
        return [
            line
            for line in declarations
            if "=" in line and not line.startswith("ROUTINE")
        ]
    return []


def routines(declarations: list, body: str) -> list:
    routines = []
    for line in declarations:
        if line.startswith("ROUTINE"):
            if "(" in line and line.split("ROUTINE ")[1].split("(")[0].strip() in body:
                routines.append(line)

            elif line.split("ROUTINE ")[1].split("EXPORTED FROM")[0].strip() in body:
                routines.append(line)
    return routines


def var_lines(declarations: list, body: str) -> list:
    variable_lines = []
    if declarations:
        for line in declarations:
            if ":" in line and not (
                line.startswith("ROUTINE") or line.startswith("PROGRAM")
            ):
                used_vars = extract_used_vars(line, body)
                variable_lines.append(
                    create_var_line(used_vars, line.split(":")[1].strip())
                )
    return variable_lines


def extract_used_vars(variable_line: str, body: str) -> list:
    used_variables = []
    for var in variable_line.split(":")[0].split(","):
        if var.strip() in body:
            used_variables.append(var.strip())
    return used_variables


def create_var_line(variables: list, variable_type: str) -> str:
    var_line = ", ".join(variables)
    return f"{var_line} : {variable_type}"


def extract_moves_from_cod(cod_text: str) -> List[ComauMove | WeldSpot]:
    # Returns a list of ComauMove objects parsed from the cod body.
    lines = cod_text.split("\n")
    movements = []
    _buffer_lines = []

    for _current_line in lines:
        _current_line = _current_line.strip()

        if _current_line.startswith(("MOVE", "MOVEFLY")):
            if _buffer_lines:
                new_movement = comau_move(_buffer_lines)
                movements.append(new_movement)
                if new_movement.move_type == Move_type.CIRCULAR:
                    via_point = comau_move(_buffer_lines, True)
                    movements.append(via_point)
                _buffer_lines = []
            _buffer_lines.append(_current_line)

        if _current_line.startswith(("WITH", "ENDMOVE")):
            _buffer_lines.append(_current_line)

    return movements


def comau_move(buffer_lines: list, via_point: bool = False) -> ComauMove | WeldSpot:
    for line in buffer_lines:
        if line.strip().startswith("WITH CONDITION"):
            if "spot" in line or "weld" in line:
                new_spot_move = WeldSpot
                new_spot_move.extract_cod(buffer_lines, via_point)
                new_spot_move.set_spot_index(new_spot_move, line)
                return new_spot_move

    new_movement = ComauMove()
    new_movement.extract_cod(buffer_lines, via_point)
    return new_movement
