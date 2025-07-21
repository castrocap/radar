import os
import re
from typing import List, Dict, Any
import google.generativeai as genai
from agno.agent import Agent
from agno.tools import tool

class ExplorerAgent(Agent):
    def scan_directory(self, path: str) -> List[Dict[str, Any]]:
        """
        Scans a directory recursively and returns a list of files with their metadata.
        Only includes files with text-based extensions or that can be read as text.
        Ignores common non-project directories.
        """
        file_inventory = []
        text_extensions = {'.py', '.r', '.R', '.txt', '.md', '.csv', '.json', '.vba', 
                         '.sql', '.js', '.ts', '.html', '.css', '.yaml', '.yml', 
                         '.ini', '.cfg', '.conf', '.sh', '.bat', '.ps1'}
        
        # Directories to ignore (expanded)
        ignore_dirs = {
            # Ambiente virtual e cache
            '.venv', 'venv', 'env', 'guruenv', '__pycache__', 
            # Dependências e builds
            'node_modules', 'dist', 'build', 'site-packages',
            # Controle de versão e IDEs
            '.git', '.idea', '.vscode', '.hg', '.svn',
            # Diretórios específicos do RADAR
            'RADAR', 'output',
            # Diretórios de teste e documentação
            'tests', 'test', 'docs', 'documentation',
            # Diretórios de cache e temporários
            '.pytest_cache', '.mypy_cache', '.coverage', 'tmp', 'temp'
        }

        # Arquivos para ignorar
        ignore_files = {
            # Arquivos de ambiente e configuração
            '.env', '.env.example', 'pyvenv.cfg',
            # Arquivos de dependência
            'requirements.txt', 'package.json', 'package-lock.json',
            # Arquivos de IDE e editor
            '.editorconfig', '.gitignore', '.gitattributes',
            # Arquivos de cache
            '.DS_Store', 'Thumbs.db',
            # Arquivos de log
            '*.log', '*.pyc', '*.pyo', '*.pyd'
        }

        if not os.path.isdir(path):
            raise ValueError(f"Path '{path}' is not a valid directory.")

        total_files = sum([len(files) for _, _, files in os.walk(path)])
        processed_files = 0

        for root, dirs, files in os.walk(path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
            
            for file in files:
                # Ignora arquivos específicos
                if file in ignore_files or any(file.endswith(pat.replace('*', '')) for pat in ignore_files if '*' in pat):
                    continue

                processed_files += 1
                if processed_files % 10 == 0:  # Update progress every 10 files
                    progress = (processed_files / total_files) * 100
                    print(f"\rScanning files... {progress:.1f}% ({processed_files}/{total_files})", end="", flush=True)

                file_path = os.path.join(root, file)
                extension = os.path.splitext(file)[1]
                if extension.lower() in text_extensions:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        # Calculate file importance based on size, imports and complexity
                        importance_score = len(content.splitlines())
                        if extension.lower() in ['.py', '.r', '.js', '.ts']:
                            # More weight for source code files
                            importance_score *= 2
                            # Check for imports/dependencies
                            if 'import ' in content or 'require' in content:
                                importance_score *= 1.5
                            
                        file_inventory.append({
                            "path": file_path,
                            "file_name": file,
                            "extension": extension,
                            "content": content,
                            "importance_score": importance_score,
                            "relative_path": os.path.relpath(file_path, path)
                        })
                    except Exception as e:
                        print(f"\nCould not process file {file_path}: {e}")

        print("\nScan complete!")
        return sorted(file_inventory, key=lambda x: x['importance_score'], reverse=True)

class CodeAnalyzerAgent(Agent):
    def analyze_codebase(self, files_info: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyzes the entire codebase to extract relationships and patterns."""
        analysis = {
            "core_files": [],
            "dependencies": {},
            "file_groups": {},
            "data_flow": [],
            "tech_stack": set()
        }
        
        # Identify core files (top 20% by importance)
        core_threshold = len(files_info) // 5
        analysis["core_files"] = [
            f['relative_path'] for f in files_info[:core_threshold]
        ]
        
        # Analyze dependencies and relationships
        for file_info in files_info:
            content = file_info['content']
            ext = file_info['extension'].lower()
            path = file_info['relative_path']
            
            # Group by technology/purpose
            if ext == '.py':
                deps = re.findall(r'^(?:from\s+([\w\.]+)|import\s+([\w\.]+))', content, re.MULTILINE)
                analysis["dependencies"][path] = sorted(list(set([d[0] or d[1] for d in deps])))
                analysis["tech_stack"].add("Python")
                
                # Identify file purpose
                if 'flask' in content.lower():
                    self._add_to_group(analysis, "Web API", path)
                elif 'model' in content.lower():
                    self._add_to_group(analysis, "Data Models", path)
                elif 'test' in path.lower():
                    self._add_to_group(analysis, "Tests", path)
                    
            elif ext == '.r':
                analysis["tech_stack"].add("R")
                libs = re.findall(r'library\((.*?)\)', content)
                analysis["dependencies"][path] = libs
                
            elif ext in ['.js', '.ts']:
                analysis["tech_stack"].add("JavaScript/TypeScript")
                if 'react' in content.lower():
                    self._add_to_group(analysis, "Frontend Components", path)
                    
            # Track data flow
            io_patterns = {
                'read': r'read|load|import|fetch',
                'write': r'write|save|export|create'
            }
            for operation, pattern in io_patterns.items():
                if re.search(pattern, content, re.I):
                    analysis["data_flow"].append({
                        "file": path,
                        "operation": operation
                    })
        
        return analysis
    
    def _add_to_group(self, analysis: Dict[str, Any], group: str, path: str):
        """Helper to add a file to a group."""
        if group not in analysis["file_groups"]:
            analysis["file_groups"][group] = []
        analysis["file_groups"][group].append(path)

class BusinessAnalystAgent(Agent):
    def __init__(self, api_key: str):
        super().__init__()
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is required for BusinessAnalystAgent.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')
        with open('prompts/business_analyst_prompt.md', 'r', encoding='utf-8') as f:
            self.prompt_template = f.read()

    def generate_overview(self, files_info: List[Dict[str, Any]], codebase_analysis: Dict[str, Any]) -> str:
        """Generates a high-level overview of the entire codebase."""
        overview_prompt = f"""
        You are a senior technical analyst documenting a codebase. Generate a clear, comprehensive overview
        based on the following analysis:

        CORE FILES:
        {codebase_analysis['core_files']}

        TECHNOLOGY STACK:
        {list(codebase_analysis['tech_stack'])}

        FILE GROUPS:
        {codebase_analysis['file_groups']}

        DATA FLOW:
        {codebase_analysis['data_flow']}

        Generate a markdown document that includes:
        1. Project Overview
        2. Architecture & Components
        3. Core Functionality
        4. Data Flow
        5. Key Files (with brief descriptions)
        6. Dependencies & Tech Stack
        """
        
        try:
            response = self.model.generate_content(overview_prompt)
            return response.text
        except Exception as e:
            return f"# Analysis Failed\n\nError generating overview: {e}"

    def analyze_core_file(self, file_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Generates detailed analysis for an important file."""
        file_prompt = f"""
        Analyze this source code file in the context of the larger project:

        FILE: {file_info['relative_path']}
        
        CONTENT:
        {file_info['content']}

        PROJECT CONTEXT:
        - Tech Stack: {list(context['tech_stack'])}
        - Related Files: {[f for f in context['dependencies'].get(file_info['relative_path'], [])]}
        - File Group: {next((g for g, files in context['file_groups'].items() if file_info['relative_path'] in files), 'Other')}

        Generate a detailed markdown document that includes:
        1. Purpose & Responsibility
        2. Key Functions/Components
        3. Dependencies & Interactions
        4. Data Flow
        5. Important Considerations
        """
        
        try:
            response = self.model.generate_content(file_prompt)
            return response.text
        except Exception as e:
            return f"# Analysis Failed\n\nError analyzing {file_info['file_name']}: {e}"

class TranslatorAgent(Agent):
    def __init__(self, api_key: str):
        super().__init__()
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is required for TranslatorAgent.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def translate_documentation(self, content: str) -> str:
        """
        Translates documentation to Portuguese while preserving technical terms.
        """
        translation_prompt = f"""
        Traduza o seguinte documento técnico para português brasileiro.
        
        REGRAS IMPORTANTES:
        1. NÃO traduza:
           - Nomes de funções, variáveis, classes
           - Comandos e sintaxe de código
           - Nomes de tecnologias (ex: Python, JavaScript)
           - Nomes de bibliotecas e frameworks
           - Paths e URLs
        
        2. MANTENHA:
           - Toda a formatação Markdown
           - Estrutura de títulos e seções
           - Indentação e espaçamento
           - Links e referências
        
        3. TRADUZA:
           - Explicações e descrições
           - Títulos de seções
           - Comentários
           - Instruções e observações
        
        DOCUMENTO:
        {content}
        """
        
        try:
            response = self.model.generate_content(translation_prompt)
            return response.text
        except Exception as e:
            print(f"\nErro ao traduzir documento: {e}")
            return content  # Retorna original em caso de erro

class DocumentationAgent(Agent):
    def save_documentation(self, overview: str, core_files_analysis: Dict[str, str], base_dir: str, translator: TranslatorAgent = None) -> str:
        """Saves the generated documentation in a RADAR folder inside the analyzed directory."""
        # Create RADAR directory inside the analyzed directory
        radar_dir = os.path.join(base_dir, "RADAR")
        if not os.path.exists(radar_dir):
            os.makedirs(radar_dir)
            
        # Translate and save main overview
        if translator:
            overview = translator.translate_documentation(overview)
        overview_path = os.path.join(radar_dir, "VISAO_GERAL.md")
        with open(overview_path, 'w', encoding='utf-8') as f:
            f.write(overview)
            
        # Save core files documentation
        componentes_dir = os.path.join(radar_dir, "componentes")
        if not os.path.exists(componentes_dir):
            os.makedirs(componentes_dir)
            
        for file_path, analysis in core_files_analysis.items():
            if translator:
                analysis = translator.translate_documentation(analysis)
            safe_name = os.path.basename(file_path).replace('/', '_')
            doc_path = os.path.join(componentes_dir, f"{safe_name}.md")
            with open(doc_path, 'w', encoding='utf-8') as f:
                f.write(analysis)
                
        return radar_dir 