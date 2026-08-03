# upgrading-ai-agentic
Configurations, Skills and MCPs IA Local



Adicionar nas configurações do VSCode (ctrl + shift + p):
````
"github.copilot.chat.mcp.enabled": true,
  "github.copilot.mcp.servers": {
    "mysql-local": {
      "command": "cmd.exe",
      "args": [
        "/c",
        "D:\\devEnv\\git_ai\\upgrading-ai-agentic\\scripts\\start-mysql-mcp.bat"
      ]
    }
  },
  "github.copilot.chat.customInstructions": [
    {
      "file": "D:\\devEnv\\git_ai\\upgrading-ai-agentic\\scripts\\search-skill-mysql.md"
    }
  ]

```