import pytest
from fastapi.testclient import TestClient
from tests.test_main import client


def test_create_student(client):
    """Test tạo sinh viên mới"""
    student_data = {
        "student_id": "SV001",
        "first_name": "Nguyễn",
        "last_name": "Văn A",
        "email": "nguyenvana@email.com",
        "phone": "0123456789",
        "address": "123 Đường ABC, TP.HCM"
    }
    
    response = client.post("/api/v1/students/", json=student_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["student_id"] == student_data["student_id"]
    assert data["first_name"] == student_data["first_name"]
    assert data["email"] == student_data["email"]


def test_get_students(client):
    """Test lấy danh sách sinh viên"""
    # Tạo một sinh viên trước
    student_data = {
        "student_id": "SV002",
        "first_name": "Trần",
        "last_name": "Thị B",
        "email": "tranthib@email.com"
    }
    client.post("/api/v1/students/", json=student_data)
    
    # Lấy danh sách sinh viên
    response = client.get("/api/v1/students/")
    assert response.status_code == 200
    
    data = response.json()
    assert "students" in data
    assert "total" in data
    assert data["total"] >= 1


def test_get_student_by_id(client):
    """Test lấy sinh viên theo ID"""
    # Tạo một sinh viên trước
    student_data = {
        "student_id": "SV003",
        "first_name": "Lê",
        "last_name": "Văn C",
        "email": "levanc@email.com"
    }
    create_response = client.post("/api/v1/students/", json=student_data)
    student_id = create_response.json()["id"]
    
    # Lấy sinh viên theo ID
    response = client.get(f"/api/v1/students/{student_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["student_id"] == student_data["student_id"]


def test_update_student(client):
    """Test cập nhật sinh viên"""
    # Tạo một sinh viên trước
    student_data = {
        "student_id": "SV004",
        "first_name": "Phạm",
        "last_name": "Thị D",
        "email": "phamthid@email.com"
    }
    create_response = client.post("/api/v1/students/", json=student_data)
    student_id = create_response.json()["id"]
    
    # Cập nhật sinh viên
    update_data = {
        "first_name": "Phạm",
        "last_name": "Văn D Updated",
        "phone": "0987654321"
    }
    
    response = client.put(f"/api/v1/students/{student_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["last_name"] == update_data["last_name"]
    assert data["phone"] == update_data["phone"]


def test_delete_student(client):
    """Test xóa sinh viên"""
    # Tạo một sinh viên trước
    student_data = {
        "student_id": "SV005",
        "first_name": "Hoàng",
        "last_name": "Văn E",
        "email": "hoangvane@email.com"
    }
    create_response = client.post("/api/v1/students/", json=student_data)
    student_id = create_response.json()["id"]
    
    # Xóa sinh viên (soft delete)
    response = client.delete(f"/api/v1/students/{student_id}")
    assert response.status_code == 200
    
    # Kiểm tra sinh viên đã bị vô hiệu hóa
    get_response = client.get(f"/api/v1/students/{student_id}")
    assert get_response.status_code == 200
    assert get_response.json()["is_active"] == False


def test_create_duplicate_student_id(client):
    """Test tạo sinh viên với mã trùng lặp"""
    student_data = {
        "student_id": "SV006",
        "first_name": "Test",
        "last_name": "User",
        "email": "test1@email.com"
    }
    
    # Tạo sinh viên đầu tiên
    response1 = client.post("/api/v1/students/", json=student_data)
    assert response1.status_code == 201
    
    # Tạo sinh viên thứ hai với cùng student_id
    student_data["email"] = "test2@email.com"
    response2 = client.post("/api/v1/students/", json=student_data)
    assert response2.status_code == 400
    assert "Mã sinh viên đã tồn tại" in response2.json()["detail"]
