from .load_strategy import FileLoader, TextLoader, CSVLoader, ExcelLoader
from typing import Dict

loaders: Dict[str, FileLoader] = {
    '.txt': TextLoader(),
    '.csv': CSVLoader(),
    '.xlsx': ExcelLoader(),
    '.xls': ExcelLoader(),
    '.dat': TextLoader(),
    '.data': TextLoader(),
}