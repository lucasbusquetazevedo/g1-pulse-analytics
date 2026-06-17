"""
Simula um teste A/B de manchete/thumbnail para um subconjunto de artigos
e avalia significância estatística via teste de proporções (z-test).

Os dados de conversão são simulados — ver docs/metodologia.md.
"""

import numpy as np
from statsmodels.stats.proportion import proportions_ztest


def simular_teste_ab(
    n_a: int,
    n_b: int,
    taxa_real_a: float,
    taxa_real_b: float,
    seed: int = 42,
) -> dict:
    rng = np.random.default_rng(seed)
    conversoes_a = rng.binomial(n_a, taxa_real_a)
    conversoes_b = rng.binomial(n_b, taxa_real_b)

    contagem = np.array([conversoes_a, conversoes_b])
    nobs = np.array([n_a, n_b])

    estatistica, p_valor = proportions_ztest(contagem, nobs)

    return {
        "conversoes_a": int(conversoes_a),
        "conversoes_b": int(conversoes_b),
        "taxa_a": conversoes_a / n_a,
        "taxa_b": conversoes_b / n_b,
        "estatistica_z": estatistica,
        "p_valor": p_valor,
        "significativo_5pct": bool(p_valor < 0.05),
    }


if __name__ == "__main__":
    # Exemplo: variante A (manchete atual) vs. variante B (manchete teste)
    resultado = simular_teste_ab(n_a=5000, n_b=5000, taxa_real_a=0.08, taxa_real_b=0.095)
    for chave, valor in resultado.items():
        print(f"{chave}: {valor}")
