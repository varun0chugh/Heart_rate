from flask import jsonify

def validate_email(email):
    # Basic email validation
    if '@' not in email or '.' not in email:
        return False
    return True

def error_response(message, code=400):
    return jsonify({'error': message}), code