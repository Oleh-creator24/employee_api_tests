import sys
import pytest
import os
from datetime import datetime


def main():
    print("Запуск тестов API сотрудников...")

    # Создаем директорию для отчетов, если ее нет
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Генерируем имя файла отчета с timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report = os.path.join(reports_dir, f"report_{timestamp}.html")

    # Базовые аргументы pytest
    pytest_args = [
        "tests/",
        "-v",
        "--tb=short",
        "--base-url=http://5.101.50.27:8000",
        f"--html={html_report}",
        "--self-contained-html"
    ]

    # Устанавливаем переменную окружения для кодировки
    os.environ['PYTHONIOENCODING'] = 'utf-8'

    print(f"HTML отчет будет сохранен в: {html_report}")
    print(f"Команда: python -m pytest {' '.join(pytest_args)}")
    print("-" * 50)

    # Запускаем pytest
    exit_code = pytest.main(pytest_args)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())