# Folder Icon Changer

[![Python application](https://github.com/Konsyliarz42/folder-icon-changer/actions/workflows/python-app.yml/badge.svg)](https://github.com/Konsyliarz42/folder-icon-changer/actions/workflows/python-app.yml)

> ONLY FOR WINDOWS SYSTEM!

This is program to change folder icon, via adding desktop.ini to folder.


## Manual 

### Set icon

```bash
python -m icon_changer --folder <folder path> --icon <icon path> --index <index of icon>
```

- folder path - Path to chosen folder.
- icon path - Path to chosen icon. Default: None
- index of icon - Index of chosen icon in icon file. Default: 0

### Remove icon

```bash
python -m icon_changer --folder <folder path>
```

- folder path - Path to chosen folder.
