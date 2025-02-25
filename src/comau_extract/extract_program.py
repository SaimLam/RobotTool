# This file contains the functions to parse a Comau code file. The code file is divided into a header, declarations, and body.
# The header contains the program name, the declarations contain the constants, routines, and variables, and the body contains the code instructions.
# The functions in this file extract the header, declarations, constants, routines, and variables from the Comau code file.
from typing import List

from comau_model.move import ComauMove
from comau_model.var_const_rout import CodConstant, CodRoutine, CodVariable
from src.comau_extract.extract_move import extract_movements
from src.comau_model.program import ComauProgram


def extract_program(cod: str, var: str = "") -> ComauProgram:
    declarations: List[str] = _extract_cod_declarations(cod)
    body: str = _extract_cod_body(cod)
    header: str = _extract_cod_header(declarations)
    name: str = _extract_name(header)

    constant_lines: List[str] = _extract_constants_lines(declarations)
    costants: List[CodConstant] = _extract_constants(constant_lines)

    routine_lines: List[str] = _extract_routine_lines(declarations, body)
    routines: List[CodRoutine] = _extract_routines(routine_lines)

    cod_variables: List[CodVariable] = _extract_cod_variables(declarations, body)

    move_list: List[ComauMove] = extract_movements(body, var)

    return ComauProgram(
        name, header, body, costants, routines, cod_variables, move_list
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


def _extract_constants(constants_lines: List[str]) -> List[CodConstant]:
    constants: List[CodConstant] = []
    for line in constants_lines:
        if "CONST" in line:
            name: str = line.split("=")[0].strip()
            value: int = int(line.split("=")[1].strip())
            constants.append(CodConstant(name, value))
    return constants


def _extract_constants_lines(declarations: List[str]) -> List[str]:
    if declarations:
        return [
            line
            for line in declarations
            if "=" in line and not line.startswith("ROUTINE")
        ]
    return []


def _extract_routines(routine_lines: list[str]) -> List[CodRoutine]:
    routines: List[CodRoutine] = []  # type: ignore
    for line in routine_lines:
        routine_name: str = line.split("ROUTINE ")[1].split("(")[0].strip()
        parent_module: str = line.split("EXPORTED FROM ")[1].strip()
        if "(" in line:
            routine_body: str = line.split("(")[1].split(")")[0]
            params: List[str] = [param.strip() for param in routine_body.split(";")]
        else:
            params: List[str] = []
        routines.append(CodRoutine(routine_name, parent_module, params))
    return routines


def _extract_routine_lines(declarations: List[str], body: str) -> List[str]:
    routines_lines: List[str] = []
    for line in declarations:
        if line.startswith("ROUTINE"):
            if "(" in line and line.split("ROUTINE ")[1].split("(")[0].strip() in body:
                routines_lines.append(line)
            elif line.split("ROUTINE ")[1].split("EXPORTED FROM")[0].strip() in body:
                routines_lines.append(line)
    return routines_lines


def _extract_cod_variables(declarations: List[str], body: str) -> List[CodVariable]:
    cod_variables: List[CodVariable] = []
    if declarations:
        for line in declarations:
            if ":" in line and not (
                line.startswith("ROUTINE") or line.startswith("PROGRAM")
            ):
                used_vars: List[str] = _extract_used_vars(line, body)
                for used_var in used_vars:
                    cod_var: CodVariable = CodVariable(
                        used_var, line.split(":")[1].strip()
                    )
                    cod_variables.append(cod_var)
    return cod_variables


def _extract_used_vars(variable_line: str, body: str) -> List[str]:
    used_variables: List[str] = [
        var.strip()
        for var in variable_line.split(":")[0].split(",")
        if var.strip() in body
    ]
    return used_variables
