# ClassPilot 🍎 
### Sistema de Gestión para Tutores Particulares

**ClassPilot** es una solución robusta diseñada para ayudar a profesores particulares a gestionar su flujo de trabajo, desde el seguimiento de alumnos hasta la programación de clases y el control de ingresos, todo bajo una arquitectura limpia y moderna.

---

## 🚀 Características Principales
* **Gestión de Alumnos:** Registro y seguimiento detallado de estudiantes.
* **Programación de Clases:** Calendario de sesiones con estados (pendiente, completada, cancelada).
* **Control de Ingresos:** Dashboard con cálculo automático de ganancias estimadas y reales.
* **Persistencia Atómica:** Sistema de almacenamiento en JSON con escritura segura para evitar la corrupción de datos.
* **API RESTful:** Documentación interactiva automática integrada.

---

## 🏗️ Arquitectura
El proyecto sigue los principios de **Clean Architecture**, dividiendo las responsabilidades en capas para garantizar la escalabilidad y facilidad de prueba:

* **Domain:** Entidades y reglas de negocio puras.
* **Application:** Servicios de orquestación (Use Cases).
* **Infrastructure:** Implementación de repositorios y persistencia de datos.
* **Presentation:** Capa de API construida con **FastAPI**.

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.x
* **Framework Web:** FastAPI
* **Validación de Datos:** Pydantic
* **Testing:** Pytest
* **Almacenamiento:** JSON con manejo de archivos atómicos.

---

## ⚙️ Instalación y Uso

1. **Clona el repositorio:**
   ```bash git clone https://github.com/santiagocx19-prog/ClassPilot.git
  
