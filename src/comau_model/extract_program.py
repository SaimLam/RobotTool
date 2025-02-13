#

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
from src.comau_model.move import ComauMove, WeldSpot
from src.comau_model.program import ComauProgram


def extract_program(cod: str, var: str = "") -> ComauProgram:
    this_program = ComauProgram()
    declarations = extract_cod_declarations(cod)
    this_program.body = extract_cod_body(cod)
    this_program.header = extract_cod_header(declarations)
    this_program.name = extract_name(this_program.header)
    this_program.constants = extract_constants(declarations)
    this_program.routines = extract_routines(declarations, this_program.body)
    this_program.var_declaration = extract_var_declarations(
        this_program.declarations, this_program.body
    )
    this_program.move_list = _extract_movements(this_program.body, var)
    this_program.weld_spots = _extract_weld_spots(this_program.move_list)


def _extract_movements(body: str, var: str = "") -> list[ComauMove]:
    movements = extract_moves_from_cod(body)
    if movements:  # Use the stored result
        for movement in movements:
            movement_var_lines = extract_move_var_lines(movement.name, var)
            if movement_var_lines:
                movement.extract_var(movement_var_lines)
    return movements


def _extract_weld_spots(move_list: list[ComauMove]) -> list[WeldSpot]:
    if move_list:
        return [move for move in move_list if isinstance(move, WeldSpot)]
