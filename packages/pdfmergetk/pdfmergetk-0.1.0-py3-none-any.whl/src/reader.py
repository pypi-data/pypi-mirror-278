# -*- coding: utf-8 -*-
"""
ReaderPDFImage : in charge to read PDF file and convert data of pages into
                 images.
"""

import fitz

from PIL import Image, ImageTk

from src.models import PDFile


class ReaderPDFImage:
    """
    Class in charge of read PDF file and converts data of pages into image.
    """

    def read_pdf(
        filename: str = None
    ) -> fitz.fitz.Document:
        """
        Reads data of PDF file or create a new PDF file.
        """
        if filename is None:
            return fitz.open()
        else:
            return fitz.open(filename, filetype='pdf')


class ImagesTKGenerator:

    def __init__(
        self,
        pdfile: PDFile,
        height: int,
        width: int
    ) -> None:
        """
        """
        self.pdfile = pdfile
        self.height = height
        self.width = width

    def generator(self) -> list:
        """
        PDF file page image generator.
        """
        # images = []
        for page in self.pdfile.data:
            page_pix = page.get_pixmap()
            currentImage = Image.frombytes(
                                    mode='RGB',
                                    size=[page_pix.width, page_pix.height],
                                    data=page_pix.samples
                                )

            resized_img = currentImage.resize(
                            (self.width, self.height),
                            Image.LANCZOS
                        )

            imageTK = ImageTk.PhotoImage(resized_img)
            yield imageTK

    def __repr__(self) -> str:
        """
        """
        return '< %s - image generator %s >' % (self.pdfile.name, id(self))
