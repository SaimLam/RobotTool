from comau_model.var_const_rout import CodVariable


def get_variables_string(cod_variables: list[CodVariable], batch_size: int = 4) -> str:
    var_string: str = "VAR \n "
    # sort the variables by type
    vars_sorted_by_type: dict[str, list[CodVariable]] = _sort_variables_by_type(
        cod_variables
    )
    # iterate over the sorted dictionary of variables and create a string
    for variable_type, variable_type_list in vars_sorted_by_type.items():
        if len(variable_type_list) <= batch_size:
            var_string += _single_var_line(variable_type_list, variable_type)
        else:
            # batch_size is a parameter
            for index in range(0, len(variable_type_list), batch_size):
                var_string += _single_var_line(
                    variable_type_list[index : index + batch_size], variable_type
                )

    return var_string


def _sort_variables_by_type(
    cod_variables: list[CodVariable],
) -> dict[str, list[CodVariable]]:
    variable_dict: dict[str, list[CodVariable]] = {}
    for variable in cod_variables:
        if variable.type not in variable_dict:
            variable_dict[variable.type] = [variable]
        else:
            variable_dict[variable.type].append(variable)
    return variable_dict


def _single_var_line(variables: list[CodVariable], var_type: str = "") -> str:
    if var_type == "":
        var_type = variables[0].type
    return ", ".join([variable.name for variable in variables]) + f" : {var_type}\n "
