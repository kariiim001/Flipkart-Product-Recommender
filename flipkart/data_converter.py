import pandas as pd
from langchain_core.documents import Document

class DataConverter:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def convert_to_documents(self):
        df = pd.read_csv(self.file_path)[['product_title', 'summary','review']]

        docs = [
            Document(
                page_content=row['review'],
                  metadata={"product_title": row['product_title'],
                             "summary": row['summary']}) for _, row in df.iterrows()
        ]
        return docs
