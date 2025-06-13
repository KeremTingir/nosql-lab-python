from fastapi import FastAPI
from app.store.redis_store import RedisStore
from app.store.hazelcast_store import HazelcastStore
from app.store.mongo_store import MongoStore
from app.model.student import Student

app = FastAPI()

# Initialize stores
RedisStore.init()
HazelcastStore.init()
MongoStore.init()

@app.get("/nosql-lab-rd/ogrenci_no={student_id}", response_model=Student)
async def get_from_redis(student_id: str):
    student = RedisStore.get(student_id)
    if student:
        return student
    return {"error": "Student not found"}

@app.get("/nosql-lab-hz/ogrenci_no={student_id}", response_model=Student)
async def get_from_hazelcast(student_id: str):
    student = HazelcastStore.get(student_id)
    if student:
        return student
    return {"error": "Student not found"}

@app.get("/nosql-lab-mon/ogrenci_no={student_id}", response_model=Student)
async def get_from_mongodb(student_id: str):
    student = MongoStore.get(student_id)
    if student:
        return student
    return {"error": "Student not found"}