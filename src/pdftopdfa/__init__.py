# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""pdftopdfa - Convert PDF files to PDF/A format."""

from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING

from .converter import (
    ConversionResult,
    PDFUAReviewFinding,
    PDFUAStatus,
    ProfileValidationResult,
    PublicationPolicy,
    convert_directory,
    convert_files,
    convert_to_pdfa,
)
from .exceptions import (
    ConversionError,
    FontEmbeddingError,
    OCRError,
    PDFToPDFAError,
    UnsupportedPDFError,
    ValidationError,
    VeraPDFError,
)
from .ocr import OCRSession, recognize_image

if TYPE_CHECKING:
    from .table import (
        TableBoundingBox,
        TableCell,
        TableRecognitionResult,
        TableType,
        prepare_table_runtime,
        recognize_table,
    )

# The table API is resolved on first access, so importing pdftopdfa does not
# load pdftopdfa.table. Neither import loads PaddleOCR; see
# prepare_table_runtime().
_TABLE_EXPORTS = frozenset(
    {
        "TableBoundingBox",
        "TableCell",
        "TableRecognitionResult",
        "TableType",
        "prepare_table_runtime",
        "recognize_table",
    }
)

try:
    __version__ = version("pdftopdfa")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [
    "__version__",
    "convert_to_pdfa",
    "convert_files",
    "convert_directory",
    "OCRSession",
    "recognize_image",
    "recognize_table",
    "prepare_table_runtime",
    "ConversionResult",
    "PDFUAReviewFinding",
    "PDFUAStatus",
    "ProfileValidationResult",
    "PublicationPolicy",
    "TableType",
    "TableBoundingBox",
    "TableCell",
    "TableRecognitionResult",
    "PDFToPDFAError",
    "ConversionError",
    "ValidationError",
    "FontEmbeddingError",
    "UnsupportedPDFError",
    "OCRError",
    "VeraPDFError",
]


def __getattr__(name: str) -> object:
    if name not in _TABLE_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    # A static import keeps pdftopdfa.table visible to freezing tools such as
    # PyInstaller, which do not follow importlib.import_module() strings.
    from . import table

    value = getattr(table, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted({*globals(), *_TABLE_EXPORTS})
