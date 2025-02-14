from dataclasses import dataclass

from comau_model.move import ComauMove


@dataclass(slots=True)
class WeldSpot(ComauMove):
    spot_index: int = 0

    def __repr__(self) -> str:
        return f"  MOVE {self.move_type.name} TO {self.name}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"

    def extract_spot_index(self, weld_string: str) -> None:
        index_str = weld_string.split("(")[1]
        if "," in index_str:
            self.spot_index = int(index_str.split(",")[0])
        else:
            self.spot_index = int(index_str.split(")")[0])
