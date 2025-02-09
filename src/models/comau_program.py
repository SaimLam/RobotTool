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
from src.models.comau_move import WeldSpot  # Import WeldSpot class
from src.models.comau_var import extract_single_var_lines


class ComauProgram:
    def __init__(self, cod_string: str, var_string: str = "") -> None:
        self.cod = cod_string
        self.var = var_string
        self.initialize_cod_components()
        self.movements = []
        if self.var:
            self.extract_movements()

    def initialize_cod_components(self) -> None:
        self.declarations = cod_declarations(self.cod)
        self.header = cod_header(self.declarations)
        self.body = cod_body(self.cod)
        self.constants = constants(self.declarations)
        self.routines = routines(self.declarations, self.body)
        self.var_lines_in_cod = var_lines(self.declarations, self.body)
        self.name = get_name(self.header)

    def extract_movements(self) -> None:
        self.movements = extract_moves_from_cod(self.body)
        if self.movements:
            movement_var_lines = None
            for movement in self.movements:
                movement_var_lines = extract_single_var_lines(movement.name, self.var)
                if movement_var_lines:
                    movement.extract_var(movement_var_lines)

    @property
    def weld_spots(self) -> list:
        """
        Returns a list of WeldSpot movements.
        """
        weld_spots = [move for move in self.movements if isinstance(move, WeldSpot)]
        return weld_spots
