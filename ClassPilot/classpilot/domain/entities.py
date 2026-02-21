from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class LessonStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELED = "canceled"


@dataclass(frozen=True)
class Tutor:
    id: str
    full_name: str
    email: str
    timezone: str
    hourly_rate: float


@dataclass(frozen=True)
class Student:
    id: str
    tutor_id: str
    full_name: str
    email: str
    goals: str


@dataclass(frozen=True)
class Lesson:
    id: str
    tutor_id: str
    student_id: str
    starts_at: datetime
    duration_minutes: int
    topic: str
    status: LessonStatus
    notes: str | None = None

