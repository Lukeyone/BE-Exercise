This repo is a tiny Django project that:

1. saves Positions, Workers, Tasks and who’s assigned to what,
2. loads starter data from four JSON files,
3. spits out one ready‑to‑draw table (HTML or JSON).

--------------------------------------------------
Folder structure
--------------------------------------------------

myapp/
│
├─ fixtures/          # JSON seed + test data
│   ├─ sample.json
│   └─ tiny.json
│
├─ management/        # one command:
│   └─ load_data.py   #   python manage.py load_data
│
├─ migrations/        # FK tweaks live here
├─ models.py          # 4 simple models
├─ views.py           # brains of the operation
├─ templates/table.html
├─ templatetags/dict_extras.py
└─ unit_tests/        # 4 quick tests

--------------------------------------------------
Quick start (local)
--------------------------------------------------

```bash
# create and activate a venv however you like
python -m venv be_exercise
be_exercise\Scripts\activate.bat 
pip install -r requirements.txt
cp .env.example .env     # tweak DB creds if needed

python manage.py migrate
python manage.py load_data
python manage.py runserver
````

Open a browser:

* `http://localhost:8000/` – pretty HTML table
* `http://localhost:8000/api/table/` – same thing as JSON

---

## What the view does

* grabs every date that shows up in **Task**
* for each **Position**:

  * sums task hours per date  → row 1
  * then does the same for each **Worker** under it → more rows
* if a worker has **no position** they’re tucked under “(No Position)”
* if a task has **no worker** it lands in a final “Unassigned” row
* any missing (row, date) combo shows up as `0` so the front‑end
  doesn’t have to think.

Both the JSON and HTML views run off exactly the same helper, so
they’ll never drift.

---

## Running the tests

```bash
# Postgres role just needs CREATEDB for the temp test DB
python manage.py test -v 2
```

The suite loads:

* **tiny.json** – edge cases (null position, unassigned tasks)
* **sample.json** – bigger “real” set

and checks totals + row order.

---

## Things left to fiddle with later

* Auto‑assign tasks so no worker gets more than 8 h per day.
* Pagination or date‑range filters if this ever gets huge.
* Dockerfile / CI pipeline (easy enough, skipped for this demo).

---

## Env vars (read by django‑environ)

```
DB_NAME=be_exercise
DB_USER=myuser
DB_PASSWORD=mypass
DB_HOST=localhost
DB_PORT=5433
```