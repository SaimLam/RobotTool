from typing import List

from comau_model.var_const_rout import CodRoutine


def get_cod_routines(declarations: list[str], cod_body: str) -> List[CodRoutine]:
    routine_lines: List[str] = _extract_routine_lines(declarations, cod_body)
    return _extract_routines(routine_lines)


def _extract_routine_lines(declarations: List[str], body: str) -> List[str]:
    routines_lines: List[str] = [
        line
        for line in declarations
        if line.startswith("ROUTINE") and _extract_routine_name(line) in body
    ]
    return routines_lines


def _extract_routines(routine_lines: list[str]) -> List[CodRoutine]:
    cod_routines: List[CodRoutine] = []
    for line in routine_lines:
        routine_name: str = _extract_routine_name(line)
        parent_module: str = _extract_parent_module(line)
        params: List[str] = _extract_routine_params(line)
        cod_routines.append(CodRoutine(routine_name, parent_module, params))
    return cod_routines


def _extract_routine_name(line: str) -> str:
    if "(" in line:
        return line.split("ROUTINE ")[1].split("(")[0].strip()
    return line.split("ROUTINE ")[1].split("EXPORTED FROM")[0].strip()


def _extract_parent_module(line: str) -> str:
    return line.split("EXPORTED FROM ")[1].strip()


def _extract_routine_params(line: str) -> List[str]:
    if "(" not in line:
        return []
    routine_body: str = line.split("(")[1].split(")")[0]
    return [param.strip() for param in routine_body.split(";")]
