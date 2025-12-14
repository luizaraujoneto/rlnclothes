import os
import logging
from waitress import serve
from rlnclothes.wsgi import application

if __name__ == '__main__':
    # Configuração de logs para exibir no console e salvar em arquivo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("waitress.log"),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger('waitress')
    
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Iniciando servidor Waitress na porta {port}...")
    
    serve(application, host='0.0.0.0', port=port)
