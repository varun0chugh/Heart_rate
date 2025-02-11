from flask import Blueprint, request, jsonify
from app import db, ma
from app.models import User, Patient, HeartRate
from app.utils import validate_email, error_response

main_bp = Blueprint('main', __name__)

# Schemas
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email')

class PatientSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'gender')

class HeartRateSchema(ma.Schema):
    class Meta:
        fields = ('id', 'value', 'timestamp')

user_schema = UserSchema()
patients_schema = PatientSchema(many=True)
heart_rate_schema = HeartRateSchema(many=True)

@main_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return error_response('Missing email or password')
    
    if not validate_email(data['email']):
        return error_response('Invalid email format')
    
    if User.query.filter_by(email=data['email']).first():
        return error_response('Email already registered')
    
    user = User(email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user_schema.dump(user)), 201

@main_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data.get('email')).first()
    
    if not user or not user.check_password(data.get('password')):
        return error_response('Invalid credentials', 401)
    
    return jsonify(user_schema.dump(user))

@main_bp.route('/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return error_response('Authentication failed', 401)
    
    if not data.get('name'):
        return error_response('Name is required')
    
    patient = Patient(
        user_id=user.id,
        name=data['name'],
        age=data.get('age'),
        gender=data.get('gender')
    )
    db.session.add(patient)
    db.session.commit()
    
    return jsonify(PatientSchema().dump(patient)), 201

@main_bp.route('/patients', methods=['GET'])
def get_patients():
    data = request.get_json()
    
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return error_response('Authentication failed', 401)
    
    patients = Patient.query.filter_by(user_id=user.id).all()
    return jsonify(patients_schema.dump(patients))

@main_bp.route('/heart_rate', methods=['POST'])
def add_heart_rate():
    data = request.get_json()
    
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return error_response('Authentication failed', 401)
    
    patient = Patient.query.get(data.get('patient_id'))
    if not patient or patient.user_id != user.id:
        return error_response('Invalid patient', 404)
    
    if not data.get('value') or not isinstance(data['value'], int):
        return error_response('Valid heart rate value required')
    
    hr = HeartRate(patient_id=patient.id, value=data['value'])
    db.session.add(hr)
    db.session.commit()
    
    return jsonify({'message': 'Heart rate recorded'}), 201

@main_bp.route('/heart_rate/<int:patient_id>', methods=['GET'])
def get_heart_rates(patient_id):
    data = request.get_json()
    
    user = User.query.filter_by(email=data.get('email')).first()
    if not user or not user.check_password(data.get('password')):
        return error_response('Authentication failed', 401)
    
    patient = Patient.query.get(patient_id)
    if not patient or patient.user_id != user.id:
        return error_response('Patient not found', 404)
    
    rates = HeartRate.query.filter_by(patient_id=patient_id).all()
    return jsonify(heart_rate_schema.dump(rates))