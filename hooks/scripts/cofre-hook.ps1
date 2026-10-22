# Hook do Copilot (VS Code) para o protocolo cofre -> memoria -> cofre.
#   SessionStart: registra o inicio da sessao e injeta o lembrete do protocolo.
#   Stop: se nada foi gravado no cofre desde o inicio, pede uma vez por sessao
#         que o agente salve o que foi util (ou declare que nao ha nada).
param([Parameter(Mandatory)][ValidateSet('SessionStart', 'Stop')][string]$Event)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)

$Vault = 'C:\Users\Raf_F\Documents\obsidian\rfsprod'
$StateDir = Join-Path $env:TEMP 'copilot-cofre'
New-Item -ItemType Directory -Force $StateDir | Out-Null

$payload = @{}
try {
    $raw = [Console]::In.ReadToEnd()
    if ($raw.Trim()) { $payload = $raw | ConvertFrom-Json }
} catch { }

$session = if ($payload.session_id) { $payload.session_id -replace '[^\w\-]', '_' } else { 'sem-sessao' }
$startFile = Join-Path $StateDir "$session.start"
$askedFile = Join-Path $StateDir "$session.asked"

function Write-Json($obj) { $obj | ConvertTo-Json -Depth 5 -Compress | Write-Output }

if ($Event -eq 'SessionStart') {
    (Get-Date).ToUniversalTime().ToString('o') | Set-Content $startFile -Encoding UTF8
    # limpa estado de sessoes com mais de 7 dias
    Get-ChildItem $StateDir -File | Where-Object LastWriteTime -lt (Get-Date).AddDays(-7) | Remove-Item -Force

    $context = @(
        'Protocolo cofre-memoria ativo (instrucao cofre-memoria.instructions.md).',
        '1) Antes de agir, busque no cofre Obsidian com obsidian-vault/search_notes e read_notes.',
        '2) Se nao houver, busque em memory/search_nodes e memory-cht-reader.',
        '3) Ao terminar, salve o que for reutilizavel no cofre com cofre-fs (Dev Logs/, Knowledge/, Projects/) e registre em Logs/AAAA-MM-DD.md.'
    ) -join "`n"
    Write-Json @{ hookSpecificOutput = @{ hookEventName = 'SessionStart'; additionalContext = $context } }
    exit 0
}

# Stop
if ($payload.stop_hook_active -or (Test-Path $askedFile)) { Write-Json @{ continue = $true }; exit 0 }

$since = if (Test-Path $startFile) { [datetime]::Parse((Get-Content $startFile -Raw).Trim()).ToLocalTime() } else { (Get-Date).AddHours(-2) }
$savedToVault = Get-ChildItem $Vault -Recurse -File -Filter *.md -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notmatch '\\\.(obsidian|trash|claude)\\' -and $_.LastWriteTime -gt $since } |
    Select-Object -First 1

if ($savedToVault) { Write-Json @{ continue = $true }; exit 0 }

New-Item -ItemType File -Force $askedFile | Out-Null
Write-Json @{
    decision = 'block'
    reason   = 'Antes de encerrar: siga a etapa 3 do protocolo cofre-memoria. Se esta sessao produziu algo reutilizavel (decisao, causa raiz, solucao validada, comando ou configuracao que funcionou), salve no cofre com cofre-fs e registre em Logs/AAAA-MM-DD.md. Se nao houver nada util, responda apenas "Cofre: nada novo a salvar".'
}
exit 0
