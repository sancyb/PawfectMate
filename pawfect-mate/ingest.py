import minsearch
import os
import pandas as pd

DATA_PATH = "../data/rag_dataset.csv"

def load_index(data_path=DATA_PATH):
    df = pd.read_csv(data_path)
    df = df.fillna('')

    documents = df.to_dict(orient='records')

    index = minsearch.Index(
        text_fields=['breed_name', 'history', 'health', 'description', 'characteristics',
                     'appearance', 'temperament'],
        keyword_fields=['id']
    )

    index.fit(documents)
    return index
