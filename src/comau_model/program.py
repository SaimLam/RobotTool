from dataclasses import dataclass

from src.comau_model.move import ComauMove
from src.comau_model.weld_spot import WeldSpot


@dataclass(slots=True)
class ComauProgram:
    name: str
    header: str
    body: str
    constants: list[str]
    routines: list[str]
    var_declaration: list[str]
    move_list: list[ComauMove]

    @property
    def weld_spots(self) -> list[WeldSpot]:
        return [move for move in self.move_list if isinstance(move, WeldSpot)]
