from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile

from classpilot.domain.entities import Lesson, LessonStatus, Student, Tutor
from classpilot.domain.repositories import LessonRepository, StudentRepository, TutorRepository


class JsonFileStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write_data({"tutors": [], "students": [], "lessons": []})

    def read_data(self) -> dict:
        with self.path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def write_data(self, data: dict) -> None:
        self._write_data(data)

    def _write_data(self, data: dict) -> None:
        with NamedTemporaryFile("w", encoding="utf-8", delete=False, dir=self.path.parent) as tmp:
            json.dump(data, tmp, ensure_ascii=True, indent=2)
            temp_path = Path(tmp.name)
        temp_path.replace(self.path)


class JsonTutorRepository(TutorRepository):
    def __init__(self, store: JsonFileStore) -> None:
        self._store = store

    def add(self, tutor: Tutor) -> Tutor:
        data = self._store.read_data()
        data["tutors"].append(asdict(tutor))
        self._store.write_data(data)
        return tutor

    def get(self, tutor_id: str) -> Tutor | None:
        data = self._store.read_data()
        for tutor_dict in data["tutors"]:
            if tutor_dict["id"] == tutor_id:
                return Tutor(**tutor_dict)
        return None


class JsonStudentRepository(StudentRepository):
    def __init__(self, store: JsonFileStore) -> None:
        self._store = store

    def add(self, student: Student) -> Student:
        data = self._store.read_data()
        data["students"].append(asdict(student))
        self._store.write_data(data)
        return student

    def get(self, student_id: str) -> Student | None:
        data = self._store.read_data()
        for student_dict in data["students"]:
            if student_dict["id"] == student_id:
                return Student(**student_dict)
        return None

    def list_by_tutor(self, tutor_id: str) -> list[Student]:
        data = self._store.read_data()
        return [Student(**row) for row in data["students"] if row["tutor_id"] == tutor_id]


class JsonLessonRepository(LessonRepository):
    def __init__(self, store: JsonFileStore) -> None:
        self._store = store

    def add(self, lesson: Lesson) -> Lesson:
        data = self._store.read_data()
        data["lessons"].append(self._to_dict(lesson))
        self._store.write_data(data)
        return lesson

    def get(self, lesson_id: str) -> Lesson | None:
        data = self._store.read_data()
        for lesson_dict in data["lessons"]:
            if lesson_dict["id"] == lesson_id:
                return self._from_dict(lesson_dict)
        return None

    def update(self, lesson: Lesson) -> Lesson:
        data = self._store.read_data()
        for index, lesson_dict in enumerate(data["lessons"]):
            if lesson_dict["id"] == lesson.id:
                data["lessons"][index] = self._to_dict(lesson)
                self._store.write_data(data)
                return lesson
        raise KeyError(f"lesson {lesson.id} not found")

    def list_by_tutor(
        self,
        tutor_id: str,
        start_from: datetime | None = None,
        end_to: datetime | None = None,
    ) -> list[Lesson]:
        data = self._store.read_data()
        lessons: list[Lesson] = []
        for row in data["lessons"]:
            if row["tutor_id"] != tutor_id:
                continue
            lesson = self._from_dict(row)
            if start_from and lesson.starts_at < start_from:
                continue
            if end_to and lesson.starts_at > end_to:
                continue
            lessons.append(lesson)
        return lessons

    @staticmethod
    def _to_dict(lesson: Lesson) -> dict:
        return {
            "id": lesson.id,
            "tutor_id": lesson.tutor_id,
            "student_id": lesson.student_id,
            "starts_at": lesson.starts_at.isoformat(),
            "duration_minutes": lesson.duration_minutes,
            "topic": lesson.topic,
            "status": lesson.status.value,
            "notes": lesson.notes,
        }

    @staticmethod
    def _from_dict(data: dict) -> Lesson:
        return Lesson(
            id=data["id"],
            tutor_id=data["tutor_id"],
            student_id=data["student_id"],
            starts_at=datetime.fromisoformat(data["starts_at"]),
            duration_minutes=data["duration_minutes"],
            topic=data["topic"],
            status=LessonStatus(data["status"]),
            notes=data.get("notes"),
        )

