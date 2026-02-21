# ClassPilot

Sistema de gestion orientado a profesores particulares (estilo SaaS), construido con **arquitectura limpia** y persistencia local en JSON, sin base de datos externa.

## Objetivo del proyecto

ClassPilot cubre un flujo real de negocio:

- Alta de profesores.
- Alta de alumnos por profesor.
- Programacion de clases.
- Cierre de clases con notas.
- Dashboard simple por profesor (alumnos, clases futuras e ingreso estimado del mes).

## Stack

- Python 3.10+
- FastAPI (API HTTP)
- Persistencia en archivo JSON (`data/classpilot.json`)
- Pytest (tests basicos)

## Arquitectura limpia

Estructura:

- `classpilot/domain`: entidades, reglas y contratos de repositorio.
- `classpilot/application`: casos de uso (servicio de negocio).
- `classpilot/infrastructure`: implementacion de repositorios sobre JSON.
- `classpilot/presentation`: API REST con FastAPI.

La capa de aplicacion depende de abstracciones del dominio y no de detalles de infraestructura.

## Instalacion

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
```

## Ejecucion

```bash
python main.py
```

API disponible en `http://127.0.0.1:8000` y docs en `http://127.0.0.1:8000/docs`.

## Endpoints principales

- `POST /tutors`
- `POST /tutors/{tutor_id}/students`
- `POST /lessons`
- `PATCH /lessons/{lesson_id}/complete`
- `GET /tutors/{tutor_id}/dashboard`
- `GET /health`

## Tests

```bash
pytest -q
```

## Notas de persistencia

- No se usa base de datos externa.
- Los datos se guardan en JSON con escritura atomica para reducir corrupcion de archivo.
- Este enfoque es ideal para MVPs, demos o despliegues de bajo volumen.

## Documentacion adicional

- `docs/architecture.md`
- `docs/api_examples.md`

