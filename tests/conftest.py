import pytest
from src.api.employee_api import EmployeeAPIClient

def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="http://5.101.50.27:8000",
        help="Base URL for the API"
    )

@pytest.fixture
def api_client(request):
    base_url = request.config.getoption("--base-url")
    client = EmployeeAPIClient(base_url=base_url)
    yield client
    # При необходимости добавьте очистку после тестов

@pytest.fixture
def created_employee_id(api_client):
    # Фикстура для создания тестового сотрудника и возврата его ID
    employee_data = {
        "first_name": "Тестовый",
        "last_name": "Сотрудник",
        "company_id": 1,
        "email": "test.employee@company.com"
    }
    response = api_client.create_employee(employee_data)
    if response.status_code == 200:
        employee_id = response.json().get('id')
        yield employee_id
        # Здесь можно добавить удаление сотрудника после теста
    else:
        pytest.skip(f"Не удалось создать тестового сотрудника: {response.text}")