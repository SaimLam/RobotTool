from comau_explorer.explore import ComauExplorer
from comau_model.program import ComauProgram


def main() -> None:
    my_explorer = ComauExplorer("/home/sai/Documents/RoboTool/robotool")
    prog: ComauProgram = my_explorer.get_program("PW_DX_J4UPPZ1030R01")

    print(prog.name)
    print("")
    for move in prog.move_list:
        print(move)
    print("")
    for weld_spot in prog.weld_spots:
        print(weld_spot)
    print("")


if __name__ == "__main__":
    main()
