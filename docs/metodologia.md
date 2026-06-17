# Metodologia — G1 Pulse

Este documento existe para deixar claro, para qualquer recrutador ou revisor de código, o que é dado real e o que é dado simulado neste projeto.

## 1. Dados reais

- **Fonte:** feeds RSS públicos do G1, organizados por editoria (`https://g1.globo.com/rss/g1/<editoria>`).
- **Campos coletados:** título, link, editoria, data/hora de publicação, data/hora de coleta.
- **O que isso representa:** o volume e o ritmo real de publicação editorial do G1 por categoria, ao longo do período de coleta.
- **O que isso NÃO representa:** nenhuma métrica de audiência, tráfego ou comportamento de usuário — esses dados são internos da Globo e não são públicos.

## 2. Dados simulados

- **Pageviews, tempo na página, compartilhamentos:** gerados via distribuição normal, com média e desvio definidos por editoria em `src/synthetic/generate_engagement.py`.
- **Premissas usadas para calibrar os parâmetros:**
  - Editorias com maior volatilidade noticiosa (mundo, política) tendem a ter picos de tráfego maiores — premissa baseada em padrões genéricos e amplamente discutidos do setor de notícias digitais, não em dado proprietário de nenhuma empresa.
  - Horários de almoço e noite recebem multiplicador de tráfego, refletindo padrões conhecidos de consumo de notícia no Brasil.
  - Fins de semana têm volume reduzido.
- **Teste A/B:** as taxas de conversão das variantes A e B são definidas manualmente como parâmetro da simulação (não inferidas de nenhum dado real), e servem para demonstrar a metodologia de teste estatístico (z-test de proporções), não para representar uma campanha real do G1.

## 3. Por que essa abordagem

Métricas de audiência de produtos de mídia são dados proprietários e sensíveis — não faria sentido, nem seria honesto, fingir tê-las. A solução foi separar claramente o que pode ser coletado de fato (o ritmo editorial público) do que precisa ser modelado (o comportamento do usuário), documentando cada premissa para que o raciocínio analítico fique auditável.

## 4. Limitações

- O modelo de engajamento é simplificado e não captura efeitos reais como repercussão em redes sociais, picos de breaking news ou sazonalidade de longo prazo.
- O teste A/B é ilustrativo — não corresponde a nenhum experimento real do G1.
- O volume de dados é pequeno (escala de portfólio), não escala de produção.
