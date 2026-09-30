# Attendance Management System

A desktop attendance management system built with Python, PyQt5, and MySQL.

## Requirements

- Python 3.10+ recommended
- MySQL 8.x / compatible MariaDB
- Windows recommended for the desktop application

## Setup

1. Create a MySQL database named `attendance_system`.
2. Import the provided `attendance_system.sql` dump.
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Configure the database connection in the project's database configuration before running.
5. Start the application:

```bash
python main.py
```

## Notes

- The SQL dump may contain demo/admin data. Change default credentials before any real deployment.
- Do not commit real database passwords, API keys, or other secrets to a public repository.
- The application uses project-relative resource paths so its UI files can also be bundled with a packaged executable.
