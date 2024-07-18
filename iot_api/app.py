from flask import Flask, request, jsonify, abort
from models import db, Admin, Company, Location, Sensor, SensorData
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/api/v1/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    company_name = data.get('company_name')
    company_api_key = str(uuid.uuid4())
    new_company = Company(company_name=company_name, company_api_key=company_api_key)
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'company_id': new_company.id, 'company_api_key': new_company.company_api_key}), 201

@app.route('/api/v1/locations', methods=['POST'])
def create_location():
    data = request.get_json()
    company_id = data.get('company_id')
    location_name = data.get('location_name')
    location_country = data.get('location_country')
    location_city = data.get('location_city')
    location_meta = data.get('location_meta')
    new_location = Location(
        company_id=company_id, location_name=location_name,
        location_country=location_country, location_city=location_city,
        location_meta=location_meta)
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'location_id': new_location.id}), 201

@app.route('/api/v1/sensors', methods=['POST'])
def create_sensor():
    data = request.get_json()
    location_id = data.get('location_id')
    sensor_name = data.get('sensor_name')
    sensor_category = data.get('sensor_category')
    sensor_meta = data.get('sensor_meta')
    sensor_api_key = str(uuid.uuid4())
    new_sensor = Sensor(
        location_id=location_id, sensor_name=sensor_name,
        sensor_category=sensor_category, sensor_meta=sensor_meta,
        sensor_api_key=sensor_api_key)
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify({'sensor_id': new_sensor.id, 'sensor_api_key': new_sensor.sensor_api_key}), 201

@app.route('/api/v1/sensor_data', methods=['POST'])
def create_sensor_data():
    data = request.get_json()
    sensor_api_key = data.get('api_key')
    sensor = Sensor.query.filter_by(sensor_api_key=sensor_api_key).first()
    if not sensor:
        abort(400, description="Invalid sensor API key")
    for entry in data['json_data']:
        timestamp = entry.get('timestamp')
        sensor_data = entry.get('data')
        new_data = SensorData(sensor_id=sensor.id, timestamp=timestamp, data=sensor_data)
        db.session.add(new_data)
    db.session.commit()
    return '', 201

@app.route('/api/v1/sensor_data', methods=['GET'])
def get_sensor_data():
    company_api_key = request.args.get('company_api_key')
    company = Company.query.filter_by(company_api_key=company_api_key).first()
    if not company:
        abort(400, description="Invalid company API key")
    from_timestamp = int(request.args.get('from'))
    to_timestamp = int(request.args.get('to'))
    sensor_ids = request.args.getlist('sensor_id')
    sensor_data = SensorData.query.filter(SensorData.sensor_id.in_(sensor_ids), SensorData.timestamp.between(from_timestamp, to_timestamp)).all()
    result = [{'sensor_id': data.sensor_id, 'timestamp': data.timestamp, 'data': data.data} for data in sensor_data]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

