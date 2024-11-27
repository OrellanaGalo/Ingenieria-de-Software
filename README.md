# Gestión de Base de Datos Personal

Este repositorio contiene un programa en Python que interactúa con una base de datos SQLite para gestionar datos personales. La aplicación permite crear una base de datos, importar datos desde un archivo CSV, consultar registros por DNI y exportar los datos a un nuevo archivo CSV. Se utiliza la librería `sqlite3` para gestionar la base de datos y `tkinter` para la interfaz gráfica de usuario.

## Funcionalidades

El programa implementa las siguientes funcionalidades:

1. **Crear Base de Datos**: Se crea una base de datos llamada `personal.db` con una tabla `personal` que almacena la información de los empleados o personas.
2. **Importar Datos**: Los datos del archivo CSV `basepersonal-csv-Galo.txt` se importan a la base de datos `personal.db`. El archivo debe contener las columnas necesarias para completar la tabla en la base de datos.
3. **Consultar Datos**: Los usuarios pueden consultar los datos almacenados en `personal.db` utilizando el DNI como clave de búsqueda.
4. **Exportar Datos**: Los datos de la base de datos `personal.db` se pueden exportar a un archivo CSV llamado `basepersonal-csv-export.txt`.

## Requisitos

- Python 3.x
- `sqlite3` (Incluido en la biblioteca estándar de Python)
- `tkinter` (Para la interfaz gráfica)

## Uso

1. **Crear la base de datos**: El programa crea automáticamente la base de datos `personal.db` cuando se ejecuta por primera vez.
2. **Importar Datos**: Selecciona el archivo CSV `basepersonal-csv-Galo.txt` para importar los datos a la base de datos.
3. **Consultar Datos**: Ingresa un DNI en la interfaz para consultar los datos de una persona.
4. **Exportar Datos**: Exporta los registros de la base de datos a un nuevo archivo CSV `basepersonal-csv-export.txt`.

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu_usuario/gestion_base_datos_personal.git
   ```

2. Navega a la carpeta del proyecto:

    ```bash
   cd gestion_base_datos_personal
   ```

3. Ejecuta el programa:

    ```bash
   python script_db.py
   ```

## Contribuciones

Si deseas contribuir a este proyecto, por favor abri un issue o un pull request con tus cambios.