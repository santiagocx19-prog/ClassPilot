# Arquitectura de ClassPilot

## Vision general

El sistema implementa una arquitectura limpia en cuatro capas para mantener separadas reglas de negocio y detalles tecnicos.

## Capas

### 1. Domain

- Entidades: `Tutor`, `Student`, `Lesson`.
- Estados: `LessonStatus`.
- Excepciones de negocio: `ValidationError`, `NotFoundError`.
- Contratos de persistencia: interfaces de repositorios.

### 2. Application

- Caso de uso central: `TutoringService`.
- Orquesta validaciones de negocio y coordina repositorios.
- No conoce FastAPI ni formato JSON de almacenamiento.

### 3. Infrastructure

- `JsonFileStore`: acceso al archivo de datos.
- Repositorios JSON concretos:
  - `JsonTutorRepository`
  - `JsonStudentRepository`
  - `JsonLessonRepository`
- Escritura atomica con archivo temporal + replace.

### 4. Presentation

- API REST en FastAPI (`classpilot/presentation/api.py`).
- Convierte payload HTTP en llamadas a casos de uso.
- Mapea errores de dominio a codigos HTTP.

## Flujo principal

1. Cliente llama un endpoint REST.
2. FastAPI crea el servicio de aplicacion con repositorios JSON.
3. El caso de uso valida reglas y persiste cambios.
4. API devuelve respuesta serializada.

## Trade-offs de no usar DB externa

Ventajas:

- Operacion simple.
- Costo operativo minimo.
- Arranque rapido para MVP.

Limitaciones:

- Concurrencia limitada.
- Sin consultas avanzadas.
- Escalabilidad horizontal reducida.

## Evolucion recomendada

Para escalar:

1. Mantener dominio y aplicacion sin cambios.
2. Reemplazar solo `infrastructure` por Postgres + SQLAlchemy.
3. Conservar la API y la logica de negocio.

