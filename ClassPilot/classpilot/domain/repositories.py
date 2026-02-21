from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from classpilot.domain.entities import Lesson, Student, Tutor


class TutorRepository(ABC):
    @abstractmethod
    def add(self, tutor: Tutor) -> Tutor:
        raise NotImplementedError

    @abstractmethod
    def get(self, tutor_id: str) -> Tutor | None:
        raise NotImplementedError


class StudentRepository(ABC):
    @abstractmethod
    def add(self, student: Student) -> Student:
        raise NotImplementedError

    @abstractmethod
    def get(self, student_id: str) -> Student | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_tutor(self, tutor_id: str) -> list[Student]:
        raise NotImplementedError


class LessonRepository(ABC):
    @abstractmethod
    def add(self, lesson: Lesson) -> Lesson:
        raise NotImplementedError

    @abstractmethod
    def get(self, lesson_id: str) -> Lesson | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, lesson: Lesson) -> Lesson:
        raise NotImplementedError

    @abstractmethod
    def list_by_tutor(
        self,
        tutor_id: str,
        start_from: datetime | None = None,
        end_to: datetime | None = None,
    ) -> list[Lesson]:
        raise NotImplementedError

