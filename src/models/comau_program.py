from dataclasses import dataclass, field
from src.models.comau_cod import (
    cod_body,
    cod_declarations,
    cod_header,
    constants,
    extract_moves_from_cod,
    get_name,
    routines,
    var_lines,
)
from src.models.comau_move import WeldSpot
from src.models.comau_var import extract_single_var_lines


@dataclass(slots=True)
class ComauProgram:
    cod: str
    var: str = ""
    declarations: list = field(default_factory=list, init=False)
    body: str = field(init=False)
    header: str = field(init=False)
    name: str = field(init=False)
    constants: list = field(default_factory=list, init=False)
    routines: list = field(default_factory=list, init=False)
    var_lines_in_cod: list = field(default_factory=list, init=False)
    movements_list: list = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.declarations = cod_declarations(self.cod)
        self.body = cod_body(self.cod)
        self.header = cod_header(self.declarations)
        self.name = get_name(self.header)
        self.constants = constants(self.declarations)
        self.routines = routines(self.declarations, self.body)
        self.var_lines_in_cod = var_lines(self.declarations, self.body)
        self.movements_list = (
            self.movements()
        )  # Call the movements method and store the result

    def movements(self) -> list:
        movements = extract_moves_from_cod(self.body)
        if movements:  # Use the stored result
            for movement in movements:
                movement_var_lines = extract_single_var_lines(movement.name, self.var)
                if movement_var_lines:
                    movement.extract_var(movement_var_lines)
        return movements

    def weld_spots(self) -> list:
        weld_spots = [
            move for move in self.movements_list if isinstance(move, WeldSpot)
        ]  # Use the stored result
        return weld_spots
