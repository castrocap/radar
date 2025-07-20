import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
from dotenv import load_dotenv
from agents import ExplorerAgent, CodeAnalyzerAgent, BusinessAnalystAgent, DocumentationAgent, TranslatorAgent

def print_header():
    print("\n" + "=" * 70)
    print("RADAR - Análise de Código".center(70))
    print("=" * 70 + "\n")
    print("Vamos analisar seu código e gerar uma documentação completa.")
    print("É rápido e fácil.\n")

def print_progress(phase, message, progress=None):
    if progress is None:
        print(f"→ {message}")
    else:
        print(f"→ {message} ({progress}%)")

def print_success(message):
    print(f"✓ {message}\n")

def print_phase(name):
    print("\n" + "-" * 70)
    print(f" {name} ".center(70, "-"))
    print("-" * 70 + "\n")

def print_completion(output_dir):
    print("\nPronto! Sua documentação está em:")
    print(f"  {output_dir}/")
    print("  ├─ VISAO_GERAL.md")
    print("  └─ componentes/\n")

def open_documentation(output_dir):
    """Abre os arquivos gerados na IDE preferencial"""
    import os
    import subprocess
    from pathlib import Path

    # Lista todos os arquivos markdown gerados
    docs_path = Path(output_dir)
    markdown_files = [
        str(docs_path / "VISAO_GERAL.md"),
        *[str(f) for f in (docs_path / "componentes").glob("*.md")]
    ]

    # Tenta abrir no Cursor primeiro
    try:
        for file in markdown_files:
            subprocess.run(["cursor", file], check=False)
        return
    except FileNotFoundError:
        pass

    # Tenta VS Code
    try:
        for file in markdown_files:
            subprocess.run(["code", file], check=False)
        return
    except FileNotFoundError:
        pass

    # Fallback para notepad no Windows
    if os.name == 'nt':
        for file in markdown_files:
            subprocess.run(["notepad", file], check=False)
    # Fallback para sistemas Unix-like
    else:
        for file in markdown_files:
            subprocess.run(["xdg-open", file], check=False)

def check_environment():
    """Verifica e valida o ambiente necessário."""
    print("Verificando ambiente...")
    
    # Verifica se .env existe
    if not os.path.exists('.env'):
        print("\nArquivo .env não encontrado!")
        print("1. Crie um arquivo .env na raiz do projeto")
        print("2. Adicione sua chave da API do Google Gemini:")
        print("   GOOGLE_API_KEY=sua_chave_aqui")
        print("\nPara obter uma chave:")
        print("1. Acesse https://makersuite.google.com/app/apikey")
        print("2. Faça login com sua conta Google")
        print("3. Crie uma nova chave de API")
        print("4. Copie a chave e adicione ao arquivo .env")
        return False
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica GOOGLE_API_KEY
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\nChave da API do Google Gemini não encontrada no arquivo .env!")
        print("Adicione sua chave usando o formato:")
        print("GOOGLE_API_KEY=sua_chave_aqui")
        return False
        
    if api_key.lower() in ['sua_chave_aqui', 'your_key_here', 'chave']:
        print("\nChave da API do Google Gemini não foi configurada!")
        print("Substitua o valor padrão pela sua chave real no arquivo .env")
        return False
    
    print("✓ Ambiente configurado corretamente.")
    return True

def main():
    print_header()
    
    # Verifica ambiente
    print("Verificando ambiente...")
    check_environment()
    print_success("Tudo certo!")

    # Pega caminho do repositório
    repo_path = input("Qual pasta você quer analisar? ")
    print()

    # Fase 1: Exploração
    print_phase("Explorando")
    explorer = ExplorerAgent()
    files = explorer.scan_directory(repo_path)
    print_success(f"Encontrei {len(files)} arquivos importantes")

    # Fase 2: Análise
    print_phase("Analisando")
    analyzer = CodeAnalyzerAgent()
    analysis = analyzer.analyze_codebase(files)
    print_success("Análise completa")

    # Fase 3: Documentação
    print_phase("Documentando")
    business = BusinessAnalystAgent()
    docs = business.generate_documentation(analysis)
    print_success("Documentação gerada")

    # Fase 4: Tradução
    print_phase("Finalizando")
    translator = TranslatorAgent()
    final_docs = translator.translate_documentation(docs)
    
    # Salva documentação
    doc_agent = DocumentationAgent()
    output_dir = doc_agent.save_documentation(final_docs, repo_path)
    print_success("Tudo pronto!")
    
    print_completion(output_dir)
    
    # Abre documentação na IDE
    print("Abrindo documentação...")
    open_documentation(output_dir)

if __name__ == "__main__":
    main() 