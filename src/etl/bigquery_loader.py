"""
Carrega os dados processados (camada real + sintética) no BigQuery.

Requer a variável de ambiente GOOGLE_APPLICATION_CREDENTIALS apontando
para um arquivo de service account JSON, e GCP_PROJECT_ID / BQ_DATASET
definidos em .env (ver .env.example).
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET = os.getenv("BQ_DATASET", "g1_pulse")
LOCATION = os.getenv("BQ_LOCATION", "US")
INPUT_PATH = Path("data/processed/articles_with_engagement.csv")


def carregar_no_bigquery(tabela: str = "articles_engagement"):
    if not PROJECT_ID:
        raise RuntimeError("Defina GCP_PROJECT_ID no arquivo .env antes de rodar este script.")

    client = bigquery.Client(project=PROJECT_ID)
    dataset_ref = bigquery.DatasetReference(PROJECT_ID, DATASET)

    try:
        client.get_dataset(dataset_ref)
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = LOCATION
        client.create_dataset(dataset)
        print(f"Dataset {DATASET} criado em {LOCATION}.")

    df = pd.read_csv(INPUT_PATH)
    tabela_ref = dataset_ref.table(tabela)

    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
    job = client.load_table_from_dataframe(df, tabela_ref, job_config=job_config)
    job.result()

    print(f"Carregados {len(df)} registros em {PROJECT_ID}.{DATASET}.{tabela}")


if __name__ == "__main__":
    carregar_no_bigquery()
