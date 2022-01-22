from unittest import TestCase
from pathlib import Path
from configparser import ConfigParser

from icons_changer.icon_changer import Directory

INI_NAME = "desktop.ini"
INI_SECTION = ".ShellClassInfo"
INI_OPTIONS = ["IconFile", "IconIndex", "ConfirmFileOp"]

TEST_FOLDER_PATH = "tests/test-folder"
TEST_ICON_PATH = TEST_FOLDER_PATH + "/test-icon.ico"
TEST_INI_PATH = TEST_FOLDER_PATH + "/" + INI_NAME


class TestChanger(TestCase):

    def test_create_object(self):
        Directory(TEST_FOLDER_PATH)

    def test_add_and_remove_icon(self):
        directory = Directory(TEST_FOLDER_PATH)
        
        directory.set_icon(TEST_ICON_PATH)
        self.assertTrue(Path(TEST_INI_PATH).exists())

        directory.remove_icon()
        self.assertFalse(Path(TEST_INI_PATH).exists())
