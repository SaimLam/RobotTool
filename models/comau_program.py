from models.comau_cod import ComauCod
from models.comau_var import ComauVar
from models.comau_move import ComauMove
from typing import List


class ComauProgram:
    def __init__(self, cod_string: str, var_string: str = "") -> None:
        self.cod = ComauCod(cod_string)
        self.var = ComauVar(var_string)
        self.name = self.get_name()
        self.movements = []
        if self.var:
            self.set_movements()

    def set_movements(self, var_text: str = "") -> None:
        # Set the var attribute of the ComauProgram object.
        if var_text:
            self.var = ComauVar(var_text)
        self.movements = self.get_movements_cod()
        self.get_movements_var()

    def get_name(self) -> str:
        # Returns the name of the program.
        if self.cod.header:
            return self.cod.header.split()[1]
        return ""

    def get_movements_cod(self) -> List[ComauMove]:
        # Returns a list of ComauMove objects parsed from the cod body.
        lines = self.cod.body.split("\n")
        movements = []
        movement_buffer_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith(("MOVE", "MOVEFLY")):
                if movement_buffer_lines:
                    new_movement = ComauMove(movement_buffer_lines)
                    movements.append(new_movement)
                    movement_buffer_lines = []
                movement_buffer_lines.append(line)
            # TODO: Add support for spot movement types
            if line.startswith(("WITH", "ENDMOVE")):
                movement_buffer_lines.append(line)

        return movements

    def get_movements_var(self) -> None:
        # Extracts the variables used in each movement in the program.
        if self.movements:
            for move in self.movements:
                move.extract_var(self.var.extract_single_var_lines(move.name))
