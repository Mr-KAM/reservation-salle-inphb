# Room Reservation System

A Flask-based web application for managing room reservations. This system allows users to browse available rooms, request reservations, and view their reservation status. Administrators can manage rooms and approve or reject reservation requests.

## Features

- **User Authentication**: Register, login, and user profiles
- **Room Management**: Browse, view, and reserve rooms
- **Reservation System**: Request, track, and manage room reservations
- **Admin Dashboard**: Manage rooms and handle reservation requests
- **Responsive Design**: Works on desktop and mobile devices

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: SQLite
- **Frontend**: Tailwind CSS, Daisy UI
- **JavaScript**: Vanilla JS for interactive features

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd room-reservation-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python run.py
   ```

5. Access the application at `http://localhost:5000`

## Default Admin Account

The system creates a default admin account on first run:
- Email: admin@example.com
- Password: admin123

*Note: Change these credentials in a production environment.*

## Project Structure

```
room-reservation-system/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # Route handlers
│   ├── forms/           # Form definitions
│   ├── templates/       # HTML templates
│   ├── static/          # Static files (CSS, JS)
│   └── __init__.py      # Application factory
├── requirements.txt     # Project dependencies
└── run.py              # Application entry point
```

## Usage

### Regular Users

1. Register for an account or log in
2. Browse available rooms
3. View room details
4. Request a room reservation
5. Check reservation status in your profile

### Administrators

1. Log in with admin credentials
2. Access the admin dashboard
3. Manage rooms (add, edit, delete)
4. Review and process reservation requests
5. View all reservations in the system

## License

This project is licensed under the MIT License - see the LICENSE file for details.
