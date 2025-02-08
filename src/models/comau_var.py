# This file contains the Comau var module which is used to extract and store information about a Comau variable.

def extract_single_var_lines( name: str, text:str) -> list:
    var_lines = []
    for line in text.split("\n"):
        if line.strip() and not line.startswith("--"):
            stripped_line = line.strip()
            split_name = stripped_line.split()[0]
            if split_name == name and not var_lines:
                var_lines.append(line)
            elif len(var_lines) == 1 and stripped_line.startswith("X"):
                var_lines.append(line)
            elif len(var_lines) == 2 and stripped_line.startswith("CNFG:"):
                var_lines.append(line)
    return var_lines
