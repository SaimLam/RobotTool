from comau_explorer.explore import ComauExplorer
from comau_model.program import ComauProgram


def main():
    my_explorer = ComauExplorer(
        "/home/sai/Documents/Code_Projects/RobotTools/RobotTool"
    )
    prog: ComauProgram = my_explorer.get_program("PW_DX_J4UPPZ1030R01")

    print(prog.name)
    print("")
    print(prog.variables_string())
    print("")


if __name__ == "__main__":
    main()
