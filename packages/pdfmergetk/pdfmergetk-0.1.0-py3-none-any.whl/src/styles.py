# -*- coding: utf-8 -*-
"""
AppStyles : in charge of styles of app.
"""

import tkinter as tk
from tkinter import ttk


class AppStyles:
    """
    In charge of all style of elements of application.
    """
    default_font = 'DejaVu Serif'
    default_size = 10
    canvas_bg = '#f8f8ff'
    color_background = '#f4f4f4'
    menu_bg = '#d7d7d7'
    active_menu = '#f0f0f0'

    def __init__(self) -> None:
        """
        Constructor
        """
        self.__style = ttk.Style()
        self.__style.theme_use('clam')

        self.frame()
        self.entrys()
        self.labels()
        self.entrys()

    def frame(self) -> None:
        """
        Style for frames.
        """
        self.__style.configure(
                'FrameStyle.TFrame',
                background=AppStyles.color_background,
            )

    def buttons(self) -> None:
        """
        Style to buttons.
        """
        self.__style.configure(
                'ButtonController.TButton',
                font=(AppStyles.default_font, AppStyles.default_size + 5),
                anchor=tk.CENTER,
                justify='center',
                background=AppStyles.color_background
            )

        self.__style.configure(
                'Button.TButton',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER,
                justify='center',
                background=AppStyles.color_background
            )
        self.__style.configure(
            'ButtonJoinMerge.TButton',
            font=(AppStyles.default_font, AppStyles.default_size + 1, 'bold'),
            anchor=tk.CENTER,
            justify='center',
            background=AppStyles.color_background
        )

    def labels(self) -> None:
        """
        Styles to labels.
        """
        self.__style.configure(
                'LabelListPDF.TLabel',
                font=(AppStyles.default_font, AppStyles.default_size),
                anchor=tk.CENTER,
                justify='center',
                background=AppStyles.color_background
            )
        self.__style.configure(
                'LabelListbox.TLabel',
                font=(AppStyles.default_font, AppStyles.default_size, 'bold'),
                anchor=tk.CENTER,
                justify='center',
                background=AppStyles.color_background
            )
        self.__style.configure(
                'LabelIndexPage.TLabel',
                font=(
                    AppStyles.default_font,
                    AppStyles.default_size + 2,
                    'bold'
                ),
                anchor=tk.CENTER,
                justify='center',
                borderwidth=2,
                relief=tk.GROOVE,
                # highlightthickness=0,
                background=AppStyles.color_background,
            )
        self.__style.configure(
                'LabelLinkProject.TLabel',
                font=(
                    AppStyles.default_font,
                    AppStyles.default_size - 1,
                    'bold'
                ),
                anchor=tk.CENTER,
                justify='center',
                background=AppStyles.color_background,
            )
        self.__style.configure(
                'AuthorLabel.TLabel',
                font=(
                    AppStyles.default_font,
                    AppStyles.default_size + 1,
                    'bold'
                ),
                anchor=tk.CENTER,
                justify='center',
                background=AppStyles.color_background,
            )

    def entrys(self) -> None:
        """
        Style to entry.
        """
        self.__style.configure(
                'PDFOutput.TEntry',
                font=(AppStyles.default_font, AppStyles.default_size),
                padding=(5, 0, 5, 0),
                anchor=tk.CENTER,
                background='white'
            )
