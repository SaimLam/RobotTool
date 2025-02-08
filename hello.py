from src.models.comau_explore import ComauExplorer
from src.models.comau_program import ComauProgram


def main() -> None:
    explorer = ComauExplorer(path="/home/sai/Documents/RoboTool/robotool")
    program = explorer.get_program("PW_DX_J4UPPZ1030R01")

    if not isinstance(program, ComauProgram):
        print("Error: Expected a ComauProgram object, but got something else.")
        return

    for move in program.movements:
        print(move.var_string())


if __name__ == "__main__":
    main()
