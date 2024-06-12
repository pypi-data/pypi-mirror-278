import pathlib
import typing

from chardet.universaldetector import UniversalDetector
from jieba.analyse import ChineseAnalyzer
from whoosh.fields import TEXT, Schema, ID
from whoosh.index import create_in, FileIndex
from whoosh.query import Regex

MatchContent = typing.NamedTuple("MatchContent", (("filename", str), ("match_text", typing.List[bytes])))

DEFAULT_EXTENSIONS = ["md", "txt", "c", "h", "py"]


class Indexer:
    def __init__(
            self,
            search_dir: pathlib.Path,
            index_dir: pathlib.Path,
            extensions: typing.Optional[typing.List[str]] = None
    ) -> None:
        if extensions is None:
            extensions = DEFAULT_EXTENSIONS

        self.search_dir = search_dir
        self.index_dir = index_dir
        self.index: typing.Optional[FileIndex] = None
        self.extensions = extensions

        self.schema = Schema(
            title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
            path=ID(stored=True),
            content=TEXT(stored=True)
        )

        self._create_index_dir()
        self._parse_search_dir()

    def _create_index_dir(self):
        if not self.index_dir.exists():
            self.index_dir.mkdir(exist_ok=True)

    def _parse_search_dir(self):
        self.index = create_in(self.index_dir, schema=self.schema)
        writer = self.index.writer()

        files = []
        for ext in self.extensions:
            files.extend(self.search_dir.rglob(f"*.{ext.lower()}"))
        print(f"[*] 找到匹配后缀文件{len(files)=}")

        detector = UniversalDetector()
        for file in files:
            detector.reset()

            with open(file, "rb") as f:
                detector.feed(f.readline())

            encoding = detector.result['encoding'] if detector.result['encoding'] != 'ascii' else 'utf8'
            with open(file, "r", encoding=encoding) as f:
                print(f"增加文件{file.name=}, {encoding=}")
                writer.add_document(title=file.name, path=file.name, content="\n".join(f.readlines()))

        detector.close()
        writer.commit()

    def query_reg(self, text: str) -> typing.List[MatchContent]:
        query = Regex("content", text)
        matches: typing.List[MatchContent] = []

        if self.index is not None:
            with self.index.searcher() as s:
                results = s.search(query, terms=True)
                for hit in results:
                    matches.append(MatchContent(filename=hit["path"], match_text=[x[1] for x in hit.matched_terms()]))
            return matches
