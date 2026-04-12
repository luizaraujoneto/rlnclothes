# Script para parar o sistema com backup automático do banco de dados

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupFile = "backup_auto_$Timestamp.sql"

Write-Host "Iniciando backup automático do banco de dados..." -ForegroundColor Cyan

# Executa o dump do banco de dados logado no container
# Nota: Redirecionamento em PowerShell pode precisar de tratamento dependendo do encoding, usando --file ou similar se necessário
docker exec rlnclothes_db pg_dump -U rlnclothesuser rlnclothesdb > $BackupFile

if ($LASTEXITCODE -eq 0) {
    Write-Host "Backup concluído com sucesso: $BackupFile" -ForegroundColor Green
} else {
    Write-Host "ERRO ao realizar o backup. Verifique se os containers estão rodando." -ForegroundColor Red
}

Write-Host "Derrubando os containers..." -ForegroundColor Yellow
docker-compose down

Write-Host "Sistema parado." -ForegroundColor Cyan
