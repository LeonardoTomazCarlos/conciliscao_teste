# Script para corrigir autenticação das APIs
$content = Get-Content "app.py" -Raw

# Substituir todas as ocorrências de @login_required em rotas de API
$pattern = "(@app\.route\('/api/[^']+.*\), methods=\[[^\]]+\])\)\s*\r?\n@login_required"
$replacement = '$1)' + "`r`n" + '@api_login_required'

$content = $content -replace $pattern, $replacement

# Salvar o arquivo modificado
$content | Set-Content "app.py" -NoNewline

Write-Host "Substituição concluída!"
