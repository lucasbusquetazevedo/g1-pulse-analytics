-- Engajamento simulado médio por hora de publicação
-- Útil para identificar os horários de "pico" simulados no modelo

SELECT
  hora_publicacao,
  ROUND(AVG(pageviews_simulado), 0) AS media_pageviews,
  ROUND(AVG(tempo_pagina_seg_simulado), 1) AS media_tempo_pagina_seg
FROM `{projeto}.g1_pulse.articles_engagement`
GROUP BY hora_publicacao
ORDER BY hora_publicacao;
