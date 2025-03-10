from typing import List, Union

from comau_model.move import ComauMove, Move_type, Pos_type
from comau_model.weld_spot import WeldSpot


def extract_movements(
    movement_lines: dict[int, list[str]], var_file: str = ""
) -> List[ComauMove]:
    movements: List[Union[ComauMove, WeldSpot]] = []
    if movement_lines:
        for index, move_lines in movement_lines.items():
            move_name: str = _extract_name(move_lines[0], False)
            if move_name == "$HOME":
                new_move = ComauMove(
                    index,
                    "$HOME",
                    False,
                    Move_type.JOINT,
                    Pos_type.jnt,
                    [],
                    {},
                    "",
                )

            else:
                movement_var_lines: List[str] = _extract_var_lines(move_name, var_file)
                new_move: Union[ComauMove, WeldSpot] = get_move(
                    index, move_name, move_lines, movement_var_lines
                )

                if new_move.move_type == Move_type.CIRCULAR:
                    via_point_name: str = _extract_name(move_lines[0], True)
                    new_move.via_point = via_point_name

                    via_point_var_lines: List[str] = _extract_var_lines(
                        via_point_name, var_file
                    )
                    via_point: ComauMove = get_move(
                        index, via_point_name, move_lines, via_point_var_lines
                    )
                    movements.append(via_point)

            movements.append(new_move)
    return movements


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
    index: int, name: str, code_lines: List[str], var_lines: List[str]
) -> Union[ComauMove, WeldSpot]:
    """Parses code lines and variable lines to create a ComauMove or WeldSpot object."""
    first_cod_line: str = code_lines[0].strip()
    fly: bool = first_cod_line.startswith("MOVEFLY")
    move_type: Move_type = _extract_move_type(first_cod_line)
    condition: List[str] = _extract_condition(code_lines)
    position_type: Pos_type = Pos_type.jnt

    coordinates: dict[str, float] = {}
    cnfg: str = ""
    if var_lines:
        coordinates = _extract_coordinates(var_lines[1])
        cnfg = _extract_cnfg(var_lines)
        position_type: Pos_type = _extract_position_type(
            var_lines[0].split()[1].strip()
        )

    if _is_weld_spot(condition):
        return WeldSpot(
            index, name, False, move_type, position_type, condition, coordinates, cnfg
        )
    return ComauMove(
        index, name, fly, move_type, position_type, condition, coordinates, cnfg
    )


def _extract_cnfg(var_lines: List[str]) -> str:
    """Extracts CNFG value from variable lines."""
    return (
        var_lines[2].strip()
        if len(var_lines) > 2 and var_lines[2].strip().startswith("CNFG")
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
