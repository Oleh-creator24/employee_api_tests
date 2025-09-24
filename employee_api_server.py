from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# "База данных" сотрудников в памяти
employees = [
    {"id": 1, "name": "Иван Иванов", "position": "Разработчик", "salary": 100000, "department": "IT"},
    {"id": 2, "name": "Петр Петров", "position": "Менеджер", "salary": 80000, "department": "Продажи"},
    {"id": 3, "name": "Мария Сидорова", "position": "Дизайнер", "salary": 90000, "department": "Дизайн"}
]

# Глобальная переменная для отслеживания следующего ID
next_id = 4


@app.route('/api/employees', methods=['GET'])
def get_employees():
    """Получить всех сотрудников"""
    return jsonify(employees)


@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Получить сотрудника по ID"""
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if employee:
        return jsonify(employee)
    return jsonify({"error": "Сотрудник не найден"}), 404


@app.route('/api/employees', methods=['POST'])
def create_employee():
    """Создать нового сотрудника"""
    global next_id

    data = request.get_json()

    # Проверка обязательных полей
    if not data or not data.get('name') or not data.get('position'):
        return jsonify({"error": "Обязательные поля: name, position"}), 400

    new_employee = {
        "id": next_id,
        "name": data['name'],
        "position": data['position'],
        "salary": data.get('salary', 0),
        "department": data.get('department', 'Не указан')
    }

    employees.append(new_employee)
    next_id += 1

    return jsonify(new_employee), 201


@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Обновить сотрудника"""
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({"error": "Сотрудник не найден"}), 404

    data = request.get_json()

    # Обновляем поля
    if 'name' in data:
        employee['name'] = data['name']
    if 'position' in data:
        employee['position'] = data['position']
    if 'salary' in data:
        employee['salary'] = data['salary']
    if 'department' in data:
        employee['department'] = data['department']

    return jsonify(employee)


@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Удалить сотрудника"""
    global employees
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if not employee:
        return jsonify({"error": "Сотрудник не найден"}), 404

    employees = [emp for emp in employees if emp['id'] != employee_id]
    return jsonify({"message": "Сотрудник удален"}), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка здоровья сервера"""
    return jsonify({"status": "healthy", "message": "Сервер работает"})


if __name__ == '__main__':
    print("🚀 Запуск сервера Employee API...")
    print("📍 API доступно по адресу: http://localhost:5000")
    print("📍 Эндпоинты:")
    print("   GET    /api/employees")
    print("   GET    /api/employees/<id>")
    print("   POST   /api/employees")
    print("   PUT    /api/employees/<id>")
    print("   DELETE /api/employees/<id>")
    print("   GET    /api/health")
    print("==================================================")

    app.run(debug=True, host='0.0.0.0', port=5000)