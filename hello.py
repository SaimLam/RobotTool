from models.explore import Explore
from models.comau_program import ComauProgram


def main() -> None:
    explorer = Explore(path="/home/sai/Documents/RoboTool/robotool")

    program = ComauProgram(
        explorer.file_read(
            file_path="/home/sai/Documents/RoboTool/robotool/PW_DX_J4UPPZ1030R01.pdl"
        )
    )

    print(program.name)
    """    for move in program.movements:
            # print(move.var_string())
            print(move)
            # print("\n")"""


if __name__ == "__main__":
    main()
