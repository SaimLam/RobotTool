class ComauCod:
    def __init__(self, text: str) -> None:
        self.text = text

    @property  # Get variable, costants and routine declarations from cod string
    def declarations(self) -> list:
        declarations = []
        if "BEGIN" in self.text:
            for line in self.text.split("BEGIN")[0].split("\n"):
                line = line.strip()
                if line and not line.startswith("--"):
                    if "VAR" in line:
                        line = line.replace("VAR", "")
                    if "CONST" in line:
                        line = line.replace("CONST", "")
                    declarations.append(line)
        return declarations

    @property  # Get the program cod header
    def header(self) -> str:
        if self.declarations:
            for line in self.declarations:
                if line.startswith("PROGRAM"):
                    return line
        return ""

    @property  # Get program cod body from BEGIN to END
    def body(self) -> str:
        if "BEGIN" in self.text and "END" in self.text:
            return self.text.split("BEGIN")[1]
        return ""

    @property  # Get list of constant declarations
    def constants(self) -> list:
        declarations = self.declarations
        return [
            line
            for line in declarations
            if "=" in line and not line.startswith("ROUTINE")
        ]

    @property  # Get used routines only from declarations
    def routines(self) -> list:
        routines = []
        body = self.body
        for line in self.declarations:
            if line.startswith("ROUTINE"):
                if (
                    "(" in line
                    and line.split("ROUTINE ")[1].split("(")[0].strip() in body
                ):
                    routines.append(line)

                elif (
                    line.split("ROUTINE ")[1].split("EXPORTED FROM")[0].strip() in body
                ):
                    routines.append(line)
        return routines

    @property  # Get variable lines from declarations that are used in the program body.
    def var_lines(self) -> list:
        variable_lines = []
        declarations = self.declarations
        if declarations:
            for line in declarations:
                if ":" in line and not (
                    line.startswith("ROUTINE") or line.startswith("PROGRAM")
                ):
                    used_vars = self._extract_used_vars(line)
                    if used_vars:
                        variable_lines.append(
                            self._create_var_line(used_vars, line.split(":")[1].strip())
                        )
        return variable_lines

    def _extract_used_vars(self, variable_line: str) -> list:
        used_variables = []
        body = self.body
        for var in variable_line.split(":")[0].split(","):
            if var.strip() in body:
                used_variables.append(var.strip())
        return used_variables

    def _create_var_line(self, variables: list, variable_type: str) -> str:
        var_line = ", ".join(variables)
        return f"{var_line} : {variable_type}"
