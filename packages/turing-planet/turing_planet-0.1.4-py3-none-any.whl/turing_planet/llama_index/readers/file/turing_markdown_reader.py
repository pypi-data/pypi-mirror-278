"""Markdown parser.

Contains parser for md files.

继承MarkdownReader，重写load_data函数，将文档的主标题，拼接到子标题，增强段落的上下文关系

"""
from pathlib import Path
from typing import Dict, List, Optional

from llama_index.core.schema import Document
from llama_index.readers.file import MarkdownReader


class TuringMarkdownReader(MarkdownReader):

    def load_data(
            self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        """Parse file into string."""
        tups = self.parse_tups(file)
        results = []
        # 获取文档的摘要
        summary = tups[0][1]
        summary_dic = {'summary': summary}
        if extra_info:
            extra_info.update(summary_dic)

        # TODO: don't include headers right now
        for header, value in tups:
            if header is None:
                results.append(Document(text=value, metadata=extra_info or summary_dic))
            else:
                results.append(
                    Document(text=f"\n\n{header}\n{value}", metadata=extra_info or summary_dic)
                )
        return results