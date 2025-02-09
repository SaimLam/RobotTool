from src.models.comau_explore import ComauExplorer


def main() -> None:
    explorer = ComauExplorer(
        path="/home/sai/Documents/Code_Projects/RobotTools/RobotTool"
    )
    program = explorer.get_program("PW_DX_J4UPPZ1030R01")

    print(program.name)
    print(program.header)
    for movement in program.movements:
        print(movement)
        print(movement.var_string())
        print()


if __name__ == "__main__":
    main()
