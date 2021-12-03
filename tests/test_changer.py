from unittest import TestCase
from pathlib import Path
from configparser import ConfigParser

from icons_changer.icon_changer import IconChanger

INI_NAME = "desktop.ini"
INI_SECTION = '.ShellClassInfo'
INI_OPTIONS = ['IconFile', 'IconIndex', "ConfirmFileOp"]

TEST_FOLDER_PATH = "tests/test-folder"
TEST_ICON_PATH = TEST_FOLDER_PATH + "/test-icon.ico"
TEST_INI_PATH = TEST_FOLDER_PATH + "/" + INI_NAME


class TestChanger(TestCase):
    def setUp(self):
        self.changer = IconChanger()

    def test_add_and_remove_folder(self):
        """
        Check adding and removing folder.
        """

        # Adding
        queue_of_folders = self.changer.folders.copy()
        self.changer.add_folder(TEST_FOLDER_PATH)
        self.assertFalse(queue_of_folders == self.changer.folders)

        # Removing
        queue_of_folders = self.changer.folders.copy()
        self.changer.remove_folder(0)
        self.assertFalse(queue_of_folders == self.changer.folders)

    def test_attributes(self):
        """
        Check base values of data about folder.
        """

        self.changer.add_folder(TEST_FOLDER_PATH, TEST_ICON_PATH)
        folder = self.changer.folders[0]

        self.assertTrue(folder.folder_path.is_absolute())
        self.assertTrue(folder.icon_path.is_absolute())
        self.assertFalse(folder.may_delete_ini)
        self.assertTrue(folder.ini_config.has_section(INI_SECTION))

        for option in INI_OPTIONS:
            self.assertTrue(folder.ini_config.has_option(INI_SECTION, option))

        self.assertEqual(
            folder.ini_path,
            folder.folder_path.joinpath(INI_NAME)
        )

    def test_change_icon(self):
        """
        Check if folder changed icon.
        """

        self.assertFalse(Path(TEST_INI_PATH).exists())

        self.changer.add_folder(TEST_FOLDER_PATH, TEST_ICON_PATH)
        folder = self.changer.folders[0]
        self.assertFalse(folder.may_delete_ini)
        self.changer.set_icon(folder)

        self.assertTrue(Path(TEST_INI_PATH).exists())
        config = ConfigParser()
        config.read(TEST_INI_PATH)
        self.assertTrue(config.has_section(INI_SECTION))
        self.assertTrue(config.has_option(INI_SECTION, INI_OPTIONS[0]))

        self.changer.add_folder(TEST_FOLDER_PATH)
        folder = self.changer.folders[1]
        self.assertTrue(folder.may_delete_ini)
        self.changer.set_icon(folder)
        self.assertFalse(Path(TEST_INI_PATH).exists())
