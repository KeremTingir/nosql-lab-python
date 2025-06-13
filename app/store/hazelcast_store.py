import hazelcast
from app.model.student import Student

class HazelcastStore:
    _client = None
    _map = None

    @classmethod
    def init(cls):
        cls._client = hazelcast.HazelcastClient(
            cluster_members=["localhost:5701"]
        )
        cls._map = cls._client.get_map("ogrenciler").blocking()
        # Populate with 10,000 students
        for i in range(10000):
            student_id = f"2025{str(i).zfill(6)}"
            student = Student(
                ogrenciNo=student_id,
                adSoyad=f"Ad Soyad {i}",
                bolum="Bilgisayar"
            )
            cls._map.put(student_id, student)

    @classmethod
    def get(cls, student_id: str) -> Student:
        return cls._map.get(student_id)