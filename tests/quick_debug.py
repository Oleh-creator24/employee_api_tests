import requests
import json


def quick_debug():
    """Быстрая диагностика проблемы"""
    url = "http://localhost:8000/api/employees"

    print("БЫСТРАЯ ДИАГНОСТИКА СОЗДАНИЯ СОТРУДНИКА")
    print("=" * 50)

    # Тестовые данные
    test_data = {
        "name": "Тест Тестов",
        "position": "Тестер",
        "department": "QA",
        "hire_date": "2024-01-01",
        "salary": 30000
    }

    print(f"URL: {url}")
    print(f"Данные: {json.dumps(test_data, ensure_ascii=False)}")

    try:
        response = requests.post(url, json=test_data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")

        # Дополнительная информация
        print(f"\nRequest Headers: {response.request.headers}")
        print(f"Request Body: {response.request.body}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    quick_debug()