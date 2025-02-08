from src.models.comau_move import ComauMove
from typing import List

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


def get_movements_cod(text: str) -> List[ComauMove]:
    # Returns a list of ComauMove objects parsed from the cod body.
    lines = text.split("\n")
    movements = []
    movement_buffer_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith(("MOVE", "MOVEFLY")):
            if movement_buffer_lines:
                new_movement = ComauMove()
                new_movement.extract_cod(movement_buffer_lines)
                movements.append(new_movement)
                movement_buffer_lines = []
            movement_buffer_lines.append(line)
        # TODO: Add support for spot movement types
        if line.startswith(("WITH", "ENDMOVE")):
            movement_buffer_lines.append(line)

    return movements
