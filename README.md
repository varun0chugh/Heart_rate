A Flask-based backend system for managing patients and their heart rate data.

## Setup Instructions

### Prerequisites
- Python 3.9+
- pip package manager

### Installation
1. Clone the repository:
bash
git clone https://github.com/varun0chugh/heartrate-monitor.git
cd heartrate-monitor
2.Create and activate virtual environment:
3.Install dependencies:
4.Initialize database:
flask db init
flask db migrate
flask db upgrade
5/Run the application:

python run.py
The API will be available at http://localhost:5000

Endpoints
1. User Registration
URL: /register

Method: POST
2. User Login
URL: /login

Method: POST

Request Body: Same as registration

Success Response: Same as registration

3. Add Patient
URL: /patients

Method: POST
4. Get Patients
URL: /patients

Method: GET
5. Record Heart Rate
URL: /heart_rate

Method: POST
6. Get Heart Rate History
URL: /heart_rate/<patient_id>

Method: GET
Database Design
One-to-Many relationships:

User → Patients

Patient → HeartRate records

Used SQLite for simplicity (can be switched to PostgreSQL/MySQL via config)

Password hashing using Werkzeug security

Security
Basic email format validation (@ and . checks)

Password authentication through request body (not production-ready)

No SSL/TLS implementation

API Design
Credentials sent in request body for simplicity

No pagination implemented for large datasets

Timestamps automatically generated server-side

Validation
Basic data type checks

Mandatory fields validation

Ownership verification for resources
