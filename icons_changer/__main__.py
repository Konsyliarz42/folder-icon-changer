from pathlib import Path
from .iconChanger import IconChanger

if __name__ == "__main__":
    folder = Path("./test_folder")
    icon = Path("./test_folder/test_icon.ico")

    chager = IconChanger()
    chager.include_json("icons.json")
