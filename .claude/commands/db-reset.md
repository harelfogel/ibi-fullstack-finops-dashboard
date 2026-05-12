Reset the database: drop all tables, re-run migrations, optionally seed with sample data.

Steps:
1. Ensure PostgreSQL is running: `docker-compose ps postgres`.
2. Drop and recreate the database:
   ```
   docker-compose exec postgres psql -U finops -d finops_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
   ```
3. Run Alembic migrations:
   ```
   docker-compose exec backend alembic upgrade head
   ```
4. Ask the user if they want to seed sample data.
5. If yes, upload `sample_data/transactions_sample.csv` via the API:
   ```
   curl -X POST http://localhost:8000/api/v1/transactions/upload -F "file=@sample_data/transactions_sample.csv"
   ```
6. Report the result: tables created, rows seeded (if applicable).
