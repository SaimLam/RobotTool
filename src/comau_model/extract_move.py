from comau_model.move import ComauMove, Move_type, Pos_type, WeldSpot


def extract_move(
    code_lines: list[str], is_via_point: bool = False
) -> ComauMove | WeldSpot:
    if not code_lines:
        raise ValueError("code_lines cannot be empty")

    this_move: WeldSpot | ComauMove = (
        WeldSpot() if _is_weld_spot(code_lines) else ComauMove()
    )

    first_cod_line: str = code_lines[0].strip()
    this_move.name = _extract_name(first_cod_line, is_via_point)
    this_move.fly = _check_movefly(first_cod_line)

    if this_move.name == "$HOME":
        this_move.move_type = Move_type.JOINT
        this_move.pos_type = Pos_type.jnt
        return this_move

    this_move.move_type = _extract_move_type(first_cod_line)
    this_move.condition = _extract_condition(code_lines)
    return this_move


def extract_move_variable(this_move: ComauMove, variable_lines: list[str]) -> ComauMove:
    if len(variable_lines) > 1:
        this_move.pos_type = _extract_position_type(variable_lines[0].split()[1])
        this_move.coordinates = _extract_move_coordinates(variable_lines[1].strip())
        if len(variable_lines) > 2:
            this_move.cnfg = variable_lines[2].strip()
    return this_move


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


def _check_movefly(first_cod_line: str) -> bool:
    return first_cod_line.startswith("MOVEFLY")


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


def _extract_move_coordinates(position_var_line: str) -> dict[str, float]:
    position_vars: list[str] = position_var_line.split()
    return {
        position_vars[i].strip(":"): float(position_vars[i + 1])
        for i in range(0, len(position_vars), 2)
    }
