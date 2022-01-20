import json
from pathlib import Path

from .icon_changer import Directory


if __name__ == "__main__":
    with open("icons.json", "r") as file:
        icons = json.loads(file.read())

    founded_folders = list()

    for drive in "CDEFGHIJKLMNOPRSTUWXYZ":
        drive = Path(f"{drive}:/")

        if drive.exists():
            print(f"Searching directories in:", drive)

        folders = [
            f
            for f in drive.rglob("*")
            if f.is_dir() and f.name in icons.keys()
            and u"Windows\\WinSxS" not in str(f)
            and u"Windows\\System" not in str(f)
            and u"WindowsApps\\Microsoft" not in str(f)
        ]

        if folders:
            for folder in folders:
                founded_folders.append(
                    (folder, icons[folder.name])
                )
                print("\t-", folder)

    print(f"Setting icons for {len(founded_folders)} folders ...")
    missing_folders = list()

    for folder, icon in founded_folders:
        icon = Path(".").joinpath(icon).absolute()

        try:
            Directory(folder).set_icon(str(icon))
        except PermissionError:
            missing_folders.append(folder)

    print("Missing folders:", len(missing_folders))

    for folder in missing_folders:
        print("\t-", folder)   