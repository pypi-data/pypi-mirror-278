# py-filesearcher

py-filesearcher是一个Python库，用于实现各类文件中特定字符的识别。

## 特点

支持文档类型包括

- 文本文件: .py, .c, .txt, .md
- OFFICE文件: .docx, .xls, .xlsx
- 压缩文件: .zip

## 安装

你可以使用 `pip` 安装 `py-filesearcher`:

```bash
pip install py-filesearcher
```

## 使用

```python
import pathlib
from py_filesearcher.indexer import Indexer

indexer = Indexer(
    search_dir=pathlib.Path("") / "data",
    index_dir=pathlib.Path("index")
)

match_contents = indexer.query_reg("world")
for m in match_contents:
    print(f"文件名: [{m.filename}], 匹配内容: [{[x.decode('utf8') for x in m.match_text]}]")
```