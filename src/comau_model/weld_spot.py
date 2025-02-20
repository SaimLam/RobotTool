import re
from dataclasses import dataclass

from src.comau_model.move import ComauMove


@dataclass(slots=True)
class WeldSpot(ComauMove):
    spot_index: int = 0

    def __post_init__(self) -> None:
        weld_string: str = self._get_spot_condition()
        self.spot_index = self._get_spot_index(weld_string)

    def __repr__(self) -> str:
        return f"  MOVE {self.move_type.name} TO {self.name}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"

    def is_name_conventional(self) -> bool:
        # WP(_[A-Za-z]+)?_\d+
        pattern = r"^WP(_[A-Z0-9]+)?_\d+$"
        return bool(re.match(pattern, self.name.upper()))

    def set_conventional_name(self) -> str:
        if not self.is_name_conventional():
            return f"WP_{self.spot_index}"
        return self.name

    def _get_spot_condition(self) -> str:
        for condition in self.condition:
            if "spot" or "weld" in condition:
                return condition
        return ""

    def _get_spot_index(self, weld_string: str) -> int:
        if "(" in weld_string:
            index_str_buffer = weld_string.split("(")[1]
            if "," in index_str_buffer:
                index_str = index_str_buffer.split(",")[0]
                if index_str.isnumeric():
                    return int(index_str)
            else:
                index_str = index_str_buffer.split(")")[0]
                if index_str.isnumeric():
                    return int(index_str)
        return 0
