# DocuTrack – Phase 1

## Setup
1. `python -m venv .venv && source .venv/bin/activate`  (Windows: `.venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. Create the database in PostgreSQL:
   ```sql
   CREATE USER docutrack_user WITH PASSWORD 'your-password';
   CREATE DATABASE docutrack OWNER docutrack_user;
   ```
4. Edit `.env` (DB_* values and a long random SECRET_KEY).
5. Generate and apply the first migration:
   ```
   alembic revision --autogenerate -m "initial schema"
   alembic upgrade head
   ```
6. Run: `python main.py` (or `flet run main.py`)
