
# Análisis de Vulnerabilidades de redes Wi-fi y aulas virtuales mediante Ataque de Fuerza Bruta


Este proyecto es un simulador de ataque de fuerza bruta, desarrollado como parte de un curso académico. Utiliza una interfaz gráfica creada con "customtkinter".

## Funcionalidades

- **Configuración Personalizada del Ataque**: Los usuarios pueden definir los parámetros del ataque, como la longitud mínima y máxima de la contraseña.

- **Generación Automática de Contraseñas**: El simulador genera todas las combinaciones posibles de contraseñas según los parámetros establecidos.

- **Simulación de Ataque de Fuerza Bruta**: Realiza un ataque probando todas las combinaciones generadas hasta encontrar la contraseña correcta.

- **Interfaz Gráfica Interactiva**: Permite a los usuarios visualizar el progreso del ataque y controlar el simulador.

- **Progreso en Tiempo Real**: Muestra el número de intentos realizados y el tiempo estimado para completar el ataque.

- **Soporte para Caracteres Especiales**: Permite la inclusión de caracteres especiales en las contraseñas.

- **Registros Detallados**: Los intentos se registran detalladamente para su posterior análisis.

## Tecnologías

- **Python 3.x**: Lenguaje de programación principal para el desarrollo del simulador de ataque de fuerza bruta.

- **customtkinter**: Biblioteca para crear interfaces gráficas modernas basadas en `tkinter`.

- **Pillow (PIL)**: Biblioteca utilizada para la manipulación de imágenes (por ejemplo, para mostrar imágenes en la interfaz gráfica).

- **pywifi**: Librería para interactuar con redes Wi-Fi y realizar pruebas de seguridad.

- **requests**: Utilizada para hacer solicitudes HTTP.

- **beautifulsoup4**: Biblioteca para web scraping y extracción de datos.

- **Threading (módulo estándar de Python)**: Utilizado para mejorar el rendimiento y realizar múltiples intentos de ataque en paralelo. 

- **Git**: Control de versiones utilizado para gestionar el código fuente del proyecto.

- **GitHub**: Plataforma para almacenar el código fuente y facilitar la colaboración.

## Integrantes del Proyecto 

Este proyecto fue realizado por los siguientes integrantes:

- **Benites Marin Martin Alberto**
- **Quispe Quispe Brayan Alonso Plácido**
- **Ríos Gonzáles Jesús Oswaldo Andrés**
- **Rosado Silva Manzur Arturo**
- **Torres Reyes Sebastian David**

## Agradecimientos

Este proyecto fue desarrollado bajo la supervisión del Profesor **Tello Canchapoma Yury Oscar**, quien proporcionó la orientación y el apoyo necesario durante todo el desarrollo. Agradecemos profundamente su ayuda en la planificación y ejecución del proyecto.

- **Profesor**: Tello Canchapoma Yury Oscar
- **Institución**: Universidad Nacional de Ingeniería

## Screenshots

Inicio de sesion

![App Screenshot](https://github.com/user-attachments/assets/c0202cee-c3bd-4d52-86eb-4f1f6b5b9f7a)

Opciones

![App Screenshot](https://github.com/user-attachments/assets/53366432-08d6-4cda-94e5-d7b5d50c07f7)

Análisis de Formularios web

![App Screenshot](https://github.com/user-attachments/assets/072dda2a-10fe-45ac-9243-337833addaf5)

Análisis de Redes Wi-fi

![App Screenshot](https://github.com/user-attachments/assets/afc9f905-a5b8-44db-92ac-a963a8fbc686)

## Dependencias

Este proyecto requiere las siguientes bibliotecas de python:

- `customtkinter`: Para crear interfaces gráficas personalizadas.
- `Pillow` (PIL): Para manejar imágenes.
- `pywifi`: Para interactuar con redes Wi-Fi.
- `requests`: Para hacer solicitudes HTTP.
- `beautifulsoup4`: Para hacer web scraping.

Puedes instalar todas las dependencias necesarias ejecutando el siguiente comando:

```bash
pip install -r requirements.txt
```


## Requisitos

Este proyecto está diseñado para funcionar con Python 3.6 o versiones posteriores, incluyendo Python 3.12.7.
## Verificación de la versión de Python

```bash
  python --version
```
## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto en tu máquina local.

### 1. Clonar el repositorio

Primero, necesitas clonar el repositorio en tu máquina. Abre una terminal y ejecuta el siguiente comando:

```bash
git clone https://github.com/sebastian0502/Analisis-de-Vulnerabilidades.git
```

### 2. Acceder al directorio del proyecto

Una vez que hayas clonado el repositorio, accede al directorio del proyecto:

```bash
cd Analisis-de-Vulnerabilidades
```

### 3. Instalar las dependencias

Con el repositorio clonado, instala todas las dependencias necesarias para ejecutar el proyecto. Ejecuta este comando:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar el proyecto

Ahora que todas las dependencias están instaladas, puedes ejecutar el script principal del proyecto. Para hacerlo, ejecuta el siguiente comando:

```bash
python aplicacion.py
```
Esto iniciará la aplicación y abrirá la interfaz gráfica.
## Uso

Una vez que hayas instalado las dependencias y ejecutado el proyecto, la aplicación estará lista para ser utilizada.

### 1. Iniciar Sesión

Para poder usar el simulador de ataque de fuerza bruta, primero debes iniciar sesión. El programa requiere un **usuario** y **contraseña** específicos para acceder a la interfaz.

- **Nombre de usuario**: `Grupo01`
- **Contraseña**: `123456789`

1. Al abrir la aplicación, aparecerá una pantalla de inicio de sesión.
2. Introduce el **nombre de usuario** y la **contraseña** proporcionados.
3. Haz clic en el botón **"Iniciar Sesión"** para acceder al simulador de ataque de fuerza bruta.

Una vez hayas iniciado sesión, podrás configurar los parámetros del ataque y comenzar a usar la herramienta.
## Documentation

Para obtener detalles técnicos sobre la estructura del código y las funciones principales, puedes acceder a la documentación completa a través del siguiente enlace:

[Documentation](https://github.com/user-attachments/files/17966934/Documentacion.docx)

