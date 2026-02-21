from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from classpilot.application.services import TutoringService
from classpilot.domain.errors import DomainError, NotFoundError
from classpilot.infrastructure.json_store import (
    JsonFileStore,
    JsonLessonRepository,
    JsonStudentRepository,
    JsonTutorRepository,
)


DATA_FILE = Path("data") / "classpilot.json"


class TutorCreateRequest(BaseModel):
    full_name: str
    email: str
    timezone: str = "UTC"
    hourly_rate: float = Field(gt=0)


class StudentCreateRequest(BaseModel):
    full_name: str
    email: str
    goals: str


class LessonScheduleRequest(BaseModel):
    tutor_id: str
    student_id: str
    starts_at: datetime
    duration_minutes: int = Field(ge=15)
    topic: str


class LessonCompleteRequest(BaseModel):
    notes: str | None = None


def get_service() -> TutoringService:
    store = JsonFileStore(DATA_FILE)
    return TutoringService(
        tutor_repository=JsonTutorRepository(store),
        student_repository=JsonStudentRepository(store),
        lesson_repository=JsonLessonRepository(store),
    )


app = FastAPI(
    title="ClassPilot API",
    description="Sistema de gestion para profesores particulares sin base de datos externa.",
    version="0.1.0",
)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tutors")
def create_tutor(payload: TutorCreateRequest, service: TutoringService = Depends(get_service)) -> dict:
    try:
        tutor = service.register_tutor(**payload.model_dump())
        return {
            "id": tutor.id,
            "full_name": tutor.full_name,
            "email": tutor.email,
            "timezone": tutor.timezone,
            "hourly_rate": tutor.hourly_rate,
        }
    except DomainError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/tutors/{tutor_id}/students")
def create_student(
    tutor_id: str,
    payload: StudentCreateRequest,
    service: TutoringService = Depends(get_service),
) -> dict:
    try:
        student = service.register_student(tutor_id=tutor_id, **payload.model_dump())
        return {
            "id": student.id,
            "tutor_id": student.tutor_id,
            "full_name": student.full_name,
            "email": student.email,
            "goals": student.goals,
        }
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except DomainError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/lessons")
def schedule_lesson(payload: LessonScheduleRequest, service: TutoringService = Depends(get_service)) -> dict:
    try:
        lesson = service.schedule_lesson(**payload.model_dump())
        return {
            "id": lesson.id,
            "tutor_id": lesson.tutor_id,
            "student_id": lesson.student_id,
            "starts_at": lesson.starts_at.isoformat(),
            "duration_minutes": lesson.duration_minutes,
            "topic": lesson.topic,
            "status": lesson.status.value,
        }
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except DomainError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.patch("/lessons/{lesson_id}/complete")
def complete_lesson(
    lesson_id: str,
    payload: LessonCompleteRequest,
    service: TutoringService = Depends(get_service),
) -> dict:
    try:
        lesson = service.complete_lesson(lesson_id=lesson_id, notes=payload.notes)
        return {
            "id": lesson.id,
            "status": lesson.status.value,
            "notes": lesson.notes,
        }
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except DomainError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/tutors/{tutor_id}/dashboard")
def tutor_dashboard(tutor_id: str, service: TutoringService = Depends(get_service)) -> dict:
    try:
        return service.tutor_dashboard(tutor_id=tutor_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

