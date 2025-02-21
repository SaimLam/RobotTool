from dataclasses import dataclass
from typing import List


@dataclass
class Routine:
    name: str
    parent_module: str
    parameters: List[str] = []

    def __repr__(self) -> str:
        """
        Return a string representation of the Routine instance.
        """
        if self.parameters:
            parameters_string: str = f"({' '.join(self.parameters)})"
            return f"ROUTINE {self.name} {parameters_string} EXPORTED FROM {self.parent_module}"
        return f"ROUTINE {self.name} EXPORTED FROM {self.parent_module}"
