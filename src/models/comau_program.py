from src.models.comau_cod import (
    cod_declarations,
    cod_header,
    cod_body,
    constants,
    routines,
    var_lines,
    get_movements_cod,
    get_name,
)
from src.models.comau_var import extract_single_var_lines


class ComauProgram:
    def __init__(self, cod_string: str, var_string: str = "") -> None:
        self.cod = cod_string
        self.var = var_string
        self.initialize_cod_components()
        self.movements = []
        if self.var:
            self.get_movements()

    def initialize_cod_components(self) -> None:
        self.declarations = cod_declarations(self.cod)
        self.header = cod_header(self.declarations)
        self.body = cod_body(self.cod)
        self.constants = constants(self.declarations)
        self.routines = routines(self.declarations, self.body)
        self.var_lines_in_cod = var_lines(self.declarations, self.body)
        self.name = get_name(self.header)

    def get_movements(self) -> None:
        if self.body:
            self.movements = get_movements_cod(self.body)
        if self.movements:
            for movement in self.movements:
                var_lines = extract_single_var_lines(movement.name, self.var)
                if var_lines:
                    movement.extract_var(var_lines)
