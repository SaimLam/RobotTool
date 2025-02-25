from dataclasses import dataclass

from comau_model.move import ComauMove
from comau_model.var_const_rout import CodConstant, CodRoutine, CodVariable
from comau_model.weld_spot import WeldSpot


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

    def constants_string(self) -> str:
        return "CONST \n " + "\n ".join(
            [str(constant) for constant in self.cod_constants]
        )

    def routines_string(self) -> str:
        return "\n".join([str(routine) for routine in self.cod_routines])

    def variables_string(self) -> str:
        return "VAR \n " + "\n ".join(
            [str(variable) for variable in self.cod_variables]
        )
