from database import SessionLocal
from models import Student

db = SessionLocal()


@app.get("/search")
def search(name: str):
    return db.query(Student).filter(Student.name.contains(name)).all()

@app.post("/students")
def add_student(student: StudentSchema):
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    return new_student