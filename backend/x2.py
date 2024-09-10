from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Инициализация приложения Flask
app = Flask(__name__)

# Настройка URL базы данных (в данном случае используется SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
# Отключение отслеживания изменений в базе данных (опционально, для улучшения производительности)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# Определение модели (таблицы) под названием 'Contact'
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Первичный ключ (автоматически увеличивающийся идентификатор)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Поле для email (уникальное и обязательное)
    age = db.Column(db.Integer, nullable=False)  # Поле для возраста (обязательное)
    fullName = db.Column(db.String(80), nullable=False)  # Поле для полного имени (обязательное)

    def __repr__(self):
        return f'<Contact {self.fullName}>'  # Определяет строковое представление объекта Contact

# Маршрут для добавления нового контакта
@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.json  # Получение данных из тела запроса (в формате JSON)
    # Создание нового контакта с данными из запроса
    new_contact = Contact(email=data['email'], age=data['age'], fullName=data['fullName'])
    db.session.add(new_contact)  # Добавление нового контакта в сессию базы данных
    db.session.commit()  # Сохранение изменений в базе данных
    return jsonify({"message": "Contact added successfully!"}), 201  # Возвращение сообщения об успешном добавлении

# Маршрут для получения всех контактов
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()  # Получение всех контактов из базы данных
    # Возвращение списка контактов в формате JSON
    return jsonify([{'id': contact.id, 'email': contact.email, 'age': contact.age, 'fullName': contact.fullName} for contact in contacts])

# Маршрут для получения конкретного контакта по идентификатору
@app.route('/contact/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)  # Поиск контакта по идентификатору
    if contact:
        # Возвращение данных контакта в формате JSON, если контакт найден
        return jsonify({'id': contact.id, 'email': contact.email, 'age': contact.age, 'fullName': contact.fullName})
    else:
        # Возвращение сообщения об ошибке, если контакт не найден
        return jsonify({"message": "Contact not found!"}), 404

# Маршрут для обновления конкретного контакта по идентификатору
@app.route('/contact/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.json  # Получение данных из тела запроса (в формате JSON)
    contact = Contact.query.get(id)  # Поиск контакта по идентификатору
    if contact:
        # Обновление полей контакта с новыми данными из запроса (если они предоставлены)
        contact.email = data.get('email', contact.email)
        contact.age = data.get('age', contact.age)
        contact.fullName = data.get('fullName', contact.fullName)
        db.session.commit()  # Сохранение изменений в базе данных
        return jsonify({'message': 'Contact updated successfully!'})  # Возвращение сообщения об успешном обновлении
    else:
        # Возвращение сообщения об ошибке, если контакт не найден
        return jsonify({"message": "Contact not found!"}), 404

# Маршрут для удаления конкретного контакта по идентификатору
@app.route('/contact/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)  # Поиск контакта по идентификатору
    if contact:
        db.session.delete(contact)  # Удаление контакта из базы данных
        db.session.commit()  # Сохранение изменений в базе данных
        return jsonify({'message': 'Contact deleted successfully!'})  # Возвращение сообщения об успешном удалении
    else:
        # Возвращение сообщения об ошибке, если контакт не найден
        return jsonify({"message": "Contact not found!"}), 404

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание всех таблиц в базе данных (если они еще не существуют)
    app.run(debug=True)  # Запуск сервера в режиме отладки
