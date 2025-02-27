# This file contains the functions to parse a Comau code file. The code file is divided into a header, declarations, and body.
# The header contains the program name, the declarations contain the constants, routines, and variables, and the body contains the code instructions.
# The functions in this file extract the header, declarations, constants, routines, and variables from the Comau code file.
from typing import List

from comau_extract.extract_moves import extract_movements
from comau_extract.extract_routines import get_cod_routines
from comau_model.cod_body import CodBody
from comau_model.move import ComauMove
from comau_model.program import ComauProgram
from comau_model.var_const_rout import CodConstant, CodRoutine, CodVariable


def extract_program(cod_text: str, var_text: str = "") -> ComauProgram:
    """Extract the Comau program from the given code text.

    This function parses the provided `cod_text` and optional `var_text`
    to construct a `ComauProgram` object, representing the extracted
    program structure, including header, body, constants, routines,
    variables, and movements.

    Args:
        cod_text (str): The Comau code text to extract the program from.
        var_text (str, optional): Additional variable text. Defaults to "".

    Returns:
        ComauProgram: The extracted Comau program.
    """

    cod_declarations: List[str] = _extract_cod_declarations(cod_text)
    body: CodBody = _extract_cod_body(cod_text)
    header: str = _extract_cod_header(cod_declarations)
    name: str = _extract_name(header)

    constant_lines: List[str] = _extract_constants_lines(cod_declarations)
    cod_constants: List[CodConstant] = _extract_constants(constant_lines)

    routines: List[CodRoutine] = get_cod_routines(cod_declarations, body.text)

    cod_variables: List[CodVariable] = _extract_cod_variables(
        cod_declarations, body.text
    )

    move_list: List[ComauMove] = extract_movements(body.movement_lines, var_text)

    return ComauProgram(
        name, header, body, cod_constants, routines, cod_variables, move_list
    )


def _extract_cod_declarations(cod_text: str) -> List[str]:
    declarations: List[str] = []
    if "BEGIN" in cod_text:
        for line in cod_text.split("BEGIN")[0].split("\n"):
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


def _extract_cod_body(text: str) -> CodBody:
    if "BEGIN" in text and "END" in text:
        return CodBody(text.split("BEGIN")[1])
    return CodBody("")


def _extract_constants(constants_lines: List[str]) -> List[CodConstant]:
    cod_constants: List[CodConstant] = []
    for line in constants_lines:
        name: str = line.split("=")[0].strip()
        value: int = int(line.split("=")[1].strip())
        cod_constants.append(CodConstant(name, value))
    return cod_constants


def _extract_constants_lines(declarations: List[str]) -> List[str]:
    if declarations:
        return [
            line.strip()
            for line in declarations
            if "=" in line and not line.startswith("PROGRAM")
        ]
    return []


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
