# Student Management System - Docker Setup

This project consists of a FastAPI backend and Vue.js frontend, both containerized with Docker.

## Services

- **Database (db)**: PostgreSQL 15
- **Backend API (api)**: FastAPI application on port 8000
- **Frontend Web (web)**: Vue.js application served with Nginx on port 3000

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. Clone the repository and navigate to the project directory:
```bash
cd /path/to/your/project
```

2. Build and start all services:
```bash
docker-compose up --build
```

3. Access the applications:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Development Mode

To run with live reload (for development):
```bash
docker-compose up --build
```

## Production Mode

For production deployment, you may want to:
1. Update environment variables in docker-compose.yml
2. Use production-ready database credentials
3. Set DEBUG=false in the API service

## Services Details

### Database
- **Image**: postgres:15
- **Port**: 5432
- **Database**: student_db
- **User**: root
- **Password**: root

### Backend API
- **Build**: ./student-be
- **Port**: 8000
- **Environment**: Development mode with auto-reload
- **Dependencies**: PostgreSQL database

### Frontend Web
- **Build**: ./student-fe (Multi-stage build with Node.js and Nginx)
- **Port**: 3000 (mapped to container port 80)
- **Dependencies**: Backend API service

## Useful Commands

```bash
# Start services
docker-compose up

# Start services in background
docker-compose up -d

# Rebuild and start services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs web
docker-compose logs api
docker-compose logs db

# Execute commands in running containers
docker-compose exec api bash
docker-compose exec web sh
docker-compose exec db psql -U root -d student_db
```

## Environment Variables

### Frontend (.env)
- `VITE_API_BASE_URL`: API base URL (default: http://localhost:8000/api/v1)

### Backend
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `DEBUG`: Debug mode (true/false)

## Troubleshooting

1. **Port conflicts**: Make sure ports 3000, 8000, and 5432 are not in use by other applications
2. **Database connection**: Wait for the database to be ready before the API starts (handled by depends_on)
3. **Build issues**: Use `docker-compose down -v` to remove volumes and `docker-compose up --build --force-recreate` to rebuild from scratch
