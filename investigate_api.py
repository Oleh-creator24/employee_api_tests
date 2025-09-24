import requests
import json


def investigate_api():
    base_url = "http://5.101.50.27:8000"

    # 1. Попробуем создать сотрудника с минимальными данными
    print("=== Тест создания сотрудника ===")
    test_data = {
        "first_name": "Иван",
        "last_name": "Иванов",
        "company_id": 1,
        "position": "Разработчик"
    }

    response = requests.post(f"{base_url}/employee/create", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        employee_id = response.json().get('id')
        print(f"Created employee ID: {employee_id}")

        # 2. Попробуем получить информацию
        print("\n=== Тест получения информации ===")
        response_get = requests.get(f"{base_url}/employee/info", params={"id": employee_id})
        print(f"Status: {response_get.status_code}")
        print(f"Response: {response_get.text}")

        # 3. Попробуем обновить информацию
        print("\n=== Тест обновления информации ===")
        update_data = {
            "id": employee_id,
            "position": "Старший разработчик"
        }
        response_patch = requests.patch(f"{base_url}/employee/change", json=update_data)
        print(f"Status: {response_patch.status_code}")
        print(f"Response: {response_patch.text}")


if __name__ == "__main__":
    investigate_api()