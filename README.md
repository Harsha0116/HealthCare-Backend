# Healthcare Backend — Django REST API

A secure, production ready healthcare application backend built using Django, Django REST Framework (DRF), PostgreSQL with JWT authentication.

---

## Tech Stack

- **Framework**: Django + Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Auth**: JWT - `djangorestframework-simplejwt`
- **Python**: Latest Version

---

## Setup Instructions

### 1. Clone & Install

```bash
cd healthcare_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example 
# Edit .env with your actual values: SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
```

### 3. Create PostgreSQL Database

```bash
CREATE DATABASE healthcare_db;
USE healthcare_db
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Start Server

```bash
python manage.py runserver
```

API available at: `http://localhost:8000`

---

**NOTE - The ID here is used 'uuid' instead of Integer 'id' to securely handling the data.**

### Authentication

#### `POST /api/auth/register/`
Register a new user with name, email, and password.

---

#### `POST /api/auth/login/`
Log in a user and return a JWT token.

---

#### `POST /api/auth/token/refresh/`
Refresh the access token to proceed for operations

---

### Patients
> All endpoints will require `Authorization: Bearer <access_token>` header

#### `POST /api/patients/` — Add a new patient (Authenticated users only).

#### `GET /api/patients/` — Retrieve all patients created by the authenticated user.

#### `GET /api/patients/<uuid>/` — Get details of a specific patient.

#### `PUT /api/patients/<uuid>/` — Update patient details.

#### `DELETE /api/patients/<uuid>/` — Delete Patient

---

### Doctors
> All endpoints require authentication only creator can update or delete.

#### `POST /api/doctors/` — Add a new doctor (Authenticated users only).

#### `GET /api/doctors/` — Retrieve all doctors.

#### `GET /api/doctors/<uuid>/` — Get details of a specific doctor.

#### `PUT /api/doctors/<uuid>/` — Update doctor details.

#### `DELETE /api/doctors/<uuid>/` — Delete a doctor record.

---

### Patient-Doctor Mappings
> All endpoints require authentication.

#### `POST /api/mappings/` — Assign Doctor to Patient

#### `GET /api/mappings/` — Retrieve all patient-doctor mappings.

#### `GET /api/mappings/<patient_uuid>/` — Get all doctors assigned to a specific patient.

#### `DELETE /api/mappings/delete/<mapping_uuid>/` — Remove a doctor from a patient.

---

## Security Features

- JWT Access tokens expire after **1 hour**
- Refresh tokens expire after **7 days**
- Refresh token rotation + blacklisting enabled
- Patients are scoped to the authenticated user
- Doctor edit,delete restricted to the creator
- Password validation enforced on registration
- Environment variables for all sensitive config

---

## Postman Testing Workflow

1. **Register** → `POST /api/auth/register/`
2. **Login** → `POST /api/auth/login/` → copy `access` token
3. Set header: `Authorization: Bearer <access_token>` on all subsequent requests
4. **Create Doctor** → `POST /api/doctors/`
5. **Create Patient** → `POST /api/patients/`
6. **Assign Doctor** → `POST /api/mappings/` with `patient_id` and `doctor_id`
7. **View Assignments** → `GET /api/mappings/<patient_id>/`
