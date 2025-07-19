# Student Management API

API quản lý sinh viên được xây dựng bằng FastAPI, SQLAlchemy và PostgreSQL.

## Cấu trúc thư mục

```
student-be/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py          # Router chính cho API v1
│   │       └── students.py        # Endpoints cho sinh viên
│   ├── core/
│   │   ├── __init__.py
│   │   ├── app.py                 # Cấu hình FastAPI app
│   │   └── settings.py            # Cấu hình ứng dụng
│   ├── db/
│   │   ├── __init__.py
│   │   └── database.py            # Cấu hình database
│   ├── models/
│   │   ├── __init__.py
│   │   └── student.py             # Model Student
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── student.py             # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   └── student_service.py     # Business logic
│   └── utils/
│       ├── __init__.py
│       └── security.py            # JWT, password hashing
├── alembic/                       # Database migrations
├── tests/                         # Unit tests
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── alembic.ini                    # Alembic configuration
└── README.md                      # Documentation
```

## Cài đặt

### 1. Clone repository và cài đặt dependencies

```bash
cd student-be
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# hoặc
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Sao chép file `.env.example` thành `.env` và cập nhật các thông số:

```bash
cp .env.example .env
```

Cập nhật file `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/student_db
SECRET_KEY=your-very-secret-key-here
```

### 3. Cài đặt PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS với Homebrew
brew install postgresql

# Windows: Tải từ https://www.postgresql.org/download/windows/
```

### 4. Tạo database

```bash
sudo -u postgres psql
CREATE DATABASE student_db;
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE student_db TO username;
\q
```

### 5. Chạy migrations

```bash
# Tạo migration đầu tiên
alembic revision --autogenerate -m "Create students table"

# Chạy migrations
alembic upgrade head
```

## Chạy ứng dụng

### Development
```bash
python main.py
```

### Production với Uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Với Docker
```bash
# Tạo Dockerfile nếu cần
docker build -t student-api .
docker run -p 8000:8000 student-api
```

## API Endpoints

### Students

- `POST /api/v1/students/` - Tạo sinh viên mới
- `GET /api/v1/students/` - Lấy danh sách sinh viên (có phân trang và tìm kiếm)
- `GET /api/v1/students/{id}` - Lấy thông tin sinh viên theo ID
- `PUT /api/v1/students/{id}` - Cập nhật thông tin sinh viên
- `DELETE /api/v1/students/{id}` - Xóa sinh viên

### System

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/docs` - Swagger documentation
- `GET /api/v1/redoc` - ReDoc documentation

## Testing

```bash
# Chạy tất cả tests
pytest

# Chạy tests với coverage
pytest --cov=app

# Chạy specific test file
pytest tests/test_students.py
```

## API Documentation

Khi ứng dụng đang chạy, bạn có thể truy cập:
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

## Ví dụ sử dụng API

### Tạo sinh viên mới

```bash
curl -X POST "http://localhost:8000/api/v1/students/" \
     -H "Content-Type: application/json" \
     -d '{
       "student_id": "SV001",
       "first_name": "Nguyễn",
       "last_name": "Văn A",
       "email": "nguyenvana@email.com",
       "phone": "0123456789",
       "date_of_birth": "2000-01-01T00:00:00",
       "address": "123 Đường ABC, TP.HCM"
     }'
```

### Lấy danh sách sinh viên

```bash
curl "http://localhost:8000/api/v1/students/?page=1&size=10&search=Nguyễn"
```

### Cập nhật sinh viên

```bash
curl -X PUT "http://localhost:8000/api/v1/students/1" \
     -H "Content-Type: application/json" \
     -d '{
       "phone": "0987654321",
       "address": "456 Đường XYZ, Hà Nội"
     }'
```

## Development

### Thêm model mới

1. Tạo model trong `app/models/`
2. Tạo schema trong `app/schemas/`
3. Tạo service trong `app/services/`
4. Tạo endpoints trong `app/api/v1/`
5. Import router vào `app/api/v1/router.py`
6. Tạo và chạy migration

### Database Migration

```bash
# Tạo migration mới
alembic revision --autogenerate -m "Description"

# Chạy migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Troubleshooting

### Lỗi kết nối database
- Kiểm tra PostgreSQL đang chạy
- Kiểm tra thông tin kết nối trong `.env`
- Kiểm tra database và user đã được tạo

### Lỗi import module
- Kiểm tra virtual environment đã được activate
- Kiểm tra tất cả dependencies đã được cài đặt
- Kiểm tra PYTHONPATH

### Lỗi migration
- Kiểm tra database connection
- Kiểm tra file `alembic/env.py` có import đúng models
- Xóa file migration lỗi và tạo lại nếu cần

## Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request
