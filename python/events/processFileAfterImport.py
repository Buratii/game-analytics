import os
import time
from utils.logger import setup_logger

logger = setup_logger()


def process_file_after_import(file_path: str, success: bool):
    try:
        processed_dir = os.path.join(os.path.dirname(file_path), "processed")
        error_dir = os.path.join(os.path.dirname(file_path), "error")
        
        for directory in [processed_dir, error_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
        
        target_dir = processed_dir if success else error_dir
        file_name = os.path.basename(file_path)
        
        timestamp = time.strftime("%Y%m%d%H%M%S")
        new_file_name = f"{os.path.splitext(file_name)[0]}_{timestamp}{os.path.splitext(file_name)[1]}"
        target_path = os.path.join(target_dir, new_file_name)
        
        os.rename(file_path, target_path)
        
        logger.info(f"Arquivo movido para: {target_path}")
        
    except Exception as e:
        logger.error(f"Erro ao processar arquivo após importação: {e}")