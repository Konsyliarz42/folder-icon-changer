from pathlib import Path
from .iconChanger import IconChanger

if __name__ == "__main__":
    chager = IconChanger()
    chager.include_json("example.json")
