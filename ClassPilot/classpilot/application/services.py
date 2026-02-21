from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from uuid import uuid4

from classpilot.domain.entities import Lesson, LessonStatus, Student, Tutor
from classpilot.domain.errors import NotFoundError, ValidationError
from classpilot.domain.repositories import LessonRepository, StudentRepository, TutorRepository


class TutoringService:
    def __init__(
        self,
        tutor_repository: TutorRepository,
        student_repository: StudentRepository,
        lesson_repository: LessonRepository,
    ) -> None:
        self._tutor_repository = tutor_repository
        self._student_repository = student_repository
        self._lesson_repository = lesson_repository

    def register_tutor(
        self,
        full_name: str,
        email: str,
        timezone: str,
        hourly_rate: float,
    ) -> Tutor:
        if hourly_rate <= 0:
            raise ValidationError("hourly_rate must be greater than 0")
        tutor = Tutor(
            id=str(uuid4()),
            full_name=full_name.strip(),
            email=email.strip().lower(),
            timezone=timezone.strip(),
            hourly_rate=hourly_rate,
        )
        return self._tutor_repository.add(tutor)

    def register_student(
        self,
        tutor_id: str,
        full_name: str,
        email: str,
        goals: str,
    ) -> Student:
        tutor = self._tutor_repository.get(tutor_id)
        if tutor is None:
            raise NotFoundError("tutor not found")
        student = Student(
            id=str(uuid4()),
            tutor_id=tutor_id,
            full_name=full_name.strip(),
            email=email.strip().lower(),
            goals=goals.strip(),
        )
        return self._student_repository.add(student)

    def schedule_lesson(
        self,
        tutor_id: str,
        student_id: str,
        starts_at: datetime,
        duration_minutes: int,
        topic: str,
    ) -> Lesson:
        tutor = self._tutor_repository.get(tutor_id)
        if tutor is None:
            raise NotFoundError("tutor not found")
        student = self._student_repository.get(student_id)
        if student is None or student.tutor_id != tutor_id:
            raise ValidationError("student is not assigned to this tutor")
        if starts_at.tzinfo is None:
            raise ValidationError("starts_at must include timezone")
        if duration_minutes < 15:
            raise ValidationError("duration_minutes must be at least 15")
        lesson = Lesson(
            id=str(uuid4()),
            tutor_id=tutor_id,
            student_id=student_id,
            starts_at=starts_at,
            duration_minutes=duration_minutes,
            topic=topic.strip(),
            status=LessonStatus.SCHEDULED,
        )
        return self._lesson_repository.add(lesson)

    def complete_lesson(self, lesson_id: str, notes: str | None = None) -> Lesson:
        lesson = self._lesson_repository.get(lesson_id)
        if lesson is None:
            raise NotFoundError("lesson not found")
        if lesson.status != LessonStatus.SCHEDULED:
            raise ValidationError("only scheduled lessons can be completed")
        updated = replace(lesson, status=LessonStatus.COMPLETED, notes=(notes or "").strip() or None)
        return self._lesson_repository.update(updated)

    def tutor_dashboard(self, tutor_id: str) -> dict[str, int | float]:
        tutor = self._tutor_repository.get(tutor_id)
        if tutor is None:
            raise NotFoundError("tutor not found")
        students = self._student_repository.list_by_tutor(tutor_id)
        now = datetime.now(UTC)
        month_start = datetime(now.year, now.month, 1, tzinfo=UTC)
        lessons = self._lesson_repository.list_by_tutor(tutor_id)
        upcoming = [
            lesson
            for lesson in lessons
            if lesson.status == LessonStatus.SCHEDULED and lesson.starts_at >= now
        ]
        monthly_completed = [
            lesson
            for lesson in lessons
            if lesson.status == LessonStatus.COMPLETED and lesson.starts_at >= month_start
        ]
        revenue = sum((lesson.duration_minutes / 60.0) * tutor.hourly_rate for lesson in monthly_completed)
        return {
            "students_count": len(students),
            "upcoming_lessons_count": len(upcoming),
            "current_month_revenue_estimate": round(revenue, 2),
        }

