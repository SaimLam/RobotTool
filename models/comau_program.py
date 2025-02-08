from models.comau_cod import ComauCod
from models.comau_move import ComauMove
from typing import List


class ComauProgram:
    def __init__(self, cod_string: str) -> None:
        self.cod = ComauCod(cod_string)

    def __repr__(self) -> str:
        # TODO: Implement __repr__ method
        return ""

    @property
    def name(self) -> str:
        # Returns the name of the program.
        if self.cod.header:
            return self.cod.header.split()[1]
        return ""

    @property
    def movements(self) -> List[ComauMove]:
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

            if line.startswith(("WITH", "ENDMOVE")):
                movement_buffer_lines.append(line)

        return movements
