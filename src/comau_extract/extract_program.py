# This file contains the functions to parse a Comau code file. The code file is divided into a header, declarations, and body.
# The header contains the program name, the declarations contain the constants, routines, and variables, and the body contains the code instructions.
# The functions in this file extract the header, declarations, constants, routines, and variables from the Comau code file.
from typing import List

from comau_model.move import ComauMove
from src.comau_extract.extract_move import extract_movements
from src.comau_model.program import ComauProgram


def extract_program(cod: str, var: str = "") -> ComauProgram:
    declarations: List[str] = _extract_cod_declarations(cod)
    body: str = _extract_cod_body(cod)
    header: str = _extract_cod_header(declarations)
    name: str = _extract_name(header)
    constants: List[str] = _extract_constants(declarations)
    routines: List[str] = _extract_routines(declarations, body)
    var_declaration: List[str] = _extract_var_declarations(declarations, body)
    move_list: List[ComauMove] = extract_movements(body, var)

    return ComauProgram(
        name, header, body, constants, routines, var_declaration, move_list
    )


def _extract_cod_declarations(text: str) -> List[str]:
    declarations: List[str] = []
    if "BEGIN" in text:
        for line in text.split("BEGIN")[0].split("\n"):
            line: str = line.strip()
            if line and not line.startswith("--"):
                if "VAR" in line:
                    line = line.replace("VAR", "")
                elif "CONST" in line:
                    line = line.replace("CONST", "")
                declarations.append(line)
    return declarations


def _extract_cod_header(declarations: List[str]) -> str:
    if declarations:
        for line in declarations:
            if line.startswith("PROGRAM"):
                return line
    return ""


def _extract_name(header: str) -> str:
    # Returns the name of the program.
    return header.split()[1] if header else ""


def _extract_cod_body(text: str) -> str:
    return text.split("BEGIN")[1] if "BEGIN" in text and "END" in text else ""


def _extract_constants(declarations: List[str]) -> List[str]:
    if declarations:
        return [
            line
            for line in declarations
            if "=" in line and not line.startswith("ROUTINE")
        ]
    return []


def _extract_routines(declarations: List[str], body: str) -> List[str]:
    routines: List[str] = []
    for line in declarations:
        if line.startswith("ROUTINE"):
            if "(" in line and line.split("ROUTINE ")[1].split("(")[0].strip() in body:
                routines.append(line)
            elif line.split("ROUTINE ")[1].split("EXPORTED FROM")[0].strip() in body:
                routines.append(line)
    return routines


def _extract_var_declarations(declarations: List[str], body: str) -> List[str]:
    variable_lines: List[str] = []
    if declarations:
        for line in declarations:
            if ":" in line and not (
                line.startswith("ROUTINE") or line.startswith("PROGRAM")
            ):
                used_vars: List[str] = _extract_used_vars(line, body)
                variable_lines.append(
                    _compose_var_declaration(used_vars, line.split(":")[1].strip())
                )
    return variable_lines


def _extract_used_vars(variable_line: str, body: str) -> List[str]:
    used_variables: List[str] = [
        var.strip()
        for var in variable_line.split(":")[0].split(",")
        if var.strip() in body
    ]
    return used_variables


def _compose_var_declaration(variables: List[str], variable_type: str) -> str:
    var_line: str = ", ".join(variables)
    return f"{var_line} : {variable_type}"
