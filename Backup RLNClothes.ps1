$DateStr = Get-Date -UFormat '%Y-%m-%d_%H-%M-%S'
$BackupPath = "G:\Meu Drive\RLNClothes\Backup\backup-$DateStr.sql"

Echo "Inicio Backup: $DateStr"
Echo --------------------------------------------------------------------------------

Echo "Executando dump no container do banco de dados..."
docker exec rlnclothes_db pg_dump -U rlnclothesuser -d rlnclothesdb -F c --verbose -f /tmp/backup_temp.sql

Echo "Copiando arquivo de backup para o destino local..."
docker cp rlnclothes_db:/tmp/backup_temp.sql "$BackupPath"

Echo "Limpando arquivo temporário do container..."
docker exec rlnclothes_db rm /tmp/backup_temp.sql

Echo --------------------------------------------------------------------------------
$DateStrFim = Get-Date -UFormat '%Y-%m-%d_%H-%M-%S'
Echo "Fim Backup: $DateStrFim" 
Pause