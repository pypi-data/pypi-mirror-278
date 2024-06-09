"""
pdfnaut is a Python library for reading and writing PDFs at a low level.
"""

from .parsers import PdfParser, PdfTokenizer
from .serializer import PdfSerializer
from .document import PdfDocument

__all__ = ("PdfParser", "PdfTokenizer", "PdfSerializer", "PdfDocument")

__name__ = "pdfnaut"
__version__ = "0.3.1"
__description__ = "Explore PDFs with ease"
__license__ = "Apache 2.0"
