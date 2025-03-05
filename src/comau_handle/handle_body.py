def apply_modifications(
    original_lines: list[tuple[int, str]], modifications: list[tuple[int, str]]
) -> list[tuple[int, str]]:
    modified_lines = original_lines.copy()
    for mod_index, mod_str in modifications:
        for i, (orig_index, _) in enumerate(modified_lines):
            if orig_index == mod_index:
                modified_lines[i] = (orig_index, mod_str)
                break
    return modified_lines
