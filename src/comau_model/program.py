from dataclasses import dataclass

from src.comau_model.move import ComauMove
from src.comau_model.var_const_rout import CodConstant, CodRoutine, CodVariable
from src.comau_model.weld_spot import WeldSpot


@dataclass(slots=True)
class ComauProgram:
    name: str
    header: str
    body: str
    cod_constants: list[CodConstant]
    cod_routines: list[CodRoutine]
    cod_variables: list[CodVariable]
    move_list: list[ComauMove]

    @property
    def weld_spots(self) -> list[WeldSpot]:
        return [move for move in self.move_list if isinstance(move, WeldSpot)]

    def _constants_string(self) -> str:
        return "\n".join([str(constant) for constant in self.cod_constants])
