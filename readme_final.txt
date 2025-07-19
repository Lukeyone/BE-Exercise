# Task‑Assignments – Django Back‑End Exercise

A compact Django app that

1. stores **Positions**, **Workers**, **Tasks**, and **Assignments**  
2. seeds those tables from the four JSON files supplied with the brief  
3. exposes two endpoints—one JSON, one HTML—that return a **ready‑made table**
   of total task‑hours per day, so a front‑end can render immediately with
   **zero additional logic**.

&nbsp;

---

## 1.  Project Goals (mapping back to the brief)

| Brief item | Where it’s implemented |
|------------|------------------------|
| **Create models** | `myapp/models.py` – 4 models with clear FKs |
| **Load JSON files** | `python manage.py load_data` – custom management command |
| **Expose endpoint** | `/api/table/` (JSON) and `/table/` (HTML) |
| **Summarise for easy table render** | `views.build_rows()` – groups, sums, and zero‑fills |

Enhancement hooks (unassigned tasks, orphan workers, auto‑allocation, etc.) are
stubbed in **Section&nbsp;8** for future work.

&nbsp;

---

## 2.  Tech Stack

* **Python 3.10**  
* **Django 4.x** (no third‑party dependencies—kept intentionally light)  
* **PostgreSQL 17** (but settings.py uses env vars so you can point to any DB)  

&nbsp;

---

## 3.  Quick Start

```bash
git clone <your‑fork>
cd work_assignment
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt                  # Django + psycopg2

# 1. migrate schema
python manage.py migrate

# 2. seed the database
python manage.py load_data

# 3. run
python manage.py runserver
