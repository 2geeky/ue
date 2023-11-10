
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate
from dotenv import load_dotenv
import os

load_dotenv()  # Ładowanie zmiennych środowiskowych

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    age = db.Column(db.Integer)
    role = db.Column(db.String(50))

class UserSchema(ma.Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1))
    surname = fields.Str(required=True, validate=validate.Length(min=1))
    age = fields.Int(required=True, validate=validate.Range(min=0))
    role = fields.Str(required=True, validate=validate.Length(min=1))

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.get_json())
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_schema.dump(new_user)), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

# ... pozostałe endpointy CRUD z odpowiednią obsługą wyjątków i walidacją ...

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
