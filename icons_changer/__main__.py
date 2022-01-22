from argparse import ArgumentParser

from .icon_changer import Directory


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--folder", help="Path to folder.", required=True)
    parser.add_argument("--icon", help="Path to icon file.", default=None)
    parser.add_argument("--index", help="Icon index.", default=0, type=int)

    args = parser.parse_args()
    folder = Directory(args.folder)

    if args.icon:
        folder.set_icon(args.icon, args.index)
    else:
        folder.remove_icon()
