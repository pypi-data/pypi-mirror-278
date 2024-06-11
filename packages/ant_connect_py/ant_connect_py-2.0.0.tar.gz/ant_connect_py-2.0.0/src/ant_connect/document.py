""" Document Dataclass Module. """

from __future__ import annotations
from pathlib import Path
from dataclasses import dataclass, asdict
import base64


@dataclass
class Document:
    """Dataclass for the ANT Document object. Use this object to parse
    and encode documents for up- and downloading to ANT CDE."""

    name: str
    extension: str
    data: str

    @staticmethod
    def _parse(document_path: Path) -> bytes:
        """Parse a document to a base64 encoded string."""
        with open(document_path, "rb") as image_file:
            encoded_file = base64.b64encode(image_file.read())

        return encoded_file

    @classmethod
    def parse_to_object(cls, document_path: Path | str) -> Document:
        """Parse a document with file path to a Document object.

        Parameters
        ----------
        document_path : Path | str
            Path to the document.

        Returns
        -------
        Document
            Document object.

        Raises
        ------
        Exception
            If document cannot be found or opened, or content is not in utf-8 format
        """
        if isinstance(document_path, str):
            document_path = Path(document_path)

        encoded_file = cls._parse(document_path)
        return cls(
            name=document_path.stem,
            extension=document_path.suffix,
            data=encoded_file.decode("utf-8"),
        )

    def encode_to_file(self, file_path: Path | str = "") -> None:
        """Encode the document data object to a file.

        Args:
            file_path (Path | str, optional): Path to document. Defaults to ''.

        Raises:
            TypeError: Error saving file from ANT.
        """
        if isinstance(file_path, str):
            file_path = Path(file_path)

        full_path = file_path / f"{self.name}{self.extension}"

        try:
            with open(full_path, "wb+") as file:
                file.write(base64.b64decode(self.data.encode("utf-8")))
        except Exception as e:
            raise TypeError(f"Error saving file from ANT: {e}")

    def as_dict(self) -> dict:
        """Return the document object as a dictionary."""
        return asdict(self)
