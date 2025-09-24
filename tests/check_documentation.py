import requests
import json


def check_api_documentation():
    """Проверка документации API"""
    base_url = "http://localhost:8000/api"

    print("ПРОВЕРКА ДОКУМЕНТАЦИИ API")
    print("=" * 50)

    # Проверка Swagger документации
    endpoints_to_check = [
        ("Swagger UI", "/docs"),
        ("ReDoc", "/redoc"),
        ("OpenAPI Schema", "/openapi.json"),
        ("JSON Schema", "/employees/schema")
    ]

    for name, endpoint in endpoints_to_check:
        url = f"{base_url}{endpoint}"
        print(f"\n{name}: {url}")

        try:
            response = requests.get(url)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                print("✓ Доступен")
                if endpoint == "/openapi.json":
                    # Парсим OpenAPI спецификацию
                    try:
                        spec = response.json()
                        print(f"OpenAPI версия: {spec.get('openapi', 'N/A')}")
                        print(f"Заголовок: {spec.get('info', {}).get('title', 'N/A')}")
                        print(f"Версия API: {spec.get('info', {}).get('version', 'N/A')}")

                        # Показываем доступные endpoints
                        paths = spec.get('paths', {})
                        print(f"\nДоступные endpoints ({len(paths)}):")
                        for path, methods in paths.items():
                            print(f"  {path}: {list(methods.keys())}")

                    except json.JSONDecodeError:
                        print("✗ Невалидный JSON")
            else:
                print("✗ Недоступен")

        except requests.exceptions.ConnectionError:
            print("✗ Не удалось подключиться")
        except Exception as e:
            print(f"✗ Ошибка: {e}")


if __name__ == "__main__":
    check_api_documentation()