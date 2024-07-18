from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(150), nullable=False)
    company_api_key = db.Column(db.String(150), nullable=False, unique=True)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    location_name = db.Column(db.String(150), nullable=False)
    location_country = db.Column(db.String(150), nullable=False)
    location_city = db.Column(db.String(150), nullable=False)
    location_meta = db.Column(db.String(150), nullable=True)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    sensor_name = db.Column(db.String(150), nullable=False)
    sensor_category = db.Column(db.String(150), nullable=False)
    sensor_meta = db.Column(db.String(150), nullable=True)
    sensor_api_key = db.Column(db.String(150), nullable=False, unique=True)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

