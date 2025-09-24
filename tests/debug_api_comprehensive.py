import requests
import json
import os
from datetime import datetime


class EmployeeAPIDebugger:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.employees_url = f"{base_url}/employees"

    def print_separator(self, title):
        print(f"\n{'=' * 60}")
        print(f"{title}")
        print(f"{'=' * 60}")

    def test_connection(self):
        """Проверка соединения с API"""
        self.print_separator("1. ТЕСТ СОЕДИНЕНИЯ С API")
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print("✓ API доступен")
                return True
            else:
                print("✗ API недоступен")
                return False
        except requests.exceptions.ConnectionError:
            print("✗ Не удалось подключиться к API")
            return False

    def test_get_employees(self):
        """Тест получения списка сотрудников"""
        self.print_separator("2. ТЕСТ ПОЛУЧЕНИЯ СОТРУДНИКОВ")
        try:
            response = requests.get(self.employees_url)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")

            if response.status_code == 200:
                employees = response.json()
                print(f"Response: {json.dumps(employees, ensure_ascii=False, indent=2)}")
                print(f"✓ Успешно получено {len(employees)} сотрудников")
            else:
                print(f"Response: {response.text}")
                print("✗ Ошибка при получении сотрудников")

            return response.status_code == 200
        except Exception as e:
            print(f"✗ Исключение: {e}")
            return False

    def test_create_employee(self, employee_data=None):
        """Тест создания сотрудника с детальной диагностикой"""
        self.print_separator("3. ТЕСТ СОЗДАНИЯ СОТРУДНИКА")

        if employee_data is None:
            employee_data = {
                "name": "Иван Иванов",
                "position": "Разработчик",
                "department": "IT",
                "hire_date": "2024-01-15",
                "salary": 50000
            }

        print(f"Отправляемые данные: {json.dumps(employee_data, ensure_ascii=False, indent=2)}")

        try:
            response = requests.post(self.employees_url, json=employee_data)
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            print(f"Response: {response.text}")

            if response.status_code == 201:
                print("✓ Сотрудник успешно создан")
                return response.json()
            else:
                # Детальный анализ ошибки
                self.analyze_error(response, employee_data)
                return None

        except Exception as e:
            print(f"✗ Исключение при создании: {e}")
            return None

    def analyze_error(self, response, employee_data):
        """Анализ ошибки создания сотрудника"""
        print("\n--- АНАЛИЗ ОШИБКИ ---")

        # Проверка структуры данных
        required_fields = ["name", "position", "department", "hire_date", "salary"]
        missing_fields = [field for field in required_fields if field not in employee_data]
        if missing_fields:
            print(f"✗ Отсутствуют обязательные поля: {missing_fields}")

        # Проверка типов данных
        if not isinstance(employee_data.get("name"), str):
            print("✗ Поле 'name' должно быть строкой")
        if not isinstance(employee_data.get("position"), str):
            print("✗ Поле 'position' должно быть строкой")
        if not isinstance(employee_data.get("department"), str):
            print("✗ Поле 'department' должно быть строкой")
        if not isinstance(employee_data.get("salary"), (int, float)):
            print("✗ Поле 'salary' должно быть числом")

        # Попробуем разные форматы данных
        self.test_alternative_formats(employee_data)

    def test_alternative_formats(self, original_data):
        """Тестирование альтернативных форматов данных"""
        print("\n--- ТЕСТ АЛЬТЕРНАТИВНЫХ ФОРМАТОВ ---")

        # Тест с минимальными данными
        minimal_data = {
            "name": "Тест Тестов",
            "position": "Тестер",
            "department": "QA",
            "hire_date": "2024-01-01",
            "salary": 30000
        }

        print("Тест с минимальными данными:")
        self.test_create_employee(minimal_data)

        # Тест с разными форматами даты
        date_formats = [
            "2024-01-01",
            "2024-01-01T00:00:00",
            "01/01/2024"
        ]

        for date_format in date_formats:
            test_data = minimal_data.copy()
            test_data["hire_date"] = date_format
            print(f"\nТест с форматом даты: {date_format}")
            self.test_create_employee(test_data)

    def test_specific_endpoints(self):
        """Тестирование конкретных эндпоинтов"""
        self.print_separator("4. ТЕСТИРОВАНИЕ ЭНДПОИНТОВ")

        endpoints = [
            "/employees",
            "/docs",
            "/openapi.json",
            "/health"
        ]

        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            print(f"\nТестирование: {url}")
            try:
                response = requests.get(url)
                print(f"Status: {response.status_code}")
                if response.status_code != 200:
                    print(f"Response: {response.text[:200]}...")
            except Exception as e:
                print(f"Error: {e}")

    def run_comprehensive_test(self):
        """Запуск комплексного тестирования"""
        print("КОМПЛЕКСНАЯ ДИАГНОСТИКА API СОТРУДНИКОВ")
        print(f"Время начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Базовый URL: {self.base_url}")

        # Тест соединения
        if not self.test_connection():
            print("API недоступен. Проверьте:")
            print("1. Запущен ли сервер?")
            print("2. Правильный ли URL?")
            print("3. Нет ли проблем с сетью?")
            return

        # Тест эндпоинтов
        self.test_specific_endpoints()

        # Тест получения сотрудников
        self.test_get_employees()

        # Тест создания сотрудника
        self.test_create_employee()

        print("\n" + "=" * 60)
        print("ДИАГНОСТИКА ЗАВЕРШЕНА")
        print("=" * 60)


if __name__ == "__main__":
    # Можно указать другой URL если нужно
    debugger = EmployeeAPIDebugger()
    debugger.run_comprehensive_test()