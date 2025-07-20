# RADAR - Repository Analysis & Documentation Automated Report

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/castrocap/radar)
![GitHub](https://img.shields.io/github/license/castrocap/radar)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

</div>

## Visão Geral

RADAR (Repository Analysis & Documentation Automated Report) é uma solução corporativa de análise e documentação automatizada desenvolvida para a Capitania Investimentos. Utilizando inteligência artificial avançada através da API Google Gemini, o sistema realiza análise profunda de repositórios de código, gerando documentação técnica padronizada e facilitando a compreensão de sistemas complexos.

## Arquitetura do Sistema

O RADAR implementa uma arquitetura distribuída e hierárquica, composta por camadas especializadas de processamento:

### Master Intelligence Agent

Componente central responsável por:
- Alocação dinâmica de recursos computacionais
- Orquestração de agentes especializados
- Validação e controle de qualidade
- Gestão de processamento paralelo

### Camada de Processamento Paralelo

**Repository Explorer**
- Análise estrutural do repositório
- Mapeamento de componentes
- Identificação de padrões arquiteturais

**Code Analyzer**
- Análise sintática e semântica
- Identificação de padrões técnicos
- Extração de métricas de código

**Dependency Analyzer**
- Mapeamento de dependências internas/externas
- Análise de integrações
- Avaliação de componentes críticos

### Camada de Inteligência de Negócio

**Business Intelligence**
- Análise de domínio
- Contextualização de negócio
- Identificação de regras de negócio

**Architecture Analyst**
- Avaliação de design de sistema
- Análise de padrões arquiteturais
- Recomendações de arquitetura

**Security Analyst**
- Avaliação de riscos
- Identificação de vulnerabilidades
- Recomendações de segurança

### Camada de Documentação

**Technical Writer**
- Geração de documentação técnica
- Especificações de sistema
- Documentação de arquitetura

**Language Processing**
- Tradução técnica para português
- Preservação de terminologia
- Consistência documental

**Documentation Integrator**
- Consolidação de documentação
- Formatação padronizada
- Controle de versão

## Instalação

### Pré-requisitos
- Python 3.9+
- Chave de API do Google Gemini

### Procedimento de Instalação

1. **Clone do Repositório**
```bash
git clone https://github.com/castrocap/radar.git
cd radar
```

2. **Configuração de Ambiente**
```bash
# Windows
install_guruenv.bat

# Linux/macOS
python -m venv guruenv
source guruenv/bin/activate
pip install -r requirements.txt
```

3. **Configuração da API Google Gemini**

a) Obtenção de Credenciais:
   - Acesse https://makersuite.google.com/app/apikey
   - Autentique-se com credenciais Google
   - Gere nova chave de API
   - Copie a chave gerada

b) Configuração Local:
   - Crie arquivo `.env` na raiz do projeto
   - Configure a chave:
     ```env
     GOOGLE_API_KEY=sua_chave_aqui
     ```

## Utilização

1. **Execução**
```bash
# Windows
radar.bat

# Linux/macOS
python main.py
```

2. **Análise de Repositório**
- Forneça o caminho completo do repositório alvo
- O sistema criará diretório `RADAR/` contendo:
  - `VISAO_GERAL.md`: Documentação geral
  - `componentes/`: Análises detalhadas

## Estrutura de Documentação

### Documentação Geral (VISAO_GERAL.md)
- Visão geral do sistema
- Arquitetura e componentes
- Funcionalidades principais
- Fluxos de dados
- Componentes críticos
- Stack tecnológico

### Documentação de Componentes
- Propósito e responsabilidades
- Interfaces e contratos
- Dependências e integrações
- Fluxos de processamento
- Considerações técnicas

## Tecnologias Utilizadas

- **Core**: Python 3.9+
- **IA**: Google Gemini API
- **Processamento**: ThreadPoolExecutor
- **Documentação**: Markdown

## Componentes do Sistema

- `main.py`: Módulo principal
- `agents.py`: Implementação de agentes
- `radar.bat`: Script de execução (Windows)
- `.env`: Configurações (não versionado)
- `.env.example`: Template de configuração
- `.gitignore`: Controle de versionamento

## Diretrizes de Segurança

- Não versionar arquivo `.env`
- Não compartilhar credenciais de API
- Utilizar `.gitignore` fornecido
- Seguir práticas de segurança corporativas

## Licença

Este software é propriedade da Capitania Investimentos.

## Suporte

Para suporte técnico:
- Consulte a documentação
- Verifique configuração da API
- Contate equipe de tecnologia da Capitania Investimentos

---

<div align="center">
Capitania Investimentos - Tecnologia
</div> 