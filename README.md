# Back End Developer Exercise

A simple Django application that demonstrates data manipulation and database performance by managing task assignments for workers.

This project was built as a coding challenge to demonstrate back-end proficiency by modeling a task-assignment system in Django. The goal was to process and expose data about workers, tasks, and positions into a frontend-friendly format.

---

## 📑 Table of Contents

1. [Project Description](#project-description)
2. [Tech Stack](#tech-stack)
3. [Setup and Installation](#setup-and-installation)
4. [Database Configuration](#database-configuration)
5. [Usage](#usage)
6. [API Endpoint](#api-endpoint)
7. [Testing](#testing)
8. [Project Structure](#project-structure)
9. [Future Improvements](#future-improvements)
10. [Author](#author)

---

## 📌 Project Description

This Django app stores data about the assignment of tasks to workers. It demonstrates:

- Data model design and loading data from JSON files:
  - `positions.json`
  - `workers.json`
  - `tasks.json`
  - `assignments.json`
- Exposing an API endpoint that delivers data pre-processed for frontend rendering, such as in the following table format:

| Name       | 11 Jan | 12 Jan |
| ---------- | ------ | ------ |
| Position 1 | 7      | 10     |
| Worker 1   | 3      | 8      |
| Worker 2   | 4      | 2      |
| Position 2 | 5      | 0      |
| Worker 3   | 5      | 0      |

- Optional enhancements include:
  - Handling unassigned tasks and workers without positions
  - Writing automated tests for the endpoint
  - Implementing logic to auto-assign tasks based on capacity and position


## 🛠 Tech Stack

- **Python 3.10**
- **Django 5.2.4**
- **PostgreSQL 17**
- **HTML/CSS**
- **Django REST Framework**
- **Psycopg**
- **React**

## 🚀 Setup and Installation

Follow these steps using **PowerShell** in **Visual Studio Code 1.102.1**:

### 1. Clone the Repository

```powershell
git clone https://github.com/Lukeyone/BE-Exercise.git

```

### 2. Change PowerShell Execution Policy

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

```

### 3. Create and Activate Virtual Environment

```powershell
python -m venv be_exercise
.\be_exercise\Scripts\activate

```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt

```

----------

## 🛢 Database Configuration

### 1. Install PostgreSQL

Ensure **PostgreSQL 17** is installed. During setup, set the port to **5433**.

### 2. Create Database and User

Open PostgreSQL via command line:

```powershell
psql -U postgres -p 5433

```

> Or if needed:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -p 5433

```

Then run the following commands:

```sql
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

\c mydatabase

GRANT ALL PRIVILEGES ON SCHEMA public TO myuser;
GRANT USAGE, CREATE ON SCHEMA public TO myuser;

```

### 3. Update Django Settings

Edit `settings.py` or `.env`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}

```


## ▶️ Usage

Once setup is complete:

```powershell
# Run migrations
python manage.py migrate

# Load JSON data into database
python manage.py load_data

# Create admin user
python manage.py createsuperuser

# Start development server
python manage.py runserver

```

Then visit the following URLs:

-   **Human-readable table view:** [http://localhost:8000/](http://localhost:8000/)
    
-   **JSON API output:** [http://localhost:8000/api/table/](http://localhost:8000/api/table/)
    
-   **Django REST framework view:** [http://localhost:8000/api/new_table/](http://localhost:8000/api/new_table/)
    


## 🔗 API Endpoint

-   `/api/table/` – Raw JSON data suitable for frontend use
    
-   `/api/new_table/` – Formatted output using Django REST framework
    
-   `/` – Human-readable HTML table view
   
### 📦 Sample JSON Output (`/api/table/`)

```json
[
  {
    "name": "Position 1",
    "2024-01-11": 7,
    "2024-01-12": 10
  },
  {
    "name": "Worker 1",
    "2024-01-11": 3,
    "2024-01-12": 8
  }
]
```
The keys are dynamic date strings. Each dictionary in the array corresponds to a position or worker. The numbers indicate total task duration (in hours) on that day.
## 🧪 Testing

To run all tests:

```powershell
python manage.py test

```
The project includes unit tests covering:
- Task auto-assignment logic
- Table endpoint structure
- KPI calculations
- Edge cases: unassigned tasks, empty positions

Fixtures simulate real-world inputs. Each test module focuses on one concern to ensure maintainability and clarity.

## ✨ Enhancements Implemented

This project includes several optional enhancements beyond the base requirements to demonstrate thoughtful backend design, business-aware logic, and practical Django skills.

### ✅ 1. **Auto-Assignment of Tasks to Workers**

Implemented via a custom management command:

```bash
python manage.py auto_assign_tasks
```

**What it does:**

* Clears all existing task assignments.
* Assigns tasks to workers based on their position and available hours (max 8 hours per day).
* Uses a “fill one worker before the next” heuristic to mirror real-world scheduling.
* Calculates and prints KPIs:

  * Total placed tasks
  * Unplaced tasks
  * Average daily worker utilisation

You can reset and reload all data using:
```bash
python manage.py flush  # wipes data
python manage.py load_data  # reloads from JSON
```
📁 Code: `myapp/management/commands/auto_assign_tasks.py`   

### ✅ 2. **Handling of Workers Without Positions**

Workers without a defined `Position` are grouped under an artificial "Empty Position" category to ensure they are represented in the output table. This allows visibility of all workers, even those in undefined roles.

📁 Test fixture: `tests/fixtures/empty_position.json`
🧪 Test case: `tests/test_empty_position.py`


### ✅ 3. **Handling of Unassigned Tasks**

Tasks that are not assigned to any worker (due to capacity or other constraints) are explicitly tracked and surfaced in the KPIs, ensuring full transparency and data integrity.

📁 Test fixture: `tests/fixtures/unassigned_tasks.json`
🧪 Test case: `tests/test_unassigned_tasks.py`


### ✅ 4. **Test Suite for All Enhancements**

Automated tests have been written to verify the behavior of the enhanced features and edge cases. Fixtures and test cases are organized clearly under `tests/`.

* `test_auto_alloc.py`: Validates the auto-assignment logic
* `test_auto_allocator_kpi.py`: Verifies KPI accuracy
* `test_empty_position.py`: Checks rendering of workers with no positions
* `test_unassigned_tasks.py`: Confirms unplaced tasks are handled correctly

## 🗂 Project Structure
This is the basic structure of the project
```
work_assignment/
│
├── manage.py
├── README.md
├── requirements.txt
│
├── work_assignment/                  # Project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── myapp/                            # Main Django app
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    │
    ├── fixtures/                     # JSON seed data
    │   ├── assignments.json
    │   ├── positions.json
    │   ├── tasks.json
    │   └── workers.json
    │
    ├── migrations/                   # Database schema changes
    │   ├── 0001_initial.py
    │   ├── 0002_alter_worker_position.py
    │   └── 0003_alter_task_position.py
    │
    ├── templates/                    # HTML output templates
    │   ├── table.html
    │   └── react_table.html
    │
    ├── templatetags/                 # Custom template filters
    │   └── dict_extras.py
    │
    ├── management/                   # Custom Django commands
    │   └── commands/
    │       ├── load_data.py
    │       └── auto_assign_tasks.py
    │
    └── tests/                        # Test suite and test data
        ├── fixtures/                 # Test fixtures
        │   ├── empty_position.json
        │   ├── kpi_fixture.json
        │   ├── sample.json
        │   ├── tiny.json
        │   └── unassigned_tasks.json
        │
        ├── __init__.py
        ├── test_auto_alloc.py
        ├── test_auto_allocator_kpi.py
        ├── test_empty_position.py
        ├── test_table_api.py
        └── test_unassigned_tasks.py
```

## 🧭 Future Improvements

If this coding challenge were more extensive in scope, there are several areas where deeper implementation would have been beneficial:

-   **Django REST Framework**: While it was used to expose endpoints, its full power (serializers, viewsets, permissions) was not fully explored due to the limited size of the project.
    
-   **React or React Native**: The frontend was not a requirement for this challenge, but if it were, I would consider using React Native or ReactJS to render the table dynamically and interactively.
    
-   **Security Enhancements**:  
    In `settings.py`, the secret key is hardcoded for simplicity. In a production app, I would use an environment variable manager like `python-decouple` or `django-environ` to securely store secrets outside of version control.
    
    ```python
    # SECURITY WARNING: In production, store secrets using env vars via packages like python-decouple.
    
    ```

## 👤 Author

**Lachlan Joshua McDonald**

-   🔗 [LinkedIn](https://www.linkedin.com/in/lachlan-mcdonald-39b097214/)
    
-   💻 [GitHub](https://github.com/Lukeyone)
    

Thank you so much for taking the time out of your day to review my submission.

I hope the README and inline comments throughout the codebase have been clear enough to walk you through my thought process. While I'm still relatively new to Django, I thoroughly enjoyed the challenge and aimed to meet the requirements thoughtfully and completely.

This was a fun exercise, especially given the relaxed, untimed format. It gave me space to focus on writing clean, understandable code.

I always maintain a strong attitude toward learning and am fascinated by new technologies. I consistently dedicate time to deeply understand any new tools or concepts I encounter. I'm a fast learner and tend to pick up technical skills quickly.