from .load_strategy import TextLoader, CSVLoader, ExcelLoader

loaders = {
            '.xlsx': ExcelLoader(),
            '.xls': ExcelLoader(),
            '.csv': CSVLoader(),
            '.txt': TextLoader(),
        }
    