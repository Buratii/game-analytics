import json
from utils.logger import setup_logger

logger = setup_logger()

def load_events_from_file(file_path: str) -> list:
    try:
        with open(file_path, "r") as f:
            events = json.load(f)
            logger.info(f"{len(events)} eventos carregados do arquivo {file_path}")
            return events
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo {file_path}: {e}")
        return []
