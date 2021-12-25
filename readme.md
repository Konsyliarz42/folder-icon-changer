![Logo](./assets/logo.png)

[![Python application](https://github.com/Konsyliarz42/folder-icon-changer/actions/workflows/python-app.yml/badge.svg?event=push)](https://github.com/Konsyliarz42/folder-icon-changer/actions/workflows/python-app.yml)
[![Unittests](https://github.com/Konsyliarz42/folder-icon-changer/actions/workflows/unittests.yml/badge.svg?branch=master&event=push)](https://github.com/Konsyliarz42/folder-icon-changer/actions/workflows/unittests.yml)

> ONLY FOR WINDOWS!

This is program to change folder icon, via adding desktop.ini to folder.

## Usage

1. Select folder
2. Select icon (only [.ico](https://en.wikipedia.org/wiki/ICO_(file_format)) type)
3. Check preview
4. Set icon
5. Fell happy :)

## Manual 

### Set icon

```bash
python -m icon_changer --folder <folder path> --icon <icon path> --index <index of icon>
```

- `folder path` - Path to chosen folder.
- `icon path` - Path to chosen icon. Default: None
- `index of icon` - Index of chosen icon in icon file. Default: 0

### Remove icon

```bash
python -m icon_changer --folder <folder path>
```

- `folder path` - Path to chosen folder.

