from typing import List, Union

from src.comau_model.move import ComauMove, Move_type, Pos_type
from src.comau_model.weld_spot import WeldSpot


def extract_movements(cod_body: str, var_file: str = "") -> List[ComauMove]:
    movements: List[Union[ComauMove, WeldSpot]] = []
    if _extract_cod_lines(cod_body):
        for move_lines in _extract_cod_lines(cod_body):
            move_name: str = _extract_name(move_lines[0], False)
            if move_name == "$HOME":
                movements.append(
                    ComauMove("$HOME", False, Move_type.JOINT, Pos_type.jnt, [], {}, "")
                )
            movement_var_lines: List[str] = _extract_var_lines(move_name, var_file)
            movements.append(get_move(move_lines, movement_var_lines))
    return movements


def _extract_cod_lines(cod_text: str) -> List[list[str]]:
    lines: List[str] = cod_text.split("\n")
    move_list: List[list[str]] = []
    move_lines: List[str] = []
    for line in lines:
        line: str = line.strip()
        if line.startswith(("MOVE", "MOVEFLY")):
            if move_lines:
                move_list.append(move_lines)
                move_lines = []
            move_lines.append(line)
        elif line.startswith(("WITH", "ENDMOVE")):
            move_lines.append(line)
    return move_list


def _extract_var_lines(move_name: str, var_file: str) -> list[str]:
    """Extract variable lines related to a move from the given text."""
    var_lines: list[str] = []
    if move_name in var_file:
        index: int = var_file.index(move_name)
        found_text: str = var_file[index:]
        lines: List[str] = found_text.split("\n")
        var_lines.extend(lines[:3])

    return var_lines


def get_move(
    code_lines: List[str], var_lines: List[str], is_via_point: bool = False
) -> Union[ComauMove, WeldSpot]:
    """Parses code lines and variable lines to create a ComauMove or WeldSpot object."""

    if not code_lines:
        raise ValueError("code_lines cannot be empty")

    first_cod_line: str = code_lines[0].strip()
    move_name: str = _extract_name(first_cod_line, is_via_point)
    fly: bool = first_cod_line.startswith("MOVEFLY")
    move_type: Move_type = _extract_move_type(first_cod_line)
    condition: List[str] = _extract_condition(code_lines)
    position_type: Pos_type = _extract_position_type(first_cod_line.split()[1])
    coordinates: dict[str, float] = _extract_coordinates(var_lines[1])
    cnfg: str = _extract_cnfg(var_lines)

    if _is_weld_spot(condition):
        return WeldSpot(
            move_name, fly, move_type, position_type, condition, coordinates, cnfg
        )
    else:
        return ComauMove(
            move_name, fly, move_type, position_type, condition, coordinates, cnfg
        )


def _extract_cnfg(var_lines: List[str]) -> str:
    """Extracts CNFG value from variable lines."""
    return (
        var_lines[2].strip()
        if len(var_lines) > 2 and var_lines[2].startswith("CNFG")
        else ""
    )


def _is_weld_spot(condition_lines: list[str]) -> bool:
    for line in condition_lines:
        stripped_line: str = line.strip()
        if stripped_line.startswith("WITH CONDITION") and (
            "spot" in stripped_line or "weld" in stripped_line
        ):
            return True
    return False


def _extract_condition(code_lines: list[str]) -> list[str]:
    condition: list[str] = []
    if code_lines[0].endswith(",") and len(code_lines) > 1:
        condition.extend(
            condition_line.strip()
            for condition_line in code_lines
            if condition_line.strip().startswith("WITH")
        )
    return condition


def _extract_name(first_cod_line: str, is_via_point: bool) -> str:
    if "$HOME" in first_cod_line:
        return "$HOME"
    cod_elements: list[str] = first_cod_line.split()
    name: str = cod_elements[5] if is_via_point else cod_elements[3]
    return name


def _extract_move_type(first_cod_line: str) -> Move_type:
    match first_cod_line.split()[1]:
        case "LINEAR":
            return Move_type.LINEAR
        case "CIRCULAR":
            return Move_type.CIRCULAR
        case _:
            return Move_type.JOINT  # Default return value


def _extract_position_type(position_type_string: str) -> Pos_type:
    match position_type_string:
        case "XTND":
            return Pos_type.xtn
        case "JNTP":
            return Pos_type.jnt
        case _:
            return Pos_type.pnt  # Default return value


def _extract_coordinates(position_var_line: str) -> dict[str, float]:
    position_vars: list[str] = position_var_line.split()
    return {
        position_vars[i].strip(":"): float(position_vars[i + 1])
        for i in range(0, len(position_vars), 2)
    }
