from typing import Optional, Dict, List
from pathlib import Path
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
import pandas as pd

# 显示全部列
pd.set_option('display.max_columns', None)
# 显示全部行
pd.set_option('display.max_row', None)
# 设置数据的显示长度（解决自动换行）
pd.set_option('display.width', None)
# 设置value的显示长度为100，默认为50
pd.set_option('max_colwidth', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)


class ExcelReader(BaseReader):

    def load_data(
            self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        excel_data = pd.ExcelFile(file)

        # 获取所有工作表的名称
        sheet_names = excel_data.sheet_names

        # 读取特定工作表的数据
        data = ""
        for sheet_name in sheet_names:
            df = pd.read_excel(file, sheet_name, dtype=str)
            data = f"{data}{sheet_name}:\n{df}\n"

        return [Document(text=data, metadata=extra_info)]


class ExcelSummaryReader(BaseReader):

    def load_data(
            self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[Document]:
        excel_data = pd.ExcelFile(file)

        # 获取所有工作表的名称
        sheet_names = excel_data.sheet_names

        # 读取特定工作表的数据
        data = extra_info['file_name']
        for sheet_name in sheet_names:
            df = pd.read_excel(file, sheet_name, dtype=str)
            data = f"{data}{sheet_name}:\n{df.columns.tolist()}\n"

        return [Document(text=data, metadata=extra_info)]
