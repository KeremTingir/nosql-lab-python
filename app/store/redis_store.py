import redis
from app.model.student import Student
import json

class RedisStore:
    _client = None

    @classmethod
    def init(cls):
        cls._client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        # Populate with 10,000 students
        for i in range(10000):
            student_id = f"2025{str(i).zfill(6)}"  # e.g., 2025000001
            student = Student(
                ogrenciNo=student_id,
                adSoyad=f"Ad Soyad {i}",
                bolum="Bilgisayar"
            )
            cls._client.set(student_id, json.dumps(student.dict()))

    @classmethod
    def get(cls, student_id: str) -> Student:
        json_data = cls._client.get(student_id)
        if json_data:
            return Student(**json.loads(json_data))
        return None