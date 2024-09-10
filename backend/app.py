from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__)


# Configure the database URL (using SQLite in this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to disable track modifications


# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Define a model (table) called 'Contact'
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    fullName = db.Column(db.String(80), nullable=False)


    def __repr__(self):
        return f'<Contact {self.fullName}>'




# Route to add a new contact
@app.route('/add_contact', methods=['POST'])
def add_contact():
    data = request.json
    new_contact = Contact(email=data['email'], age=data['age'], fullName=data['fullName'])
    db.session.add(new_contact)
    db.session.commit()
    return jsonify({"message": "Contact added successfully!"}), 201


# Route to get all contacts
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([{'id': contact.id, 'email': contact.email, 'age': contact.age, 'fullName': contact.fullName} for contact in contacts])


# Route to get a specific contact by id
@app.route('/contact/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id) # select * from xxx where
    if contact:
        return jsonify({'id': contact.id, 'email': contact.email, 'age': contact.age, 'fullName': contact.fullName})
    else:
        return jsonify({"message": "Contact not found!"}), 404


# Route to update a specific contact by id
@app.route('/contact/<int:id>', methods=['PUT'])
def update_contact(id):
    data = request.json
    contact = Contact.query.get(id)
    if contact:
        contact.email = data.get('email', contact.email)
        contact.age = data.get('age', contact.age)
        contact.fullName = data.get('fullName', contact.fullName)
        db.session.commit()
        return jsonify({'message': 'Contact updated successfully!'})
    else:
        return jsonify({"message": "Contact not found!"}), 404


# Route to delete a specific contact by id
@app.route('/contact/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if contact:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully!'})
    else:
        return jsonify({"message": "Contact not found!"}), 404


# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
       
    app.run(debug=True)
