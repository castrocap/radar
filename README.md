# RADAR - Repository Analysis & Documentation Automated Report

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/castrocap/radar)
![GitHub](https://img.shields.io/github/license/castrocap/radar)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)

</div>

## 🎯 Visão Geral

O RADAR é uma ferramenta de análise e documentação automatizada desenvolvida para a Capitania Investimentos. Utilizando IA avançada (Google Gemini), ele analisa repositórios de código, gera documentação técnica padronizada e facilita a compreensão de projetos complexos.

<div align="center">

![RADAR Workflow](https://raw.githubusercontent.com/castrocap/radar/master/docs/images/workflow.png)

</div>

### ✨ Principais Funcionalidades

- 🔍 **Análise Automatizada**: Mapeia e analisa estrutura de código, dependências e padrões
- 📚 **Documentação Inteligente**: Gera documentação técnica usando IA (Google Gemini)
- 🌐 **Tradução Técnica**: Traduz automaticamente a documentação para português mantendo termos técnicos
- ⚡ **Processamento Paralelo**: Análise otimizada para grandes repositórios
- 📊 **Documentação Contextual**: Foco em componentes críticos e suas relações

## 🚀 Instalação

### Pré-requisitos
- Python 3.9+
- Chave de API do Google Gemini (instruções abaixo)

### Setup

1. **Clone o repositório**
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

3. **Configure a API do Google Gemini**

O RADAR utiliza a API do Google Gemini para análise e documentação. Para configurar:

a) **Obtenha uma chave de API**:
   - Acesse https://makersuite.google.com/app/apikey
   - Faça login com sua conta Google
   - Crie uma nova chave de API
   - Copie a chave gerada

b) **Configure o arquivo .env**:
   - Crie um arquivo `.env` na raiz do projeto
   - Adicione sua chave:
     ```env
     GOOGLE_API_KEY=sua_chave_aqui
     ```

**Nota**: O RADAR verificará automaticamente se a API está configurada corretamente antes de iniciar.

## 💻 Uso

1. **Execute o RADAR**
```bash
# Windows
radar.bat

# Linux/macOS
python main.py
```

2. **Informe o diretório**
- Digite o caminho completo do repositório a ser analisado
- O RADAR criará uma pasta `RADAR` dentro do diretório com:
  - `VISAO_GERAL.md`: Documentação geral do projeto
  - `componentes/`: Análises detalhadas dos arquivos principais

## 📖 Estrutura da Documentação

### VISAO_GERAL.md
- Visão geral do projeto
- Arquitetura e componentes
- Funcionalidade principal
- Fluxo de dados
- Arquivos principais
- Dependências e tecnologias

### Componentes
Análises detalhadas dos arquivos mais importantes, incluindo:
- Objetivo e responsabilidade
- Funções/componentes principais
- Dependências e interações
- Fluxo de dados
- Considerações importantes

## 🏗️ Arquitetura

O RADAR utiliza uma arquitetura de agentes especializados:

- **ExplorerAgent**: Mapeia e analisa estrutura de arquivos
- **CodeAnalyzerAgent**: Analisa código e extrai padrões
- **BusinessAnalystAgent**: Gera documentação usando IA
- **TranslatorAgent**: Traduz mantendo termos técnicos
- **DocumentationAgent**: Organiza e salva documentação

## 🛠️ Tecnologias

- **Python**: Linguagem principal
- **Google Gemini**: IA para análise e documentação
- **ThreadPoolExecutor**: Processamento paralelo
- **Markdown**: Formato de documentação

## 📁 Arquivos Importantes

- `main.py`: Script principal
- `agents.py`: Implementação dos agentes
- `radar.bat`: Script de execução para Windows
- `.env`: Configurações e chaves (não versionado)
- `.env.example`: Exemplo de configuração
- `.gitignore`: Controle de versionamento

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'feat: Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 🔒 Segurança

- **NÃO** commite o arquivo `.env` ou qualquer arquivo contendo chaves/tokens
- **NÃO** compartilhe sua chave da API do Google Gemini
- Use o `.gitignore` fornecido para proteger dados sensíveis

## ⚖️ Licença

Este projeto é proprietário da Capitania Investimentos.

## 💬 Suporte

Para suporte ou dúvidas:
- Verifique a documentação acima
- Certifique-se de que a API está configurada corretamente
- Entre em contato com o time de tecnologia da Capitania Investimentos

---

<div align="center">
Desenvolvido com ❤️ pela Capitania Investimentos
</div> 