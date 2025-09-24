import requests
import json


def debug_api():
    base_url = "http://5.101.50.27:8000"

    # Тестовые данные
    test_data = {
        "first_name": "Тестовый",
        "last_name": "Отладка",
        "company_id": 1,
        "email": "debug.test@company.com"
    }

    print("Отладка API сотрудников:")
    print("=" * 50)

    # Тест создания сотрудника
    print("1. Тест создания сотрудника:")
    response = requests.post(f"{base_url}/employee/create", json=test_data)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        try:
            data = response.json()
            print("JSON Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print("Response is not JSON")

    print("=" * 50)


if __name__ == "__main__":
    debug_api()