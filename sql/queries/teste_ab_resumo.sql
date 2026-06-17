-- Resumo dos resultados do teste A/B
-- Preencher após exportar os resultados de src/analysis/ab_test.py
-- para uma tabela `ab_test_results` no mesmo dataset.

SELECT *
FROM `{projeto}.pulso_editorial.ab_test_results`
ORDER BY executado_em DESC;
