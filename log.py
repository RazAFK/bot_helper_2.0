import logging
import os
import re
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(script_dir, "logs")
os.makedirs(logs_dir, exist_ok=True)

# Настройка логгера для информации (UTF-8)
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)
info_handler = logging.FileHandler(
    os.path.join(logs_dir, "info.log"), 
    encoding='utf-8'
)
info_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
info_logger.addHandler(info_handler)

# Настройка логгера для ошибок
error_logger = logging.getLogger('error_logger')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(
    os.path.join(logs_dir, "error.log"), 
    encoding='utf-8'
)
error_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - [%(error_type)s] %(message)s')
)
error_logger.addHandler(error_handler)

def extract_error_details(error):
    """Извлекает основное сообщение об ошибке и параметры из SQLAlchemy ошибки"""
    error_type = type(error).__name__
    error_msg = str(error)
    
    # Для SQLAlchemy ошибок
    if hasattr(error, 'orig'):
        # Извлекаем основное сообщение (до квадратных скобок)
        main_msg = error_msg.split('\n')[0].strip()
        
        # Ищем параметры в сообщении
        params_match = re.search(r'\[parameters: (.*?)\]', error_msg)
        params = params_match.group(1) if params_match else 'no parameters'
        
        return f"{main_msg} [params: {params}]"
    
    return error_msg

def log_error(error):
    """Логирует ошибку в сокращенном формате"""
    error_type = type(error).__name__
    error_details = extract_error_details(error)
    error_logger.error(
        error_details,
        extra={'error_type': error_type}
    )

def log_info(message):
    """Записывает сообщение в logs/info.log"""
    info_logger.info(message)