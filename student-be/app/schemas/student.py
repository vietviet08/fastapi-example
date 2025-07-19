from datetime import datetime, date
from typing import Optional, Union
from pydantic import BaseModel, EmailStr, Field, field_validator


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1, max_length=20, description="Mã sinh viên")
    first_name: str = Field(..., min_length=1, max_length=50, description="Họ")
    last_name: str = Field(..., min_length=1, max_length=50, description="Tên")
    email: EmailStr = Field(..., description="Email")
    phone: Optional[str] = Field(None, max_length=20, description="Số điện thoại")
    date_of_birth: Optional[Union[datetime, date, str]] = Field(None, description="Ngày sinh")
    address: Optional[str] = Field(None, description="Địa chỉ")

    @field_validator('date_of_birth', mode='before')
    @classmethod
    def parse_date_of_birth(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            # Try parsing date format first
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                # Try parsing datetime format
                try:
                    return datetime.fromisoformat(v.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError('Invalid date format')
        return v


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    date_of_birth: Optional[Union[datetime, date, str]] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator('date_of_birth', mode='before')
    @classmethod
    def parse_date_of_birth(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                try:
                    return datetime.fromisoformat(v.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError('Invalid date format')
        return v


class StudentInDB(StudentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class StudentResponse(StudentInDB):
    pass


class StudentListResponse(BaseModel):
    students: list[StudentResponse]
    total: int
    page: int
    size: int
    pages: int
