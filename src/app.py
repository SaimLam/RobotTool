from comau_explorer.explore import ComauExplorer
from comau_model.program import ComauProgram


def main() -> None:
    my_explorer = ComauExplorer("/home/sai/Documents/RoboTool/robotool")
    prog: ComauProgram = my_explorer.get_program("PW_DX_J4UPPZ1030R01")

    print(prog.name)
    print("")
    print(prog.body.text)
    print("")


if __name__ == "__main__":
    main()
