import re
from dataclasses import dataclass

from comau_model.move import ComauMove


@dataclass(slots=True)
class WeldSpot(ComauMove):
    @property
    def spot_index(self) -> int:
        if self.condition:
            if condition := self._find_spot_condition():
                return self._index_from_condition(condition)
        return 0

    @spot_index.setter
    def spot_index(self, value: int) -> None:
        if self.condition:
            if condition := self._find_spot_condition():
                condition.replace(str(self.spot_index), str(value))

    def change_index(self, new_index: int) -> None:
        self.spot_index = new_index

    def __repr__(self) -> str:
        return f"  MOVE {self.move_type.name} TO {self.name}, \n    {'\n   '.join(self.condition)} \n  ENDMOVE"

    def is_name_conventional(self) -> bool:
        # weld spot name pattern: WP(_[A-Z 0-9]+)?_\d+
        pattern = r"^WP(_[A-Z0-9]+)?_\d+$"
        return bool(re.match(pattern, self.name.upper()))

    def is_index_conventional(self) -> bool:
        if self.is_name_conventional():
            return str(self.spot_index) in self.name
        return self.spot_index > 1

    def set_conventional_name(self) -> str:
        return self.name if self.is_name_conventional() else f"WP_{self.spot_index}"

    def _find_spot_condition(self) -> str:
        for condition in self.condition:
            if "spot" in condition:
                return condition
        return ""

    def _index_from_condition(self, spot_condition: str) -> int:
        condition_params: str = spot_condition.split("(")[1].split(")")[0].strip()
        if condition_params.isnumeric():
            return int(condition_params.strip())
        return int(self._extract_index_from_params(condition_params))

    def _extract_index_from_params(self, params: str) -> int:
        for param in params.split(","):
            stripped_param: str = param.strip()
            # Check if the param is a number and has more than 1 digit
            if stripped_param.isnumeric() and len(stripped_param) > 1:
                return int(stripped_param)
        return 0
