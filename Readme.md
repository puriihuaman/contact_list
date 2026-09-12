# Agenda de contacto

## Descripción General

Una aplicación interactiva de línea de comandos (CLI) para gestionar la agenda de contactos de una persona usando un
sistema CRUD (Crear, Leer, Actualizar, Eliminar).

## Funcionalidades Principales (Requerimientos)

La aplicación debe ser capaz de:

- **Gestionar usuarios (CRUD)**: Crear, leer, actualizar y eliminar contactos.
- **Campos requeridos**: Nombre, Número de teléfono, Correo electrónico y Categoría (ej. Familia, Trabajo, Amigos).
- **Búsqueda parcial**: Capacidad de buscar contactos ingresando solo una parte del nombre, correo o teléfono (ej.
  buscar "mar" devolverá "María", "Omar", etc.).
- **Visualización**: Mostrar una lista formateada con todos los contactos almacenados.
- **Simulación de llamada**: Opción para "llamar" a un contacto registrado.
- **Validación**:
    - Los datos no pueden estar vacíos.
    - El número de teléfono debe ser único (no se puede registrar el mismo número en dos contactos diferentes).
- **Manejo de Errores (EAFP)**: El sistema atrapa excepciones nativas de Python (`ValueError`) para evitar caídas del
  programa ante entradas inválidas del usuario.
- **Excepciones de Negocio**: Implementación de errores personalizados (ej. `TelefonoDuplicadoError`) para proteger la
  integridad de los datos.
- **Auditoría de Tiempo**: Uso del módulo `datetime` para registrar la fecha de creación y última actualización de cada
  contacto.
- **Fechas Humanizadas**: Interfaz amigable que muestra el tiempo relativo (ej. "Creado hace 2 horas") en lugar de
  fechas en formato crudo.
- **Sistema de Autenticación Multiusuario**:
    - Registro de usuarios con validación de contraseña (mínimo 6 caracteres) y confirmación de contraseña.
    - Inicio de sesión con bloqueo de cuenta: Si un usuario falla la contraseña 3 veces consecutivas, su cuenta se
      bloquea por seguridad y el sistema regresa al menú principal.
    - Privacidad de datos (Multi-tenant): Cada usuario registrado tiene su propia agenda de contactos independiente.
      Ningún usuario puede ver o editar los contactos de otro.

## Arquitectura y Conceptos Técnicos

- **Paradigma**: El proyecto está construido bajo el paradigma de **Programación Orientada a Objetos (POO)**, aplicando
  principios de encapsulamiento, composición y abstracción.
- **Encapsulamiento**: Protección estricta de datos sensibles. Los atributos críticos (como contraseñas y el estado de
  bloqueo) son privados (ej. `__password`, `__is_locked`) y solo son accesibles a través de decoradores `@property`
  (Getters/Setters).
- **Modelado de Clases Principales**:
    - `Contacto`: Entidad que encapsula los datos personales de un contacto y automatiza sus fechas de auditoría
      (`datetime`).
    - `Agenda`: Controlador instanciable que contiene la lógica CRUD. Gestiona y protege una lista privada de objetos
      `Contacto`.
    - `Usuario`: Entidad que encapsula las credenciales y el estado de la cuenta. **(Composición)** Cada usuario posee
      su propia instancia exclusiva de la clase `Agenda`, aislando sus datos de los demás usuarios.
    - `AuthManager`: Clase estática que actúa como base de datos central en memoria. Gestiona el registro, validación de
      inicios de sesión y políticas de seguridad (bloqueo por 3 intentos).
- **Manejo de Errores (EAFP)**:
    - Implementación de filosofía *EAFP* (Es más fácil pedir perdón que permiso) en las entradas del usuario.
    - Creación de excepciones personalizadas (`UsuarioBloqueadoError`, `TelefonoDuplicadoError`,
      `UsuarioNoEncontradoError`) para delegar el manejo de la lógica de negocio a la capa de interfaz.
- **Modularidad (Ficheros)**:
    - `src/main.py`: Punto de entrada y orquestador de las fases (Autenticación -> CRUD).
    - `src/ui.py`: Capa de presentación. Maneja menús, formatos (fechas relativas) y atrapa (`try/except`) las excepciones.
    - `src/models/`: Definición de las clases base (`Contacto`, `Agenda`, `Usuario`).
    - `src/auth_manager.py`: Definición de la clase estática `AuthManager`.
    - `src/exceptions/blocked_user_error.py`: Clases de errores personalizados que heredan de `Exception`.
    - `src/config.py`: Constantes globales (ej. `CATEGORIES`).

## Flujo de Ejecución

- **Fase 1: Autenticación**
    - El programa inicia y muestra el menú de seguridad:

        - [1] Iniciar sesión
        - [2] Registrarse
        - [0] Salir

    - El usuario se registra (Nombre de usuario, email, contraseña, confirmar contraseña).
    - El usuario inicia sesión. Si falla 3 veces, su usuario se bloquea temporalmente. Si acierta, pasa a la Fase 2.


- **Fase 2: Agenda de contactos (CRUD)**

    - Se muestra el menú principal de la agenda (solo con los contactos del usuario activo).
    - El usuario puede Crear, Leer, Actualizar o Eliminar *sus* contactos.
    - Al elegir "Cerrar sesión", el programa regresa a la Fase 1.

## Roadmap del Proyecto (Futuras versiones)

- `v1.0 (Completada)`: CRUD funcional en memoria y uso de funciones de orden superior (`filter`, `map`).
- `v2.0 (Actual)`: Integración de manejo de errores robusto (`try/except`), creación de excepciones personalizadas y
  auditoría de tiempo con el módulo `datetime`.
- `v3.0 (Futura)`: Persistencia de datos mediante lectura y escritura de archivos (`.txt` o `.json`)