# extracting the comau program functions
from typing import List, Union

from src.comau_model.extract_cod import (
    extract_cod_body,
    extract_cod_declarations,
    extract_cod_header,
    extract_constants,
    extract_move_var_lines,
    extract_moves_from_cod,
    extract_name,
    extract_routines,
    extract_var_declarations,
)
from src.comau_model.extract_move import extract_move_variable
from src.comau_model.move import ComauMove
from src.comau_model.program import ComauProgram
from src.comau_model.weld_spot import WeldSpot


def extract_program(cod: str, var: str = "") -> ComauProgram:
    this_program = ComauProgram()
    declarations: List[str] = extract_cod_declarations(cod)
    this_program.body = extract_cod_body(cod)
    this_program.header = extract_cod_header(declarations)
    this_program.name = extract_name(this_program.header)
    this_program.constants = extract_constants(declarations)
    this_program.routines = extract_routines(declarations, this_program.body)
    this_program.var_declaration = extract_var_declarations(
        declarations, this_program.body
    )
    this_program.move_list = _extract_movements(this_program.body, var)
    return this_program


def _extract_movements(body: str, var: str = "") -> List[ComauMove]:
    movements: List[Union[ComauMove, WeldSpot]] = extract_moves_from_cod(body)
    if movements:  # Use the stored result
        for movement in movements:
            if movement_var_lines := extract_move_var_lines(movement.name, var):
                extract_move_variable(movement, movement_var_lines)
    return movements
