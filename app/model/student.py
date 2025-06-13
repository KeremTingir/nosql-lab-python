from pydantic import BaseModel

class Student(BaseModel):
    ogrenciNo: str
    adSoyad: str
    bolum: str