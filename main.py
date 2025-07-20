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
    """Verifica se o ambiente está configurado corretamente"""
    # Carrega variáveis de ambiente do .env
    load_dotenv()
    
    # Verifica chave da API
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\n❌ Chave da API Google não encontrada!")
        print("   1. Crie um arquivo .env na pasta do projeto")
        print("   2. Adicione sua chave: GOOGLE_API_KEY=sua_chave_aqui")
        print("   3. Rode o programa novamente")
        return False
    return True

def main():
    print_header()
    
    # Verifica ambiente
    print("Verificando ambiente...")
    if not check_environment():
        return
    print_success("Tudo certo!")

    # Pega caminho do repositório
    repo_path = input("Qual pasta você quer analisar? ")
    print()

    try:
        # Inicializa agentes
        api_key = os.getenv("GOOGLE_API_KEY")
        explorer = ExplorerAgent()
        analyzer = CodeAnalyzerAgent()
        doc_agent = DocumentationAgent()

        # Fase 1: Exploração
        print_phase("Explorando")
        files = explorer.scan_directory(repo_path)
        print_success(f"Encontrei {len(files)} arquivos importantes")

        # Fase 2: Análise
        print_phase("Analisando")
        analysis = analyzer.analyze_codebase(files)
        print_success("Análise completa")

        # Fase 3: Documentação
        print_phase("Documentando")
        business = BusinessAnalystAgent(api_key=api_key)
        docs = business.generate_overview(analysis)
        print_success("Documentação gerada")

        # Fase 4: Tradução
        print_phase("Finalizando")
        translator = TranslatorAgent(api_key=api_key)
        final_docs = translator.translate_documentation(docs)
        
        # Salva documentação
        output_dir = doc_agent.save_documentation(final_docs, repo_path)
        print_success("Tudo pronto!")
        
        print_completion(output_dir)
        
        # Abre documentação na IDE
        print("Abrindo documentação...")
        open_documentation(output_dir)

    except Exception as e:
        print(f"\n❌ Ops! Algo deu errado: {str(e)}")
        print("   Se o problema persistir, fale com o time de tecnologia.")
        return

if __name__ == "__main__":
    main() 