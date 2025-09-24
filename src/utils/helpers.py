import time
import requests
from typing import Dict, Any


def measure_response_time(func, *args, **kwargs) -> float:
    """Измеряет время выполнения функции"""
    start_time = time.time()
    func(*args, **kwargs)
    end_time = time.time()
    return end_time - start_time


def is_valid_json(response: requests.Response) -> bool:
    """Проверяет, является ли ответ валидным JSON"""
    try:
        response.json()
        return True
    except ValueError:
        return False


def validate_employee_structure(employee_data: Dict[str, Any]) -> bool:
    """Проверяет структуру данных сотрудника"""
    required_fields = ['id', 'name', 'position']
    return all(field in employee_data for field in required_fields)