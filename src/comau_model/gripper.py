from dataclasses import dataclass
from enum import Enum
from typing import List


class SequenceState(Enum):
    OPEN = "open"
    CLOSE = "close"


class VacuumState(Enum):
    VAC_ON = "vac_on"
    VAC_OFF = "vac_off"
    VAC_BLOW = "vac_blow"


@dataclass(slots=True)
class Sequence:
    nr: int
    state: SequenceState
    check_state: bool
    open_inputs: List[int]
    close_inputs: List[int]
    open_outputs: List[int]
    close_outputs: List[int]


@dataclass(slots=True)
class Vacuum:
    nr: int
    state: VacuumState
    check_state: bool
    vac_on_inputs: List[int]
    vac_on_outputs: List[int]
    vac_off_outputs: List[int]
    vac_blow_outputs: List[int]


@dataclass(slots=True)
class PartPresent:
    nr: int
    check_state: bool
    inputs: List[int]


@dataclass(slots=True)
class Gripper:
    nr: int
    air_inputs: List[int]
    sequences: List[Sequence]
    vacuums: List[Vacuum]
    part_present: List[PartPresent]
    air_supervision: tuple[int, bool]
    part_supervision: tuple[int, bool]
