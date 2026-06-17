"""
Gera métricas de engajamento SIMULADAS para os artigos coletados.

IMPORTANTE: nenhum número aqui reflete dados reais da Globo/G1.
Os parâmetros foram calibrados com base em padrões públicos e
genéricos conhecidos do setor de mídia digital (ver docs/metodologia.md):

- Editorias de maior volatilidade noticiosa (mundo, política) recebem
  picos de pageviews simulados maiores.
- Horários de pico (almoço e noite) recebem multiplicador de tráfego.
- Fins de semana têm volume geral reduzido.

Ajuste os parâmetros em `PARAMETROS_EDITORIA` conforme refinar o modelo.
"""

import json
from pathlib import Path

import numpy as np
import pandas as pd

INPUT_PATH = Path("data/raw/articles.jsonl")
OUTPUT_PATH = Path("data/processed/articles_with_engagement.csv")

PARAMETROS_EDITORIA = {
    "politica": {"media_pageviews": 8000, "desvio": 3000},
    "economia": {"media_pageviews": 5000, "desvio": 2000},
    "mundo": {"media_pageviews": 9000, "desvio": 4000},
    "natureza": {"media_pageviews": 3000, "desvio": 1200},
    "ciencia-e-saude": {"media_pageviews": 4000, "desvio": 1500},
    "educacao": {"media_pageviews": 2500, "desvio": 1000},
    "carros": {"media_pageviews": 3500, "desvio": 1400},
    "turismo-e-viagem": {"media_pageviews": 2800, "desvio": 1100},
}

HORARIOS_PICO = (12, 13, 19, 20, 21)


def gerar_engajamento(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = df.copy()

    df["publicado_em"] = pd.to_datetime(df["publicado_em"], errors="coerce", utc=True)
    df["hora_publicacao"] = df["publicado_em"].dt.hour
    df["fim_de_semana"] = df["publicado_em"].dt.dayofweek >= 5

    pageviews = []
    for _, row in df.iterrows():
        params = PARAMETROS_EDITORIA.get(
            row["editoria"], {"media_pageviews": 3000, "desvio": 1000}
        )
        base = rng.normal(params["media_pageviews"], params["desvio"])

        multiplicador_horario = 1.4 if row["hora_publicacao"] in HORARIOS_PICO else 1.0
        multiplicador_fds = 0.7 if row["fim_de_semana"] else 1.0

        valor = max(base * multiplicador_horario * multiplicador_fds, 100)
        pageviews.append(round(valor))

    df["pageviews_simulado"] = pageviews
    df["tempo_pagina_seg_simulado"] = (
        rng.normal(95, 25, size=len(df)).clip(min=20).round()
    )
    df["compartilhamentos_simulado"] = (
        df["pageviews_simulado"] * rng.uniform(0.005, 0.02, size=len(df))
    ).round()

    return df


def main():
    registros = [
        json.loads(linha) for linha in INPUT_PATH.open("r", encoding="utf-8") if linha.strip()
    ]
    if not registros:
        print("Nenhum artigo encontrado em data/raw/articles.jsonl. Rode rss_collector.py primeiro.")
        return

    df = pd.DataFrame(registros)
    df_final = gerar_engajamento(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(OUTPUT_PATH, index=False)
    print(f"{len(df_final)} registros processados com engajamento simulado.")


if __name__ == "__main__":
    main()
