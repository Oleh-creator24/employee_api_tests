import requests
from requests import Response
import time
from typing import Dict, Any, Optional


class EmployeeAPIClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        # Добавляем заголовки для JSON
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def create_employee(self, employee_data: Dict[str, Any]) -> Response:
        url = f"{self.base_url}/employee/create"
        try:
            return self.session.post(url, json=employee_data, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise Exception("Timeout при создании сотрудника")

    def get_employee_info(self, employee_id: int) -> Response:
        url = f"{self.base_url}/employee/info"
        params = {"employee_id": employee_id}
        try:
            return self.session.get(url, params=params, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise Exception("Timeout при получении информации о сотруднике")

    def update_employee(self, employee_data: Dict[str, Any]) -> Response:
        url = f"{self.base_url}/employee/update"
        try:
            return self.session.put(url, json=employee_data, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise Exception("Timeout при обновлении сотрудника")