from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullName = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.fullName}>'

@app.before_first_request
def create_tables():
    db.create_all()

# Определите маршруты CRUD здесь...


# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'fullName' in data or not 'email' in data or not 'age' in data:
        abort(400, description="Invalid data")
    new_user = User(fullName=data['fullName'], email=data['email'], age=data['age'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": new_user.id}), 201

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'fullName': user.fullName,
        'email': user.email,
        'age': user.age
    } for user in users])

# Get a user by ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")
    return jsonify({
        'id': user.id,
        'fullName': user.fullName,
        'email': user.email,
        'age': user.age
    })

# Update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")
    data = request.get_json()
    if 'fullName' in data:
        user.fullName = data['fullName']
    if 'email' in data:
        user.email = data['email']
    if 'age' in data:
        user.age = data['age']
    db.session.commit()
    return jsonify({
        'id': user.id,
        'fullName': user.fullName,
        'email': user.email,
        'age': user.age
    })

# Delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found")
    db.session.delete(user)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
