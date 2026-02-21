from datetime import UTC, datetime, timedelta

import pytest

from classpilot.application.services import TutoringService
from classpilot.domain.errors import ValidationError
from classpilot.infrastructure.json_store import (
    JsonFileStore,
    JsonLessonRepository,
    JsonStudentRepository,
    JsonTutorRepository,
)


@pytest.fixture
def service(tmp_path):
    store = JsonFileStore(tmp_path / "classpilot.json")
    return TutoringService(
        tutor_repository=JsonTutorRepository(store),
        student_repository=JsonStudentRepository(store),
        lesson_repository=JsonLessonRepository(store),
    )


def test_complete_lesson_changes_status(service: TutoringService):
    tutor = service.register_tutor("Ana Ruiz", "ana@demo.com", "UTC", 30.0)
    student = service.register_student(tutor.id, "Leo", "leo@demo.com", "Exam prep")
    lesson = service.schedule_lesson(
        tutor_id=tutor.id,
        student_id=student.id,
        starts_at=datetime.now(UTC) + timedelta(days=1),
        duration_minutes=60,
        topic="Functions",
    )
    completed = service.complete_lesson(lesson.id, notes="Great progress")

    assert completed.status.value == "completed"
    assert completed.notes == "Great progress"


def test_schedule_requires_student_assigned_to_tutor(service: TutoringService):
    tutor_a = service.register_tutor("A", "a@demo.com", "UTC", 25)
    tutor_b = service.register_tutor("B", "b@demo.com", "UTC", 30)
    student_b = service.register_student(tutor_b.id, "Student", "s@demo.com", "Math")

    with pytest.raises(ValidationError):
        service.schedule_lesson(
            tutor_id=tutor_a.id,
            student_id=student_b.id,
            starts_at=datetime.now(UTC) + timedelta(days=1),
            duration_minutes=60,
            topic="Wrong tutor",
        )

