# Student Management System

A modern full-stack application for student management built with FastAPI and Vue.js, fully containerized with Docker for easy deployment and development.

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🚀 Features

### Backend Features
- **FastAPI Framework**: High-performance, easy-to-learn, fast to code, ready for production
- **SQLAlchemy ORM**: Object-relational mapping for database operations
- **Alembic Migrations**: Database version control
- **JWT Authentication**: Secure API access with token-based authentication
- **Pydantic Validation**: Type hints and data validation
- **PostgreSQL Database**: Reliable, robust relational database
- **Modular Architecture**: Well-organized code structure following best practices

### Frontend Features
- **Vue.js 3**: Progressive JavaScript framework with Composition API
- **TypeScript**: Type safety and better developer experience
- **Pinia**: State management for Vue applications
- **Vue Router**: Official router for Vue.js
- **Internationalization (i18n)**: Multilingual support (English, Japanese, Vietnamese)
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive Design**: Mobile-friendly user interface
- **Component-Based Architecture**: Reusable UI components

## 📋 Project Structure

```
.
├── student-be/                  # FastAPI backend
│   ├── alembic/                 # Database migrations
│   │   ├── versions/            # Migration versions
│   │   └── env.py               # Alembic configuration
│   ├── app/                     # Application code
│   │   ├── api/                 # API endpoints
│   │   │   └── v1/              # API version 1
│   │   ├── core/                # Core functionality
│   │   ├── db/                  # Database configuration
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── utils/               # Utility functions
│   ├── tests/                   # Test suite
│   ├── Dockerfile               # Backend container configuration
│   └── requirements.txt         # Python dependencies
│
├── student-fe/                  # Vue.js frontend
│   ├── src/                     # Application source code
│   │   ├── api/                 # API clients
│   │   ├── assets/              # Static assets
│   │   ├── components/          # Reusable Vue components
│   │   ├── composables/         # Vue composition functions
│   │   ├── i18n/                # Internationalization
│   │   │   └── locales/         # Language files
│   │   ├── router/              # Vue Router configuration
│   │   ├── stores/              # Pinia stores
│   │   ├── types/               # TypeScript type definitions
│   │   ├── utils/               # Utility functions
│   │   └── views/               # Page components
│   ├── Dockerfile               # Frontend container configuration
│   └── package.json             # Node.js dependencies
│
└── docker-compose.yml           # Docker services configuration
```

## 🔧 Prerequisites

- Docker and Docker Compose
- Git

## 🏁 Getting Started

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/vietviet08/fastapi-example
cd student-management-system
```

2. Create required environment files:

For backend (create `student-be/.env.docker`):
```
DATABASE_URL=postgresql://root:root@db:5432/student_db
SECRET_KEY=your-secret-key-here
DEBUG=true
ALLOWED_ORIGINS=["http://localhost:3000"]
```

For frontend (create `student-fe/.env`):
```
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

3. Build and start all services:
```bash
docker-compose up --build
```

4. Access the applications:
   - 🌐 **Frontend**: [http://localhost:3000](http://localhost:3000)
   - 🚀 **Backend API**: [http://localhost:8000](http://localhost:8000)
   - 📚 **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - 📖 **API Redoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Initial Setup

On first run, create an admin user:
```bash
docker-compose exec api python create_admin.py
```

## 💻 Development

### Backend Development

- **Hot Reload**: Changes to Python files will automatically restart the server
- **Run Tests**: `docker-compose exec api pytest`
- **Create Migration**: `docker-compose exec api alembic revision --autogenerate -m "description"`
- **Apply Migration**: `docker-compose exec api alembic upgrade head`
- **Access Shell**: `docker-compose exec api bash`

### Frontend Development

- **Hot Reload**: Changes to Vue files will trigger automatic rebuilds
- **Access Shell**: `docker-compose exec web sh`
- **Add Dependency**: `docker-compose exec web npm install --save package-name`

## 🌍 API Endpoints

The complete API documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs)

Key endpoints:

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token

### Students
- `GET /api/v1/students` - List students
- `POST /api/v1/students` - Create student
- `GET /api/v1/students/{id}` - Get student details
- `PUT /api/v1/students/{id}` - Update student
- `DELETE /api/v1/students/{id}` - Delete student

## 🐳 Docker Services

### Database (PostgreSQL)
- **Image**: postgres:15
- **Port**: 5432
- **Credentials**: user=root, password=root, db=student_db
- **Data**: Persisted in a Docker volume

### Backend API (FastAPI)
- **Port**: 8000
- **Dependencies**: PostgreSQL database
- **Code**: Mounted as a volume for live reload

### Frontend Web (Vue.js with Nginx)
- **Port**: 3000 (mapped to container port 80)
- **Build**: Multi-stage build for production optimization

## ⚙️ Environment Variables

### Backend Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://root:root@db:5432/student_db |
| SECRET_KEY | JWT secret key | (Required) |
| DEBUG | Debug mode | false |
| ALLOWED_ORIGINS | CORS allowed origins | ["*"] |

### Frontend Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| VITE_API_BASE_URL | API base URL | http://localhost:8000/api/v1 |

## 🚀 Production Deployment

For production deployment:

1. Create production environment files:
   - `student-be/.env.prod` with secure settings
   - `student-fe/.env.prod` with production API URL

2. Update docker-compose command:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

3. Recommended production settings:
   - Use strong, unique passwords
   - Set DEBUG=false
   - Configure HTTPS
   - Set specific ALLOWED_ORIGINS
   - Use Docker Swarm or Kubernetes for orchestration

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Ensure PostgreSQL service is running: `docker-compose ps`
   - Check database logs: `docker-compose logs db`
   - Verify connection string in `.env.docker`

2. **API Not Accessible**
   - Check if API container is running: `docker-compose ps api`
   - View API logs: `docker-compose logs api`
   - Ensure port 8000 is not used by another service

3. **Frontend Not Loading**
   - Verify web container is running: `docker-compose ps web`
   - Check web logs: `docker-compose logs web`
   - Ensure port 3000 is not used by another service

4. **Database Migration Issues**
   - Apply migrations manually: `docker-compose exec api alembic upgrade head`
   - Check migration logs: `docker-compose exec api alembic history`

### Reset Everything

To completely reset your environment:
```bash
docker-compose down -v
docker-compose up --build --force-recreate
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.
