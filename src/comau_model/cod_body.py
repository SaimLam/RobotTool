class CodBody:
    def __init__(self, text: str) -> None:
        self.text = text

    @property
    def lines(self) -> list[tuple[int, str]]:
        return [
            (i, line.strip()) for i, line in enumerate(self.text.split("\n")) if line
        ]

    @property
    def movement_lines(self) -> dict[int, list[str]]:
        move_lines: dict[int, list[str]] = {}
        line_index: int = 0
        for line in self.lines:
            line_str: str = line[1].strip()
            if line_str.startswith(("MOVE", "MOVEFLY")):
                line_index = line[0]
                move_lines[line_index] = [line_str]
            elif line_str.startswith(("WITH", "ENDMOVE")):
                move_lines[line_index].append(line_str)
        return move_lines

    @property
    def sys_var_lines(self) -> list[tuple[int, str]]:
        return [line for line in self.lines if line[1].startswith("$")]

    @property
    def io_lines(self) -> list[tuple[int, str]]:
        return [line for line in self.lines if line[1].startswith(("D_send", "D_wait"))]

    @property
    def collision_zone_lines(self) -> list[tuple[int, str]]:
        return [
            line
            for line in self.lines
            if line[1].startswith(("engage_zone", "release_zone"))
        ]

    @property
    def comment_lines(self) -> list[tuple[int, str]]:
        return [line for line in self.lines if line[1].startswith("--")]

    @property
    def gripper_lines(self) -> list[tuple[int, str]]:
        return [
            line for line in self.lines if line[1].startswith(("gripper_", "grip_"))
        ]
