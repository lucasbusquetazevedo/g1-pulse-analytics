"""
Coleta metadados de artigos do G1 via feeds RSS públicos por editoria.

Camada de dados REAIS do projeto G1 Pulse — não coleta métricas de
engajamento (pageviews, tempo na página, etc.), que são dados internos
do produto e não estão disponíveis publicamente. Essa camada é gerada
separadamente em src/synthetic/generate_engagement.py.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import feedparser

CATEGORIAS = [
    "politica",
    "economia",
    "mundo",
    "natureza",
    "ciencia-e-saude",
    "educacao",
    "carros",
    "turismo-e-viagem",
]

BASE_URL = "https://g1.globo.com/rss/g1/{categoria}"
OUTPUT_PATH = Path("data/raw/articles.jsonl")


def carregar_links_existentes(path: Path) -> set:
    if not path.exists():
        return set()
    links = set()
    with path.open("r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            registro = json.loads(linha)
            links.add(registro["link"])
    return links


def coletar_categoria(categoria: str) -> list[dict]:
    url = BASE_URL.format(categoria=categoria)
    feed = feedparser.parse(url)
    artigos = []
    for entrada in feed.entries:
        artigos.append(
            {
                "id": hashlib.sha256(entrada.link.encode()).hexdigest()[:16],
                "titulo": entrada.title,
                "link": entrada.link,
                "editoria": categoria,
                "publicado_em": entrada.get("published", None),
                "coletado_em": datetime.now(timezone.utc).isoformat(),
            }
        )
    return artigos


def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    links_existentes = carregar_links_existentes(OUTPUT_PATH)

    novos = []
    for categoria in CATEGORIAS:
        try:
            artigos = coletar_categoria(categoria)
        except Exception as erro:
            print(f"Falha ao coletar '{categoria}': {erro}")
            continue

        for artigo in artigos:
            if artigo["link"] not in links_existentes:
                novos.append(artigo)
                links_existentes.add(artigo["link"])

    if novos:
        with OUTPUT_PATH.open("a", encoding="utf-8") as f:
            for artigo in novos:
                f.write(json.dumps(artigo, ensure_ascii=False) + "\n")

    print(f"{len(novos)} novos artigos coletados.")


if __name__ == "__main__":
    main()
