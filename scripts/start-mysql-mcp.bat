@echo off
:: Navega para a raiz do projeto (uma pasta acima de onde o script estará, no .vscode)
cd /d "%~dp0.."

:: Se o arquivo .env existir, carrega as variáveis silenciosamente para a memória
if exist .env (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do set "%%A=%%B"
)

:: Executa o MCP montando a string de conexão com as variáveis carregadas
npx -y @modelcontextprotocol/server-mysql "mysql://%DB_USER%:%DB_PASSWORD%@%DB_HOST%:%DB_PORT%/%DB_DATABASE%"
