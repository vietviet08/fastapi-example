from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.student import (
    StudentCreate, 
    StudentUpdate, 
    StudentResponse, 
    StudentListResponse
)
from app.services.student_service import StudentService
import math

router = APIRouter()


@router.post("/students/", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    """Tạo sinh viên mới"""
    service = StudentService(db)
    
    # Kiểm tra mã sinh viên đã tồn tại
    existing_student = service.get_student_by_student_id(student.student_id)
    if existing_student:
        raise HTTPException(status_code=400, detail="Mã sinh viên đã tồn tại")
    
    # Kiểm tra email đã tồn tại
    existing_email = service.get_student_by_email(student.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
    return service.create_student(student)


@router.get("/students/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Lấy thông tin sinh viên theo ID"""
    service = StudentService(db)
    student = service.get_student_by_id(student_id)
    
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    
    return student


@router.get("/students/", response_model=StudentListResponse)
def get_students(
    page: int = Query(1, ge=1, description="Số trang"),
    size: int = Query(10, ge=1, le=100, description="Số lượng mỗi trang"),
    search: Optional[str] = Query(None, description="Từ khóa tìm kiếm"),
    db: Session = Depends(get_db)
):
    """Lấy danh sách sinh viên với phân trang và tìm kiếm"""
    service = StudentService(db)
    
    skip = (page - 1) * size
    students = service.get_students(skip=skip, limit=size, search=search)
    total = service.get_students_count(search=search)
    pages = math.ceil(total / size) if total > 0 else 1
    
    return StudentListResponse(
        students=students,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.put("/students/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_update: StudentUpdate,
    db: Session = Depends(get_db)
):
    """Cập nhật thông tin sinh viên"""
    service = StudentService(db)
    
    # Kiểm tra email đã tồn tại (nếu có cập nhật email)
    if student_update.email:
        existing_email = service.get_student_by_email(student_update.email)
        if existing_email and existing_email.id != student_id:
            raise HTTPException(status_code=400, detail="Email đã tồn tại")
    
    updated_student = service.update_student(student_id, student_update)
    if not updated_student:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    
    return updated_student


@router.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    hard_delete: bool = Query(False, description="Xóa hoàn toàn (true) hoặc vô hiệu hóa (false)"),
    db: Session = Depends(get_db)
):
    """Xóa sinh viên"""
    service = StudentService(db)
    
    if hard_delete:
        success = service.hard_delete_student(student_id)
        message = "Xóa sinh viên hoàn toàn thành công"
    else:
        success = service.delete_student(student_id)
        message = "Vô hiệu hóa sinh viên thành công"
    
    if not success:
        raise HTTPException(status_code=404, detail="Không tìm thấy sinh viên")
    
    return {"message": message}
