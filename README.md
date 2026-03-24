# 📅 Learn Months - Aventuras con los Meses 🦉

¡Bienvenido a **Aventuras con los Meses**! Una aplicación educativa interactiva desarrollada en Python diseñada para ayudar a los niños a aprender, practicar y dominar los meses del año de una forma divertida y dinámica.

## 🚀 Características Principales

- **Sistema de Usuarios y Persistencia:** Registro e inicio de sesión con base de datos SQLite. Guarda el progreso y los récords de cada estudiante de forma individual.
- **Módulo "Aprender":** Interfaz interactiva para escuchar la pronunciación de los meses mediante síntesis de voz (TTS).
- **Módulo "Test":** Evaluación de conocimientos con selección múltiple.
- **Módulo "Ordenar":** Desafío de lógica para organizar los meses cronológicamente.
- **Mascota Guía Inteligente:** Un búho guía que ofrece retroalimentación en tiempo real basada en el desempeño del usuario.
- **Generador de Diplomas:** Sistema de recompensa que genera un certificado de "Maestro del Tiempo" (Canvas interactivo) al alcanzar la puntuación máxima en ambos juegos.

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** Python 3.x
- **Interfaz Gráfica:** Tkinter
- **Base de Datos:** SQLite3
- **Procesamiento de Imágenes:** Pillow (PIL)
- **Síntesis de Voz:** Pyttsx3

## 📦 Requisitos e Instalación

Para que la aplicación funcione correctamente, asegúrate de tener instaladas las siguientes librerías de Python. Puedes instalarlas ejecutando los siguientes comandos en tu terminal:

```bash
pip install Pillow
pip install pyttsx3
La aplicación crea automáticamente el archivo de la base de datos progreso_meses.db al ejecutarse por primera vez, por lo que no es necesario configurar servidores externos.

🎮 Cómo Ejecutar
Clona este repositorio o descarga el código fuente.

Abre una terminal en la carpeta del proyecto.

Ejecuta el comando:

Bash
python main.py
📊 Estructura de la Base de Datos
La tabla usuarios gestiona la siguiente información:

usuario: Nombre único del alumno.

contrasena: Clave de acceso.

record_test: Máxima puntuación en el cuestionario (0-10).

record_ordenar: Máxima puntuación en el juego de orden (0-12).

ultima_conexion: Registro histórico de actividad.
