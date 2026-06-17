-- Volume de publicações e pageviews simulados por editoria e dia
-- Tabela esperada: `{projeto}.g1_pulse.articles_engagement`

SELECT
  editoria,
  DATE(publicado_em) AS data_publicacao,
  COUNT(*) AS total_artigos,
  SUM(pageviews_simulado) AS pageviews_total_simulado
FROM `{projeto}.g1_pulse.articles_engagement`
GROUP BY editoria, data_publicacao
ORDER BY data_publicacao DESC, pageviews_total_simulado DESC;
