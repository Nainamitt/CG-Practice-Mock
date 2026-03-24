from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Student
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Pydantic Schema
class StudentSchema(BaseModel):
    name: str
    age: int
    course: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE
@app.post("/students", status_code=201)
def add_student(student: StudentSchema, db: Session = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

# READ ALL + FILTER
@app.get("/students")
def get_students(course: str = None, db: Session = Depends(get_db)):
    if course:
        return db.query(Student).filter(Student.course == course).all()
    return db.query(Student).all()

# READ ONE
@app.get("/students/{id}")
def get_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Not found")
    return student

# UPDATE
@app.put("/students/{id}")
def update_student(id: int, updated: StudentSchema, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404)

    student.name = updated.name
    student.age = updated.age
    student.course = updated.course

    db.commit()
    return student

# DELETE
@app.delete("/students/{id}")
def delete_student(id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id).first()
    if not student:
        raise HTTPException(status_code=404)

    db.delete(student)
    db.commit()
    return {"message": "Deleted"}

# BONUS SEARCH
@app.get("/search")
def search(name: str, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.name.contains(name)).all()