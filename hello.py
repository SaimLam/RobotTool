from src.models.comau_explore import ComauExplorer


def main() -> None:
    explorer = ComauExplorer(path="/home/sai/Documents/RoboTool/robotool")
    program = explorer.get_program("PW_DX_J4UPPZ1030R01")

    print()
    print(program.name)
    print()
    print(program.header)
    print()
    for spot in program.weld_spots():
        print(spot)
        print(spot.spot_index)
        print()


if __name__ == "__main__":
    main()
