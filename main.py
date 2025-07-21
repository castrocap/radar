import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
from dotenv import load_dotenv
from agents import ExplorerAgent, CodeAnalyzerAgent, BusinessAnalystAgent, DocumentationAgent, TranslatorAgent

def print_header():
    print("\n" + "═" * 70)
    print("RADAR - Análise Inteligente de Código".center(70))
    print("═" * 70 + "\n")
    print("Transformando seu código em documentação clara e objetiva.".center(70))
    print("Powered by Google Gemini".center(70) + "\n")

def print_progress(phase, message, progress=None):
    if progress is None:
        print(f"→ {message}")
    else:
        bar_length = 40
        filled = int(progress * bar_length / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"\r→ {message} [{bar}] {progress:.1f}%", end="", flush=True)

def print_success(message):
    print(f"\n✓ {message}")

def print_phase(name):
    print("\n" + "─" * 70)
    print(f" {name} ".center(70, "─"))
    print("─" * 70 + "\n")

def print_completion(output_dir):
    print("\n" + "═" * 70)
    print(" Documentação Gerada com Sucesso! ".center(70))
    print("═" * 70 + "\n")
    print(f"📁 Diretório: {output_dir}/")
    print("   ├─ VISAO_GERAL.md  - Resumo e estrutura do projeto")
    print("   └─ componentes/    - Análise detalhada dos arquivos\n")

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
    if not check_environment():
        return

    # Pega caminho do repositório
    repo_path = input("\n📂 Digite o caminho do projeto para análise: ")
    print()

    try:
        # Inicializa agentes
        api_key = os.getenv("GOOGLE_API_KEY")
        explorer = ExplorerAgent()
        analyzer = CodeAnalyzerAgent()
        business = BusinessAnalystAgent(api_key=api_key)
        translator = TranslatorAgent(api_key=api_key)
        doc_agent = DocumentationAgent()

        # Fase 1: Exploração
        print_phase("Mapeando Estrutura")
        files = explorer.scan_directory(repo_path)
        print_success(f"Identificados {len(files)} arquivos relevantes")

        # Fase 2: Análise
        print_phase("Analisando Código")
        analysis = analyzer.analyze_codebase(files)
        print_success("Análise técnica concluída")

        # Fase 3: Documentação
        print_phase("Gerando Documentação")
        
        # Gera visão geral
        overview = business.generate_overview(files, analysis)
        
        # Analisa arquivos principais (top 20%)
        print("Processando componentes principais...")
        core_files = {}
        total_core = len(files) // 5  # Top 20%
        for i, file_info in enumerate(files[:total_core]):
            progress = ((i + 1) / total_core) * 100
            print_progress("Analisando", f"Arquivo {i+1}/{total_core}", progress)
            
            try:
                file_analysis = business.analyze_core_file(file_info, analysis)
                translated = translator.translate_documentation(file_analysis)
                core_files[file_info["relative_path"]] = translated
            except Exception as e:
                print(f"\nErro ao analisar {file_info['relative_path']}: {e}")
        
        print("\n✓ Análise dos componentes concluída")

        # Traduz e salva
        overview_pt = translator.translate_documentation(overview)
        output_dir = doc_agent.save_documentation(
            overview=overview_pt,
            core_files_analysis=core_files,
            base_dir=repo_path
        )
        
        print_completion(output_dir)
        
        # Abre documentação na IDE
        try:
            open_documentation(output_dir)
            print("✓ Documentação aberta no seu editor")
        except Exception as e:
            print(f"\n⚠️ Não foi possível abrir automaticamente: {output_dir}")

    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        print("   Por favor, entre em contato com o time de tecnologia.")
        return

if __name__ == "__main__":
    main() 