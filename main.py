import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
from dotenv import load_dotenv
from agents import ExplorerAgent, CodeAnalyzerAgent, BusinessAnalystAgent, DocumentationAgent, TranslatorAgent

def print_header():
    """Prints a clean, professional header."""
    print("\n" + "="*70)
    print(" "*25 + "RADAR - Análise Técnica")
    print(" "*15 + "Repository Analysis & Documentation Automated Report")
    print("="*70 + "\n")

def print_section(title: str):
    """Prints a section header."""
    print(f"\n{'-'*70}")
    print(f" {title}")
    print(f"{'-'*70}\n")

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
    """
    Main orchestration script for RADAR.
    Generates standardized technical documentation for code repositories.
    """
    # 1. SETUP
    print_header()
    
    print("Esta ferramenta analisa e documenta seu repositório de código de forma automática.")
    print("O processo é otimizado e leva apenas alguns minutos.\n")

    # Verifica ambiente
    if not check_environment():
        print("\nConfigure o ambiente e tente novamente.")
        return

    # Instantiate agents
    explorer = ExplorerAgent()
    code_analyzer = CodeAnalyzerAgent()
    doc_agent = DocumentationAgent()
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        business_analyst = BusinessAnalystAgent(api_key=api_key)
        translator = TranslatorAgent(api_key=api_key)
    except ValueError as e:
        print(f"Erro: {e}. Verifique o arquivo .env.")
        return

    # Get target directory from user
    target_directory = input("Informe o caminho do repositório a ser analisado: ")
    if not os.path.isdir(target_directory):
        print(f"\nErro: Diretório '{target_directory}' não encontrado.")
        return

    try:
        # 2. SCAN FILES
        print_section("Fase 1: Varredura Inicial")
        print(f"Mapeando estrutura do repositório: '{target_directory}'")
        all_files_info = explorer.scan_directory(path=target_directory)
        if not all_files_info:
            print("\nNenhum arquivo de código encontrado para análise.")
            return
        print(f"✓ {len(all_files_info)} arquivos mapeados.")

        # 3. ANALYZE CODEBASE
        print_section("Fase 2: Análise Estrutural")
        print("Processando arquitetura e dependências...")
        codebase_analysis = code_analyzer.analyze_codebase(all_files_info)
        print("✓ Análise estrutural concluída.")
        
        # 4. GENERATE DOCUMENTATION
        print_section("Fase 3: Geração de Relatórios")
        
        # Generate main overview
        print("Elaborando visão geral do projeto...")
        overview = business_analyst.generate_overview(all_files_info, codebase_analysis)
        print("✓ Visão geral concluída.")
        
        # Analyze core files (top 20% by importance)
        print("\nAnalisando componentes principais...")
        core_files_analysis = {}
        core_files = all_files_info[:len(all_files_info)//5]  # Top 20%
        total_core = len(core_files)
        
        with ThreadPoolExecutor(max_workers=min(8, total_core)) as executor:
            future_to_file = {
                executor.submit(
                    business_analyst.analyze_core_file, 
                    file_info,
                    codebase_analysis
                ): file_info 
                for file_info in core_files
            }
            
            completed = 0
            for future in future_to_file:
                file_info = future_to_file[future]
                try:
                    completed += 1
                    progress = (completed / total_core) * 100
                    print(f"\rProgresso: {progress:.1f}% ({completed}/{total_core})", end="", flush=True)
                    
                    analysis = future.result()
                    core_files_analysis[file_info['relative_path']] = analysis
                except Exception as e:
                    print(f"\nFalha ao analisar {file_info['relative_path']}: {e}")
            print("\n✓ Análise dos componentes concluída.")

        # 5. TRANSLATE & SAVE DOCUMENTATION
        print_section("Fase 4: Tradução e Finalização")
        print("Traduzindo documentação para português...")
        radar_dir = doc_agent.save_documentation(
            overview=overview,
            core_files_analysis=core_files_analysis,
            base_dir=target_directory,
            translator=translator
        )
        print("✓ Tradução concluída.")
        
        print("\nProcesso concluído com sucesso!")
        print("\nDocumentação gerada em:")
        print(f"  {radar_dir}/")
        print("  ├─ VISAO_GERAL.md")
        print("  └─ componentes/")
        print("\nPróximos passos:")
        print("  1. Valide a documentação gerada")
        print("  2. Compartilhe com a equipe")
        print("  3. Atualize conforme necessário")
        print("\n" + "="*70)

    except Exception as e:
        print(f"\nErro inesperado: {e}")
        print("Entre em contato com o time de tecnologia.")

if __name__ == "__main__":
    main() 