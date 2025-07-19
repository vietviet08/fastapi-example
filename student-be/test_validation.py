from app.schemas.student import StudentCreate
from pydantic import ValidationError
import json

# Test data tương tự như frontend gửi
test_data = {
    "student_id": "SV001",
    "first_name": "Nguyễn",
    "last_name": "Văn A",
    "email": "test@example.com",
    "phone": "0123456789",
    "date_of_birth": "2000-01-01",
    "address": "Test address"
}

try:
    student = StudentCreate(**test_data)
    print("Validation successful!")
    print(f"Student: {student}")
except ValidationError as e:
    print("Validation error:")
    print(json.dumps(e.errors(), indent=2))
