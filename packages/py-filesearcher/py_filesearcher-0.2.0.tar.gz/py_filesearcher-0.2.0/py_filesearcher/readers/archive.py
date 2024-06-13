import pathlib
import typing
import zipfile

from py_filesearcher.readers.base import BaseReader
from py_filesearcher.readers.excel import ExcelReaderXls, ExcelReaderXlsx
from py_filesearcher.readers.text import TextReader
from py_filesearcher.readers.word import WordReader

DOCUMENT_READERS: typing.Dict[str, type(BaseReader)] = dict(
    docx=WordReader(),
    txt=TextReader(),
    c=TextReader(),
    xls=ExcelReaderXls(),
    xlsx=ExcelReaderXlsx(),
)


class ZipReader(BaseReader):
    def __init__(self):
        super().__init__()

    def read(self, file_path: typing.Union[pathlib.Path, typing.IO[bytes]]) -> str:
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            file_names = zip_file.namelist()

            for file_name in file_names:
                with zip_file.open(file_name) as file:
                    reader: BaseReader = DOCUMENT_READERS.get(
                        pathlib.Path(file_name).suffix[1:],
                        "Reader not found"
                    )
                    content = reader.read(file)
                    return content


ARCHIVE_READERS: typing.Dict[str, type(BaseReader)] = dict(
    zip=ZipReader(),
)

ALL_READERS: typing.Dict[str, type(BaseReader)] = dict(
    **DOCUMENT_READERS,
    **ARCHIVE_READERS
)
