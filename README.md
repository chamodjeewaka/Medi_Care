# MediConnect – A Digital Healthcare Management System

#### Video Demo: https://www.youtube.com/watch?v=8nlg9R6SCcI&t=2s
#### Description:

## Introduction

MediConnect is a web-based digital healthcare management system developed as my final project for Harvard University's CS50x – Introduction to Computer Science course.

The main purpose of MediConnect is to simplify the management of healthcare information and improve the interaction between doctors and patients through a centralized digital platform. Traditional healthcare environments often involve manually maintaining patient records, consultation details, and prescriptions. Managing these records can become difficult when information needs to be accessed or updated regularly.

MediConnect aims to address these challenges by providing a simple and user-friendly system where patients can access their medical information and doctors can manage consultations and maintain patient records digitally.

## User Management and Authentication

MediConnect provides separate authentication systems for patients and doctors to ensure that each user has access to the appropriate functionalities.

Patients can register for an account by providing the required information and subsequently log in using their credentials. Doctors have a separate login interface that allows them to access their dedicated dashboard.

The application uses Flask sessions to maintain user authentication and manage access to different sections of the system. Passwords are not stored as plain text. Instead, they are hashed using Werkzeug's password hashing functions to improve account security.

## Patient Features

After logging in, patients are directed to their personal dashboard, which provides access to the main features of the application.

Patients can:

- Create an account and log in securely.
- Browse the available doctors.
- View doctors' names, specializations, qualifications, and other relevant information.
- Access their personal dashboard.
- View their previous medical consultations.
- Review clinical descriptions and diagnoses recorded by doctors.
- View prescribed medicines and their corresponding instructions.
- Access their medical history in an organized format.

The medical history feature allows patients to review their previous consultations without having to rely entirely on manually maintained medical documents.

## Doctor Features

Doctors can access a separate dashboard through the doctor login system. The dashboard provides functionalities to manage patient consultations and medical records.

Doctors can:

- Log in through a dedicated doctor authentication interface.
- Access their personal dashboard.
- View patients who have previously consulted them.
- Search for patients and access relevant patient information.
- Review patients' previous medical records.
- Record new consultation details.
- Provide clinical descriptions and diagnoses.
- Create and save prescriptions for patients.

The doctor dashboard is designed to organize patient information and make consultation management more convenient.

## Consultation and Prescription Management

One of the main features of MediConnect is its consultation and prescription management system.

During a consultation, doctors can record relevant clinical information about a patient's condition. The consultation form allows doctors to enter a detailed clinical description and diagnosis.

Doctors can also prescribe multiple medicines for a single consultation. Each medicine can be recorded with the following information:

- Medicine name
- Dosage
- Frequency
- Duration
- Quantity

This approach allows each medicine to have its own prescription details rather than combining all medicines into a single text field.

Consultation details and prescriptions are stored in the database and associated with the relevant patient and doctor. This makes it possible to retrieve the records when reviewing a patient's medical history.

## Medical History Management

The medical history section allows patients to access their previous consultation records in one place.

Instead of displaying medical information as unorganized text, the application presents consultation details in a structured format.

Patients can review the doctor associated with a consultation, consultation dates, clinical descriptions, diagnoses, and prescribed medicines.

Doctors can also access relevant previous consultation records of their patients. This helps them understand the patient's previous medical information when managing subsequent consultations.

## Technologies Used

The application was developed using several technologies:

**Python:** Used as the primary programming language for implementing the application's backend logic, handling user requests, and processing data.

**Flask:** Used as the web application framework to manage application routes, authentication, form submissions, and communication between the frontend and backend.

**SQLite:** Used as the relational database management system to store user accounts, doctor information, patient information, consultations, and prescription records.

**CS50 SQL Library:** Used to interact with the SQLite database and execute SQL queries from the Flask application.

**HTML5:** Used to structure the web pages and application interfaces.

**CSS3:** Used to design the user interface, including dashboards, forms, navigation elements, and other visual components.

**Bootstrap:** Used to create responsive layouts and improve the overall user interface.

**JavaScript:** Used to implement additional frontend interactions and improve the user experience.

**Flask-Session:** Used to manage user sessions and maintain authentication states.

**Werkzeug:** Used for secure password hashing and password verification.

## Database Design

SQLite is used to maintain the application's data in a structured manner.

The database contains related records for users, doctors, patients, consultations, and prescriptions.

SQL queries are used to insert, retrieve, update, and manage information. Relationships between the records allow consultations and prescriptions to be associated with the correct patients and doctors.

The database design also allows multiple medicines to be associated with a single consultation, making prescription management more flexible.

## Security and Access Control

Security is an important consideration in MediConnect.

The application implements password hashing to avoid storing passwords in plain text. Session-based authentication is used to identify logged-in users and manage access to different application features.

Parameterized SQL queries are used to reduce the risk of SQL injection. Separate authentication and access-control logic is implemented for patient and doctor accounts.

## Design and User Interface

The application was designed with simplicity and usability in mind. Separate dashboards are provided for patients and doctors so that users can easily access the functionalities relevant to their roles.

The interface includes organized navigation, structured information displays, consultation forms, and prescription forms. CSS and Bootstrap are used to create a consistent visual design across the application.

## Learning Outcomes

Developing MediConnect provided an opportunity to apply the programming concepts and problem-solving techniques learned throughout CS50x to a practical application.

Through this project, I gained experience in:

- Developing web applications using Python and Flask.
- Designing and managing relational databases using SQLite.
- Writing SQL queries and working with database relationships.
- Implementing user registration and authentication.
- Managing sessions and controlling access to application features.
- Processing HTML forms and handling HTTP requests.
- Connecting frontend interfaces with backend functionality.
- Organizing application data and implementing CRUD operations.
- Designing user-friendly web interfaces.

This project also helped me understand how different technologies work together to develop a complete web-based application.

## Conclusion

MediConnect demonstrates how web technologies can be used to develop a centralized platform for managing basic healthcare information and doctor-patient interactions.

Although this application was developed as an academic project, it provided valuable practical experience in software development, database management, web technologies, and application security.

MediConnect represents my effort to combine the knowledge gained from CS50x with a practical problem-solving approach to develop a meaningful digital solution.
