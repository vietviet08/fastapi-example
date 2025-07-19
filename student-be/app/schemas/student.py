from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=20, description="Mã sinh viên")
    first_name: str = Field(..., min_length=1, max_length=50, description="Họ")
    last_name: str = Field(..., min_length=1, max_length=50, description="Tên")
    email: EmailStr = Field(..., description="Email")
    phone: Optional[str] = Field(None, max_length=20, description="Số điện thoại")
    date_of_birth: Optional[datetime] = Field(None, description="Ngày sinh")
    address: Optional[str] = Field(None, description="Địa chỉ")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[datetime] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None


class StudentInDB(StudentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True


class StudentResponse(StudentInDB):
    pass


class StudentListResponse(BaseModel):
    students: list[StudentResponse]
    total: int
    page: int
    size: int
    pages: int
