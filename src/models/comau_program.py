from dataclasses import dataclass, field
from src.models.comau_cod import (
    extract_cod_body,
    extract_cod_declarations,
    extract_cod_header,
    extract_constants,
    extract_moves_from_cod,
    extract_name,
    extract_routines,
    extract_var_declarations,
    get_weld_spots,
)
from src.models.comau_var import extract_move_var_lines


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
    var_declaration: list = field(default_factory=list, init=False)
    move_list: list = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.declarations = extract_cod_declarations(self.cod)
        self.body = extract_cod_body(self.cod)
        self.header = extract_cod_header(self.declarations)
        self.name = extract_name(self.header)
        self.constants = extract_constants(self.declarations)
        self.routines = extract_routines(self.declarations, self.body)
        self.var_declaration = extract_var_declarations(self.declarations, self.body)
        self.move_list = (
            self._extract_movements()
        )  # Call the movements method and store the result

    def _extract_movements(self) -> list:
        movements = extract_moves_from_cod(self.body)
        if movements:  # Use the stored result
            for movement in movements:
                movement_var_lines = extract_move_var_lines(movement.name, self.var)
                if movement_var_lines:
                    movement.extract_var(movement_var_lines)
        return movements

    def weld_spots(self) -> list:
        return get_weld_spots(self.move_list)
