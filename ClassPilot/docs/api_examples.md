# Ejemplos de API

## 1) Crear profesor

```bash
curl -X POST http://127.0.0.1:8000/tutors ^
  -H "Content-Type: application/json" ^
  -d "{\"full_name\":\"Ana Ruiz\",\"email\":\"ana@example.com\",\"timezone\":\"UTC\",\"hourly_rate\":35}"
```

## 2) Crear alumno

```bash
curl -X POST http://127.0.0.1:8000/tutors/{tutor_id}/students ^
  -H "Content-Type: application/json" ^
  -d "{\"full_name\":\"Lucas\",\"email\":\"lucas@example.com\",\"goals\":\"Algebra\"}"
```

## 3) Programar clase

```bash
curl -X POST http://127.0.0.1:8000/lessons ^
  -H "Content-Type: application/json" ^
  -d "{\"tutor_id\":\"{tutor_id}\",\"student_id\":\"{student_id}\",\"starts_at\":\"2026-03-10T18:00:00+00:00\",\"duration_minutes\":60,\"topic\":\"Ecuaciones cuadraticas\"}"
```

## 4) Completar clase

```bash
curl -X PATCH http://127.0.0.1:8000/lessons/{lesson_id}/complete ^
  -H "Content-Type: application/json" ^
  -d "{\"notes\":\"Buen avance en factorizacion\"}"
```

## 5) Ver dashboard del profesor

```bash
curl http://127.0.0.1:8000/tutors/{tutor_id}/dashboard
```

