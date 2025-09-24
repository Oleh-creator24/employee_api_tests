import subprocess
import sys
import time
import requests
from pathlib import Path
import os


def check_server_ready(url="http://localhost:8000", timeout=30):
    """Проверяет, готов ли сервер"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/docs", timeout=5)
            if response.status_code == 200:
                return True
        except:
            print(".", end="", flush=True)
            time.sleep(2)
    return False


def check_existing_server():
    """Проверяет, не запущен ли уже сервер на порту 8000"""
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Сервер уже запущен на http://localhost:8000")
            return True
    except:
        pass
    return False


def install_dependencies():
    """Устанавливает необходимые зависимости"""
    print("📦 Проверка зависимостей...")

    dependencies = ["fastapi", "uvicorn", "pydantic"]

    for dep in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep} установлен")
        except ImportError:
            print(f"❌ {dep} не установлен. Установка...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ {dep} успешно установлен")
            except subprocess.CalledProcessError:
                print(f"❌ Не удалось установить {dep}")


def run_employee_api():
    """Запускает Employee API из src/api/employee_api.py"""
    print("🚀 ЗАПУСК EMPLOYEE API")
    print("=" * 50)

    # Проверяем существование файла
    api_file = Path("src/api/employee_api.py")
    if not api_file.exists():
        print(f"❌ Файл {api_file} не найден!")
        return False

    print(f"✅ Найден файл приложения: {api_file}")

    # Проверяем зависимости
    install_dependencies()

    # Проверяем, не запущен ли уже сервер
    if check_existing_server():
        print("Сервер уже запущен!")
        return True

    # Запускаем сервер
    app_module = "src.api.employee_api:app"

    print(f"🔄 Запускаем: {app_module}")

    try:
        # Запускаем сервер
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            app_module,
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])

        print("\n⏳ Сервер запускается...")
        print("Проверяем готовность", end="")

        # Ждем пока сервер станет доступен
        if check_server_ready():
            print("\n✅ Сервер успешно запущен!")
            print("\n📚 Документация API:")
            print("   - Swagger UI: http://localhost:8000/docs")
            print("   - ReDoc:      http://localhost:8000/redoc")
            print("\n🔧 Основные эндпоинты:")
            print("   - Корневой:   http://localhost:8000/")
            print("   - Health:     http://localhost:8000/health")
            print("   - Сотрудники: http://localhost:8000/api/employees")
            print("\n⏹️  Для остановки сервера нажмите Ctrl+C")

            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Остановка сервера...")
                process.terminate()
                return True
        else:
            print("\n❌ Сервер не запустился за отведенное время")
            process.terminate()
            return False

    except FileNotFoundError:
        print("❌ uvicorn не установлен. Установите его: pip install uvicorn")
        return False
    except Exception as e:
        print(f"❌ Ошибка при запуске сервера: {e}")
        return False


if __name__ == "__main__":
    run_employee_api()