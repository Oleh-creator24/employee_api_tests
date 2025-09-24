import requests
import json


class EmployeeAPITester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.employees_url = f"{base_url}/api/employees"
        self.created_employee_id = None

    def check_server_health(self):
        """Проверка доступности сервера"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def print_test_result(self, test_name, success, response=None):
        """Вывод результата теста"""
        status = "✅ УСПЕХ" if success else "❌ ОШИБКА"
        print(f"{status} | {test_name}")

        if response is not None and not success:
            print(f"   Код статуса: {response.status_code}")
            if response.text:
                try:
                    error_data = response.json()
                    print(f"   Ошибка: {error_data}")
                except:
                    print(f"   Ответ: {response.text}")

    def test_get_all_employees(self):
        """Тест получения всех сотрудников"""
        response = requests.get(self.employees_url)
        success = response.status_code == 200

        if success:
            employees = response.json()
            print(f"   📊 Найдено сотрудников: {len(employees)}")

        self.print_test_result("GET Все сотрудники", success, response)
        return success

    def test_get_employee_by_id(self, employee_id=1):
        """Тест получения сотрудника по ID"""
        response = requests.get(f"{self.employees_url}/{employee_id}")
        success = response.status_code == 200

        if success:
            employee = response.json()
            print(f"   👤 Сотрудник: {employee['name']} ({employee['position']})")

        self.print_test_result(f"GET Сотрудник ID={employee_id}", success, response)
        return success

    def test_create_employee(self):
        """Тест создания нового сотрудника"""
        new_employee = {
            "name": "Алексей Тестов",
            "position": "Тестировщик",
            "salary": 75000,
            "department": "QA"
        }

        response = requests.post(self.employees_url, json=new_employee)
        success = response.status_code == 201

        if success:
            created_employee = response.json()
            self.created_employee_id = created_employee['id']
            print(f"   👤 Создан сотрудник ID={self.created_employee_id}")

        self.print_test_result("POST Создание сотрудника", success, response)
        return success

    def test_update_employee(self):
        """Тест обновления сотрудника"""
        if not self.created_employee_id:
            print("   ⚠️ Нет ID созданного сотрудника для теста обновления")
            return False

        updated_data = {
            "name": "Алексей Обновленный",
            "position": "Старший тестировщик",
            "salary": 85000
        }

        response = requests.put(
            f"{self.employees_url}/{self.created_employee_id}",
            json=updated_data
        )
        success = response.status_code == 200

        if success:
            updated_employee = response.json()
            print(f"   🔄 Обновлен: {updated_employee['name']}")

        self.print_test_result(f"PUT Обновление сотрудника ID={self.created_employee_id}", success, response)
        return success

    def test_delete_employee(self):
        """Тест удаления сотрудника"""
        if not self.created_employee_id:
            print("   ⚠️ Нет ID созданного сотрудника для теста удаления")
            return False

        response = requests.delete(f"{self.employees_url}/{self.created_employee_id}")
        success = response.status_code == 200

        if success:
            print(f"   🗑️ Удален сотрудник ID={self.created_employee_id}")

        self.print_test_result(f"DELETE Удаление сотрудника ID={self.created_employee_id}", success, response)
        return success

    def test_nonexistent_employee(self):
        """Тест запроса несуществующего сотрудника"""
        response = requests.get(f"{self.employees_url}/9999")
        success = response.status_code == 404

        self.print_test_result("GET Несуществующий сотрудник", success, response)
        return success

    def run_all_tests(self):
        """Запуск всех тестов"""
        print("🧪 ТЕСТИРОВАНИЕ ЛОКАЛЬНОГО EMPLOYEE API")
        print("=" * 50)

        # Проверка доступности сервера
        if not self.check_server_health():
            print("❌ Сервер не доступен. Запустите сервер сначала.")
            print("💡 Запустите: python simple_employee_api_server.py")
            return False

        print("✅ Сервер доступен. Начинаем тестирование...")
        print()

        # Запуск тестов в правильном порядке
        tests = [
            self.test_get_all_employees,
            self.test_get_employee_by_id,
            self.test_create_employee,
            self.test_update_employee,
            self.test_nonexistent_employee,
            self.test_delete_employee
        ]

        results = []
        for test in tests:
            result = test()
            results.append(result)
            print()

        # Статистика
        passed = sum(results)
        total = len(results)

        print("=" * 50)
        print(f"📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ: {passed}/{total} пройдено")

        if passed == total:
            print("🎉 Все тесты прошли успешно!")
        else:
            print("⚠️ Некоторые тесты не прошли")

        return passed == total


if __name__ == "__main__":
    tester = EmployeeAPITester()
    tester.run_all_tests()