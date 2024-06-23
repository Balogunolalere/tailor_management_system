
# Tailor Management System

The Tailor Management System is a web application built with FastAPI to manage tailor-related activities such as user authentication, contact management, family management, measurement management, and user management. The system provides a set of API routes to perform CRUD operations and other functionalities.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Directory Structure](#directory-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication and authorization
- Contact management
- Family management
  - Add and remove family members
  - Retrieve family measurements
- Measurement management
  - Export measurements to PDF
  - Send measurements via email
- User management

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/balogunolalere/tailor_management_system.git
    cd tailor_management_system
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```


## Configuration

Configuration settings are defined in the `app/core/config.py` file. You can set the following environment variables:

- `PROJECT_NAME`: The name of the project.
- `API_V1_STR`: The API version string.
- `SECRET_KEY`: The secret key for JWT.
- `ALGORITHM`: The algorithm used for JWT.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: The expiration time for access tokens.
- `DATABASE_URL`: The database URL.
- `EMAIL_*`: Email server settings.

## Usage

To run the application, use the following command:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication

- `POST /api/v1/auth/login`: User login
- `POST /api/v1/auth/signup`: User signup
- `POST /api/v1/auth/refresh-token`: Refresh access token

### Contacts

- `GET /api/v1/contacts`: Get all contacts
- `POST /api/v1/contacts`: Create a new contact
- `GET /api/v1/contacts/{contact_id}`: Get a contact by ID
- `PUT /api/v1/contacts/{contact_id}`: Update a contact by ID
- `DELETE /api/v1/contacts/{contact_id}`: Delete a contact by ID

### Families

- `GET /api/v1/families`: Get all families
- `POST /api/v1/families`: Create a new family
- `GET /api/v1/families/{family_id}`: Get a family by ID
- `PUT /api/v1/families/{family_id}`: Update a family by ID
- `DELETE /api/v1/families/{family_id}`: Delete a family by ID
- `POST /api/v1/families/{family_id}/members`: Add a member to a family
- `DELETE /api/v1/families/{family_id}/members/{member_id}`: Remove a member from a family

### Measurements

- `GET /api/v1/measurements`: Get all measurements
- `POST /api/v1/measurements`: Create a new measurement
- `GET /api/v1/measurements/{measurement_id}`: Get a measurement by ID
- `PUT /api/v1/measurements/{measurement_id}`: Update a measurement by ID
- `DELETE /api/v1/measurements/{measurement_id}`: Delete a measurement by ID
- `POST /api/v1/measurements/{measurement_id}/export`: Export a measurement to PDF
- `POST /api/v1/measurements/{measurement_id}/send`: Send a measurement via email

### Users

- `GET /api/v1/users`: Get all users
- `POST /api/v1/users`: Create a new user
- `GET /api/v1/users/{user_id}`: Get a user by ID
- `PUT /api/v1/users/{user_id}`: Update a user by ID
- `DELETE /api/v1/users/{user_id}`: Delete a user by ID

## Directory Structure

```plaintext
tailor_management_system/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── contacts.py
│   │   ├── deps.py
│   │   ├── families.py
│   │   ├── measurements.py
│   │   ├── users.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   ├── crud/
│   │   ├── contact.py
│   │   ├── family.py
│   │   ├── measurement.py
│   │   ├── user.py
│   ├── models/
│   │   ├── contact.py
│   │   ├── family.py
│   │   ├── measurement.py
│   │   ├── user.py
│   ├── schemas/
│   │   ├── contact.py
│   │   ├── family.py
│   │   ├── measurement.py
│   │   ├── token.py
│   │   ├── user.py
│   ├── utils/
│   │   ├── email.py
│   │   ├── pdf_generator.py
│   ├── database.py
│   ├── main.py
├── requirements.txt
├── .env
├── README.md
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

Feel free to customize this README further based on any additional details or specific requirements you have for the project.