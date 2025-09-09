from .load_strategy import TextLoader, CSVLoader, ExcelLoader

loaders = {
    '.txt': TextLoader(),
    '.csv': CSVLoader(),  # Тепер з покращеною логікою
    '.xlsx': ExcelLoader(),
    '.xls': ExcelLoader(),
    # Можете додати інші розширення які теж мають оброблятися як текст
    '.dat': TextLoader(),
    '.data': TextLoader(),
}