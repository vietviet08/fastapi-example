from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_student(self, student_data: StudentCreate) -> Student:
        """Tạo sinh viên mới"""
        db_student = Student(**student_data.dict())
        self.db.add(db_student)
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
    
    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        """Lấy sinh viên theo ID"""
        return self.db.query(Student).filter(Student.id == student_id).first()
    
    def get_student_by_student_id(self, student_id: str) -> Optional[Student]:
        """Lấy sinh viên theo mã sinh viên"""
        return self.db.query(Student).filter(Student.student_id == student_id).first()
    
    def get_student_by_email(self, email: str) -> Optional[Student]:
        """Lấy sinh viên theo email"""
        return self.db.query(Student).filter(Student.email == email).first()
    
    def get_students(self, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Student]:
        """Lấy danh sách sinh viên với phân trang và tìm kiếm"""
        query = self.db.query(Student)
        
        if search:
            query = query.filter(
                (Student.first_name.ilike(f"%{search}%")) |
                (Student.last_name.ilike(f"%{search}%")) |
                (Student.student_id.ilike(f"%{search}%")) |
                (Student.email.ilike(f"%{search}%"))
            )
        
        return query.offset(skip).limit(limit).all()
    
    def get_students_count(self, search: Optional[str] = None) -> int:
        """Đếm tổng số sinh viên"""
        query = self.db.query(func.count(Student.id))
        
        if search:
            query = query.filter(
                (Student.first_name.ilike(f"%{search}%")) |
                (Student.last_name.ilike(f"%{search}%")) |
                (Student.student_id.ilike(f"%{search}%")) |
                (Student.email.ilike(f"%{search}%"))
            )
        
        return query.scalar()
    
    def update_student(self, student_id: int, student_data: StudentUpdate) -> Optional[Student]:
        """Cập nhật thông tin sinh viên"""
        db_student = self.get_student_by_id(student_id)
        if not db_student:
            return None
        
        update_data = student_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_student, field, value)
        
        self.db.commit()
        self.db.refresh(db_student)
        return db_student
    
    def delete_student(self, student_id: int) -> bool:
        """Xóa sinh viên (soft delete)"""
        db_student = self.get_student_by_id(student_id)
        if not db_student:
            return False
        
        db_student.is_active = False
        self.db.commit()
        return True
    
    def hard_delete_student(self, student_id: int) -> bool:
        """Xóa sinh viên hoàn toàn"""
        db_student = self.get_student_by_id(student_id)
        if not db_student:
            return False
        
        self.db.delete(db_student)
        self.db.commit()
        return True
