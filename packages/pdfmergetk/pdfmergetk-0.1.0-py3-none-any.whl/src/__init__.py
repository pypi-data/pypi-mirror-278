# -*- coding: utf-8 -*-
"""
PDFMergeTK application.
"""

from src.gui import main

from src.gui import (
    ElementsTK,
    LanguagesClass,
    LoadImagePDFThread,
    MainGUI,
    UserListBox,
    DisplayCanvas,
    AvoidOpeningThemMultipleTimes,
    WarningOpenedApp
)

from src.styles import AppStyles
from src.langs import languagesDict
from src.reader import ReaderPDFImage
from src.models import PDFile
from src.dataclass import Data
from src.configmanager import ConfigManager
