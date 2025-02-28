from dataclasses import dataclass
from enum import Enum


class InputType(Enum):
    DIGITAL = "DIN"
    ANALOG = "AIN"
    FREQUENCY = "FMI"


class OutputType(Enum):
    DIGITAL = "DOUT"
    ANALOG = "AOUT"
    FREQUENCY = "FMO"


@dataclass(slots=True)
class IO_Com:
    nr: int
    name: str


@dataclass(slots=True)
class Input(IO_Com):
    type: InputType
    state: bool = False
    value: int = 0


@dataclass(slots=True)
class Output(IO_Com):
    type: OutputType
    state: bool = False
    value: int = 0


@dataclass(slots=True)
class Register(IO_Com):
    value: int = 0
