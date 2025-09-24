class TestData:
    """Класс с тестовыми данными для сотрудников"""

    @staticmethod
    def get_valid_employee_data():
        return {
            "first_name": "Иван",
            "last_name": "Иванов",
            "company_id": 1,
            "position": "Разработчик",
            "department": "IT",
            "salary": 100000,
            "email": "ivan.ivanov@company.com",
            "phone": "+79161234567"
        }

    @staticmethod
    def get_minimal_employee_data():
        return {
            "first_name": "Петр",
            "last_name": "Петров",
            "company_id": 1,
            "position": "Тестировщик"
        }

    @staticmethod
    def get_invalid_employee_data():
        return {
            "first_name": "",  # Пустое имя
            "last_name": "",  # Пустая фамилия
            "company_id": -1,  # Невалидный ID компании
            "position": ""  # Пустая должность
        }

    @staticmethod
    def get_updated_employee_data():
        return {
            "first_name": "Иван",
            "last_name": "Сидоров",
            "position": "Старший разработчик",
            "salary": 120000
        }

    @staticmethod
    def get_edge_case_data():
        """Данные для граничных случаев"""
        return [
            {
                "first_name": "A" * 50,
                "last_name": "Тестов",
                "company_id": 1,
                "position": "Должность"
            },
            {
                "first_name": "Тест",
                "last_name": "A" * 50,
                "company_id": 1,
                "position": "Должность"
            },
        ]