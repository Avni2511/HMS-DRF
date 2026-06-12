# Hospital Management System

## Overview

Hospital Management System is a web-based healthcare platform that streamlines interactions between patients, doctors, and administrators. The system enables appointment scheduling, doctor availability management, prescription generation, email notifications, and AI-powered symptom analysis.

The goal of the project is to simplify healthcare management by providing a centralized platform where patients can book appointments, doctors can manage consultations, and administrators can oversee hospital operations.

---

## Features

### Patient Module

* User Registration and Login
* View Available Doctors
* Check Doctor Availability
* Book Appointments
* Receive Appointment Confirmation Emails
* View Appointment History
* View Prescriptions
* AI Symptom Checker

### Doctor Module

* Doctor Login
* Manage Appointments
* Approve or Cancel Appointments
* Add Prescriptions for Patients
* Set Availability Schedule

### Admin Module

* Manage Doctors
* Monitor Appointments
* Manage System Users

### AI Symptom Checker

* Accepts patient symptoms
* Suggests possible health conditions
* Provides basic precautions and recommendations
* Includes fallback logic when AI API is unavailable

---

## Project Workflow

1. Patient registers and logs into the system.
2. Patient views available doctors and their schedules.
3. Patient books an appointment.
4. Appointment confirmation email is sent automatically.
5. Doctor reviews appointment requests.
6. Doctor approves or cancels appointments.
7. Doctor adds prescriptions after consultation.
8. Patient views prescriptions from the dashboard.
9. Patient can use the AI Symptom Checker for preliminary health guidance.

---

## Technology Stack

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Backend

* Python
* Django

### Database

* SQLite

### AI Integration

* Google Gemini API
* Rule-Based Fallback Symptom Analysis

### Email Service

* Gmail SMTP

---

## Database Models

* User
* Patient
* Doctor
* Doctor Availability
* Appointment
* Prescription

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Hospital-Management-System
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Start Server

```bash
python manage.py runserver
```

---

## Future Enhancements

* Online Video Consultation
* Medical Records Management
* Laboratory Report Upload
* Medicine Recommendation System
* Advanced AI Diagnosis Support
* Payment Gateway Integration

---

## Author

Avni Gupta

---

## License

This project is developed for educational and academic purposes.
