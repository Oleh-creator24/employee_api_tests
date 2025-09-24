import sys
import pytest
import os
import json
from datetime import datetime


def main():
    print("Запуск тестов API сотрудников...")

    # Создаем директорию для отчетов, если ее нет
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    # Генерируем имя файла отчета с timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Используем JUnit XML отчет вместо HTML (более стабильный)
    xml_report = os.path.join(reports_dir, f"report_{timestamp}.xml")

    # Базовые аргументы pytest
    pytest_args = [
        "tests/",
        "-v",
        "--tb=short",
        "--base-url=http://5.101.50.27:8000",
        f"--junit-xml={xml_report}",
        "--disable-warnings"
    ]

    print(f"XML отчет будет сохранен в: {xml_report}")
    print(f"Команда: python -m pytest {' '.join(pytest_args)}")
    print("-" * 50)

    # Запускаем pytest
    exit_code = pytest.main(pytest_args)

    if exit_code == 0:
        print("✅ Все тесты прошли успешно!")
    else:
        print(f"❌ Некоторые тесты завершились с ошибкой. Код выхода: {exit_code}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())