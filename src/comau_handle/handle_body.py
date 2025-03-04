def generate_body_str(
    lines: list[tuple[int, str]], modifications: list[tuple[int, str]]
) -> str:
    body_str = "BEGIN\n"
    for line in lines:
        modified_line: str = _get_modified_line(line[0], modifications)
        if modified_line:
            body_str += modified_line + "\n"
        else:
            body_str += line[1] + "\n"

    return body_str


def _get_modified_line(line_index: int, modifications: list[tuple[int, str]]) -> str:
    modified_line: str = ""
    for line in modifications:
        if line[0] == line_index:
            modified_line = line[1]
            break
    return modified_line
