from __future__ import annotations

from sqlalchemy import select

from models.student import Student
from repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository):
    def get_by_user_id(self, user_id: int) -> Student | None:
        return self._session.scalar(select(Student).where(Student.user_id == user_id))

    def number_exists(self, student_number: str) -> bool:
        return self._session.scalar(
            select(Student.id).where(Student.student_number == student_number)
        ) is not None

    def add(self, student: Student) -> Student:
        self._session.add(student)
        self._session.flush()
        return student
