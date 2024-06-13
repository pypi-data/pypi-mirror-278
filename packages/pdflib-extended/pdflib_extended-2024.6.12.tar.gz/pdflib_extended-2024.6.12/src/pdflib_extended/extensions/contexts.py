from contextlib import AbstractContextManager
from pathlib import Path
from typing import Union, Optional, ContextManager, TYPE_CHECKING
from typing_extensions import Self
from .blocks import Block
from ..core.pdflib_base import PDFlibBase  # noqa: F401

from ..exceptions import (
    InvalidDocumentHandle,
    InvalidPageHandle,
    DocumentWriteException,
    EmptyNewDocumentException,
    InvalidImageHandle,
)

if TYPE_CHECKING:
    from ..pdflib import PDFlib


class Page(AbstractContextManager["Page"]):
    def __init__(
        self,
        p: "PDFlib",
        document_handle: int,
        page_number: int,
        optlist: Optional[str] = "",
    ) -> None:
        self.p = p
        self.document_handle = document_handle
        self.page_number = page_number
        self.optlist = optlist

    def __enter__(self) -> Self:
        self.handle: int = self.p.open_pdi_page(
            self.document_handle, self.page_number, self.optlist
        )
        if self.handle < 0:
            raise InvalidPageHandle(self.p.get_errmsg())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.p.close_pdi_page(self.handle)

    def fit_page(self, x: float, y: float, optlist: Optional[str] = "") -> None:
        self.p.fit_pdi_page(self.handle, x, y, optlist)

    @property
    def block_count(self) -> int:
        return int(
            self.p.pcos_get_number(
                self.document_handle, f"length:pages[{self.page_number - 1}]/blocks"
            )
        )

    @property
    def blocks(self) -> list[Block]:
        return [Block.create_block(self.p, self, i) for i in range(self.block_count)]

    @property
    def width(self) -> float:
        width: float = self.p.pcos_get_number(
            self.document_handle, f"pages[{self.page_number - 1}]/width"
        )
        return width

    @property
    def height(self) -> float:
        height: float = self.p.pcos_get_number(
            self.document_handle, f"pages[{self.page_number - 1}]/height"
        )
        return height


class Document(AbstractContextManager["Document"]):
    def __init__(
        self, p: "PDFlib", file_path: Union[str, Path], optlist: Optional[str] = ""
    ) -> None:
        self.p = p
        self.file_path = Path(file_path)
        self.optlist = optlist

    def __enter__(self) -> Self:
        self.handle: int = self.p.open_pdi_document(
            self.file_path.as_posix(), self.optlist
        )
        if self.handle < 0:
            raise InvalidDocumentHandle(self.p.get_errmsg())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.p.close_pdi_document(self.handle)

    def open_page(
        self, page_number: int, optlist: Optional[str] = ""
    ) -> ContextManager[Page]:
        return Page(self.p, self.handle, page_number, optlist)

    @property
    def page_count(self) -> int:
        return int(self.p.pcos_get_number(self.handle, "length:pages"))


class NewPage(AbstractContextManager["NewPage"]):
    def __init__(
        self, p: "PDFlib", width: float, height: float, optlist: Optional[str] = ""
    ) -> None:
        self.p = p
        self.width = width
        self.height = height
        self.optlist = optlist

    def __enter__(self) -> Self:
        self.p.begin_page_ext(self.width, self.height, self.optlist)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.p.end_page_ext("")


class NewDocument(AbstractContextManager["NewDocument"]):
    def __init__(
        self, p: "PDFlib", file_path: Union[str, Path], optlist: Optional[str] = ""
    ) -> None:
        self.p = p
        self.file_path = Path(file_path)
        self.optlist = optlist
        self.page_count = 0

    def __enter__(self) -> Self:
        result = self.p.begin_document(self.file_path.as_posix(), "")
        if result < 0:
            raise DocumentWriteException(self.p.get_errmsg())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if not self.page_count > 0:
            raise EmptyNewDocumentException(
                "Generated document doesn't contain any pages"
            )
        self.p.end_document("")

    def start_page(
        self,
        width: float = 612.0,
        height: float = 792.0,
        optlist: Optional[str] = "",
    ) -> ContextManager[NewPage]:
        self.page_count += 1
        return NewPage(self.p, width, height, optlist)


class Image(AbstractContextManager["Image"]):
    def __init__(
        self,
        p: "PDFlib",
        file_path: Union[str, Path],
        image_type: Optional[str] = "auto",
        optlist: Optional[str] = "",
    ) -> None:
        self.p = p
        self.file_path = Path(file_path)
        self.image_type = image_type
        self.optlist = optlist

    def __enter__(self) -> Self:
        self.handle = self.p.load_image(
            self.image_type, self.file_path.as_posix(), self.optlist
        )
        if self.handle < 0:
            raise InvalidImageHandle(self.p.get_errmsg())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.p.close_image(self.handle)

    @property
    def width(self) -> float:
        width: float = self.p.info_image(self.handle, "imagewidth", "")
        return width

    @property
    def height(self) -> float:
        height: float = self.p.info_image(self.handle, "imageheight", "")
        return height

    def fit_image(self, x: float, y: float, optlist: Optional[str] = "") -> None:
        self.p.fit_image(self.handle, x, y, optlist)
