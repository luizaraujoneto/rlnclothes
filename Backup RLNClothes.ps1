Echo "Inicio Backup: $(Get-Date -UFormat '%Y-%m-%d_%H-%M-%S')"
Echo --------------------------------------------------------------------------------
C:\PostgreSQL\15\bin\pg_dump.exe --dbname=postgresql://postgres:346954kg@127.0.0.1:5432/rlnclothesdb --format=c --blobs="rlnclothesdb"  --file="G:\\Meu Drive\\RLNClothes\\Backup\\backup-$(Get-Date -UFormat '%Y-%m-%d_%H-%M-%S').sql" --verbose 
Echo --------------------------------------------------------------------------------
Echo "Fim Backup: $(Get-Date -UFormat '%Y-%m-%d_%H-%M-%S')" 
Pause