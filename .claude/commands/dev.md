Start the full development stack with Docker Compose.

Steps:
1. Run `docker-compose up --build -d` from the project root.
2. Wait for all services to become healthy:
   - `docker-compose ps` to check status.
   - Retry up to 60 seconds if services are still starting.
3. Report service URLs when ready:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - PostgreSQL: localhost:5432 (finops/finops)
4. If any service fails, show `docker-compose logs <service>` for the failing service.
