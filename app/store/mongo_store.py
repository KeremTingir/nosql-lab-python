from pymongo import MongoClient
from app.model.student import Student

class MongoStore:
    _client = None
    _collection = None

    @classmethod
    def init(cls):
        cls._client = MongoClient("mongodb://localhost:27017")
        cls._collection = cls._client["nosqllab"]["ogrenciler"]
        cls._collection.drop()  # Clear existing data
        # Populate with 10,000 students
        for i in range(10000):
            student_id = f"2025{str(i).zfill(6)}"
            student = Student(
                ogrenciNo=student_id,
                adSoyad=f"Ad Soyad {i}",
                bolum="Bilgisayar"
            )
            cls._collection.insert_one(student.dict())

    @classmethod
    def get(cls, student_id: str) -> Student:
        doc = cls._collection.find_one({"ogrenciNo": student_id})
        if doc:
            return Student(**doc)
        return None