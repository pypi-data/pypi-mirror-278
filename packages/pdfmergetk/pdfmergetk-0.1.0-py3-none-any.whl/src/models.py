# -*- coding: utf-8 -*-
"""
PDFile : PDF file object, holds their name, data, images, number of pages.
"""

import fitz

from typing import List


class PDFile:
    """
    In charge to holds data of PDF file.
    """

    def __init__(
        self,
        name: str,
        data: fitz.fitz.Document,
        images: List[fitz.fitz.Pixmap]
    ) -> None:
        """
        Constructor
        """
        self.name = name
        self.data = data
        self.images = images
        self.n_pages = len(self.data)

    def __repr__(self) -> str:
        """
        Returns a representation of instance.
        """
        return '<[ Name: %s, Pages: %i, Images: %i ]>' % (
                    self.name,
                    self.n_pages,
                    len(self.images)
                )
