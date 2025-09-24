import requests
import json


def test_remote_api():
    """Тестирует удаленный API сервер"""
    base_url = "http://5.101.50.27:8000"

    print("🌐 ТЕСТИРОВАНИЕ УДАЛЕННОГО API")
    print("=" * 50)

    # Тестируем эндпоинты из investigate_api.py
    test_cases = [
        ("POST", "/employee/create", {
            "first_name": "Иван",
            "last_name": "Иванов",
            "company_id": 1,
            "position": "Разработчик"
        }),
        ("GET", "/employee/info", {"id": 1}),
        ("PATCH", "/employee/change", {
            "id": 1,
            "position": "Старший разработчик"
        })
    ]

    for method, endpoint, data in test_cases:
        url = f"{base_url}{endpoint}"
        print(f"\n{method} {endpoint}:")
        print(f"Data: {json.dumps(data, ensure_ascii=False)}")

        try:
            if method == "GET":
                response = requests.get(url, params=data)
            elif method == "POST":
                response = requests.post(url, json=data)
            elif method == "PATCH":
                response = requests.patch(url, json=data)

            print(f"Status: {response.status_code}")

            if response.status_code < 400:
                print("✅ Успех")
                if response.content:
                    try:
                        result = response.json()
                        print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
                    except:
                        print(f"Response: {response.text}")
            else:
                print("❌ Ошибка")
                print(f"Response: {response.text}")

        except Exception as e:
            print(f"❌ Исключение: {e}")


if __name__ == "__main__":
    test_remote_api()