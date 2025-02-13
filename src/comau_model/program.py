from dataclasses import dataclass, field

from comau_model.move import ComauMove, WeldSpot


@dataclass(slots=True)
class ComauProgram:
    name: str = field(init=False)
    header: str = field(init=False)
    body: str = field(init=False)
    constants: list[str] = field(default_factory=list, init=False)
    routines: list[str] = field(default_factory=list, init=False)
    var_declaration: list[str] = field(default_factory=list, init=False)
    move_list: list[ComauMove] = field(default_factory=list, init=False)

    @property
    def weld_spots(self) -> list[WeldSpot]:
        return [move for move in self.move_list if isinstance(move, WeldSpot)]
