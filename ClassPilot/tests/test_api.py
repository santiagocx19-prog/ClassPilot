from datetime import UTC, datetime, timedelta
from pathlib import Path

from fastapi.testclient import TestClient

from classpilot.presentation import api
from classpilot.application.services import TutoringService
from classpilot.infrastructure.json_store import (
    JsonFileStore,
    JsonLessonRepository,
    JsonStudentRepository,
    JsonTutorRepository,
)


def build_test_client(tmp_path: Path) -> TestClient:
    data_file = tmp_path / "api_data.json"

    def _get_service() -> TutoringService:
        store = JsonFileStore(data_file)
        return TutoringService(
            tutor_repository=JsonTutorRepository(store),
            student_repository=JsonStudentRepository(store),
            lesson_repository=JsonLessonRepository(store),
        )

    api.app.dependency_overrides[api.get_service] = _get_service
    return TestClient(api.app)


def test_happy_path_creation(tmp_path: Path):
    client = build_test_client(tmp_path)

    tutor_response = client.post(
        "/tutors",
        json={
            "full_name": "Marcos",
            "email": "marcos@demo.com",
            "timezone": "UTC",
            "hourly_rate": 40,
        },
    )
    assert tutor_response.status_code == 200
    tutor_id = tutor_response.json()["id"]

    student_response = client.post(
        f"/tutors/{tutor_id}/students",
        json={"full_name": "Paula", "email": "paula@demo.com", "goals": "Conversation"},
    )
    assert student_response.status_code == 200
    student_id = student_response.json()["id"]

    lesson_response = client.post(
        "/lessons",
        json={
            "tutor_id": tutor_id,
            "student_id": student_id,
            "starts_at": (datetime.now(UTC) + timedelta(days=2)).isoformat(),
            "duration_minutes": 60,
            "topic": "Speaking drill",
        },
    )
    assert lesson_response.status_code == 200
    assert lesson_response.json()["status"] == "scheduled"

