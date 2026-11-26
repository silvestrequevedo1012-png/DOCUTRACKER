# DocuTrack - Phase 2 (authentication, registration, role-based access)

Extract this zip INTO your existing docutrack folder (overwrite when asked).
It does not touch .env, docutrack.db, database/connection.py or migrations.

1. Add these lines to your .env (see .env.example):
   SESSION_TIMEOUT_MINUTES=30
   MAX_LOGIN_ATTEMPTS=5
   LOCKOUT_MINUTES=15
   ADMIN_EMAIL=admin@docutrack.com
   ADMIN_PASSWORD=ChangeMe123!
   (use your own admin password; .local / .test email domains are rejected)
2. pip install -r requirements.txt   (no new packages)
3. python -m database.seed           (creates the admin + 5 document types; safe to re-run)
4. python main.py

No database migration is needed in Phase 2.
