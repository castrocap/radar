# Code Oracle

O Code Oracle é uma ferramenta de diagnóstico e catalogação automatizada, projetada para analisar repositórios de código em ambientes corporativos. Ele utiliza um time de agentes de IA, construídos com o framework **Agno**, para realizar engenharia reversa do propósito de negócio a partir do código-fonte (Python, R, VBA, etc.) e gerar documentação clara e padronizada.

O objetivo é transformar diretórios de código, muitas vezes pouco documentados, em um "oráculo" de informações consultável, acessível tanto para equipes técnicas quanto para analistas de negócio.

## Funcionalidades

- **Exploração de Diretórios**: Um Agente Explorador mapeia recursivamente uma estrutura de pastas para identificar todos os arquivos de código.
- **Análise Técnica**: Um Agente Analista de Código extrai metadados, dependências e operações de I/O de cada script.
- **Análise de Negócio com IA**: Um Agente Analista de Negócio utiliza a API do Google Gemini para interpretar o código, gerando um resumo de alto nível sobre seu propósito.
- **Geração de Documentação**: Um Agente Documentador monta e salva um arquivo Markdown completo para cada script.
- **Catalogação Centralizada**: Todas as informações são salvas em um arquivo `catalog.csv` para fácil consulta.

## Tech Stack

- Python 3.9+
- Agno (agno-agi)
- Google Gemini API
- Pandas 