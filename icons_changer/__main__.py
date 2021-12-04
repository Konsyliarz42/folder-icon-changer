from argparse import ArgumentParser

from .icon_changer import IconChanger


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--folder", help="Path to folder.", required=True)
    parser.add_argument("--icon", help="Path to icon file.", default=None)
    parser.add_argument("--index", help="Icon index.", default=0, type=int)
    args = parser.parse_args()
    changer = IconChanger()
    folder = changer.add_folder(args.folder, args.icon, args.index)
    changer.set_icon(folder)
