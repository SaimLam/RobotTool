from src.comau_model.explore import ComauExplorer
from src.comau_model.program import ComauProgram


def main() -> None:
    explorer = ComauExplorer(
        path="/home/sai/Documents/Code_Projects/RobotTools/RobotTool"
    )
    program: ComauProgram = explorer.get_program("PW_DX_J4UPPZ1030R01")

    print()
    print(program.name)
    print()

    for spot in program.weld_spots:
        print(spot.name)
        print()
        print(spot.condition)
        print()


if __name__ == "__main__":
    main()
