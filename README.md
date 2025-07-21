# R A D A R

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/castrocap/radar)
![GitHub](https://img.shields.io/github/license/castrocap/radar)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

</div>

## Sobre o Projeto

O RADAR é uma ferramenta desenvolvida pela Capitania Investimentos para análise e documentação automática de código. Usando inteligência artificial, ele mapeia, entende e documenta repositórios inteiros de forma rápida e precisa.

## Como Funciona

Nossa arquitetura é distribuída em camadas especializadas:

### Agente Principal

O cérebro do sistema que:
- Distribui recursos de processamento
- Coordena os agentes especializados
- Garante qualidade das entregas
- Gerencia processamento em paralelo

### Processamento Paralelo

**Explorador**
- Mapeia a estrutura do repositório
- Identifica componentes principais
- Detecta padrões de arquitetura

**Analisador de Código**
- Avalia sintaxe e semântica
- Identifica padrões técnicos
- Extrai métricas importantes

**Analisador de Dependências**
- Mapeia conexões entre componentes
- Avalia integrações
- Identifica pontos críticos

### Inteligência de Negócio

**Analista de Negócio**
- Entende o domínio
- Contextualiza funcionalidades
- Mapeia regras de negócio

**Analista de Arquitetura**
- Avalia design do sistema
- Analisa padrões
- Sugere melhorias

**Analista de Segurança**
- Avalia riscos
- Identifica pontos sensíveis
- Propõe melhorias

### Documentação

**Documentador Técnico**
- Gera documentação técnica
- Especifica componentes
- Documenta arquitetura

**Processador de Texto**
- Ajusta linguagem
- Mantém termos técnicos
- Garante consistência

**Integrador**
- Junta toda documentação
- Padroniza formato
- Controla versões

## Como Usar

### Requisitos
- Python 3.9+
- Chave da API Google Gemini

### Instalação

1. **Baixe o código**
```bash
git clone https://github.com/castrocap/radar.git
cd radar
```

2. **Configure o ambiente**
```bash
# Windows
install_guruenv.bat

# Linux/macOS
python -m venv guruenv
source guruenv/bin/activate
pip install -r requirements.txt
```

3. **Configure sua chave API**

a) Pegue sua chave:
   - Entre em https://makersuite.google.com/app/apikey
   - Faça login
   - Crie uma chave
   - Copie ela

b) Configure:
   - Crie um arquivo `.env`
   - Coloque sua chave:
     ```env
     GOOGLE_API_KEY=sua_chave_aqui
     ```

## Usando

1. **Rode o programa**
```bash
# Windows
radar.bat

# Linux/macOS
python main.py
```

2. **Analise seu código**
- Digite o caminho da pasta
- O RADAR vai criar uma pasta `RADAR/` com:
  - `VISAO_GERAL.md`: Resumo geral
  - `componentes/`: Detalhes técnicos

## O Que Você Recebe

### Visão Geral
- Resumo do sistema
- Como funciona
- Principais funções
- Como os dados fluem
- Partes importantes
- Tecnologias usadas

### Detalhes dos Componentes
- Para que serve
- Como se conecta
- Do que depende
- Como processa
- Pontos importantes

## Tecnologias

- **Base**: Python 3.9+
- **IA**: API Google Gemini
- **Performance**: ThreadPoolExecutor
- **Docs**: Markdown

## Arquivos Principais

- `main.py`: Programa principal
- `agents.py`: Nossos agentes
- `radar.bat`: Atalho Windows
- `.env`: Suas configurações
- `.env.example`: Exemplo
- `.gitignore`: Controle git

## Segurança

- Nunca compartilhe seu `.env`
- Proteja sua chave API
- Use o `.gitignore`
- Siga as práticas da empresa

## Direitos

Propriedade da Capitania Investimentos.

## Ajuda

Precisa de ajuda?
- Leia o manual acima
- Confira sua API
- Fale com o time de tecnologia

---

<div align="center">
Capitania Investimentos
</div> 