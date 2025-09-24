import sys
import subprocess
import os
from datetime import datetime


def main():
    print("Запуск тестов API сотрудников...")

    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(reports_dir, f"test_log_{timestamp}.txt")

    # Формируем команду
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--base-url=http://5.101.50.27:8000",
        "--disable-warnings"
    ]

    print(f"Команда: {' '.join(cmd)}")
    print(f"Лог будет сохранен в: {log_file}")
    print("-" * 50)

    # Запускаем через subprocess с правильной кодировкой
    with open(log_file, 'w', encoding='utf-8') as log:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )

        # Выводим вывод в реальном времени и сохраняем в файл
        for line in process.stdout:
            print(line, end='')
            log.write(line)
            log.flush()

        process.wait()
        exit_code = process.returncode

    print("-" * 50)
    if exit_code == 0:
        print("✅ Все тесты прошли успешно!")
    else:
        print(f"❌ Тесты завершились с ошибкой. Код: {exit_code}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())