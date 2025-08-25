# Sysacad Flask

Sistema académico desarrollado en **Flask**, Utilizando de base el sistema SYSACAD, que permite:

- Gestionar alumnos, universidades, planes, materias y cargos.  
- Generar certificados de alumnos regulares en formato **.docx** con plantillas.  
- Exponer un conjunto de **endpoints REST** para operar sobre los datos académicos.  

Este proyecto fue creado como proyecto universitario para la materia Desarrollo de Software, usando PostgreSQL como base de datos y Flask-Migrate para la gestión de esquemas.
## 2. Requerimientos e instalación

### 🔧 Requerimientos previos
- Python **3.12** o superior
- PostgreSQL (ej. `dev_sysacad`, `test_sysacad`)
- PowerShell (Windows) o bash/zsh (Linux/Mac)

---

### 📦 Crear el entorno virtual
En la raíz del proyecto, crear la carpeta `.venv`:

### Iniciar powershell, iniciarla como administrador
python -m venv .venv

### ⚡ Activar el entorno virtual
Windows (PowerShell):
.\.venv\Scripts\Activate

Linux / MacOS:
source .venv/bin/activate

Vas a ver algo como:

(.venv) PS \tu ruta\Sysacad>

### 📥 Instalar dependencias

El proyecto incluye un script install.ps1 que instala automáticamente los paquetes de requirements.txt.

Ejecutá:

.\install.ps1


⚠️ Problema común en PowerShell:
Si ves un error como “No se puede ejecutar el script porque no está firmado digitalmente”, desbloqueá el archivo y permití ejecución de scripts locales:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Unblock-File -Path .\install.ps1


y luego volvé a correr:

.\install.ps1

✅ Verificación

Después de instalar, comprobá que todo está correcto:

python -m pip list

Deberías ver Flask, SQLAlchemy y el resto de dependencias listadas.

## 3. Ejecución del proyecto

### ▶️ Usando Flask directamente

Con el entorno virtual activado:
Es importante que se cree su .env , en el archivo env-example, tiene que colocar su usario y contraseña
luego guardarlo como un archivo ".env"

## Luego en powershell
powershell
$env:FLASK_APP="app:create_app"
$env:FLASK_ENV="development"
flask run
Esto levantará el servidor en:

http://127.0.0.1:5000

## ▶️ Usando el script boot.ps1 (recomendado en Windows)

En la raíz del proyecto ejecutá:

.\boot.ps1

## Este script:

Activa el entorno virtual .venv.

Configura la variable FLASK_APP=app:create_app.

Arranca la aplicación con flask run.

## ⚠️ Problema común en PowerShell

Si aparece el error:

No se puede ejecutar el archivo .ps1 porque no está firmado digitalmente


## Solucionalo con:

Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
Unblock-File -Path .\boot.ps1


y volvé a correr:

.\boot.ps1

✅ Verificación

Si todo salió bien, deberías ver en consola algo como:

 * Serving Flask app 'app:create_app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 
## 4. Carga inicial de datos en la base

Una vez verificado que la aplicación levanta correctamente en `http://127.0.0.1:5000`, es necesario poblar la base de datos con información inicial.

---

### 📝 Crear archivo CSV con alumnos

El script `crear_csv.py` genera un archivo `alumnos.csv` con **2.5 millones de registros** de alumnos ficticios.

Ejecutar:

powershell
python crear_csv.py

### ⏱️ Este proceso demora aproximadamente 1 minuto en una PC de escritorio estándar.
Al finalizar, tendrás el archivo alumnos.csv en la raíz del proyecto.

### 📥 Importar los datos a la base de datos

Luego de generar el CSV, ejecutá el siguiente script:

python scripts/cargatodo.py


Este script:

Crea las tablas necesarias si no existen.

Importa todas las entidades académicas (universidades, facultades, planes, materias, etc.).

Inserta los 2.5 millones de alumnos en la tabla alumnos.

⚡ El proceso está optimizado con inserciones por lotes y puede tardar varios minutos dependiendo del hardware.

✅ Verificación

Una vez finalizado, podés comprobar la carga de todo desde pgadmin o SQL Shell

## 5. Endpoints principales

La API expone múltiples recursos en formato **REST** bajo el prefijo `/sys`.  
Los principales son:

---

### 👨‍🎓 Alumno
- `GET    /sys/alumno` → Listar todos los alumnos  
- `GET    /sys/alumno/<nro_legajo>` → Obtener un alumno por número de legajo  
- `POST   /sys/alumno` → Crear un alumno nuevo  
- `PUT    /sys/alumno/<nro_legajo>` → Actualizar un alumno existente  
- `DELETE /sys/alumno/<nro_legajo>` → Eliminar un alumno  

---

### 🏛️ Universidad
- `GET    /sys/universidad` → Listar todas las universidades  
- `GET    /sys/universidad/<id>` → Obtener una universidad por ID  
- `POST   /sys/universidad` → Crear una universidad nueva  
- `DELETE /sys/universidad/<id>` → Eliminar una universidad  

---

### 📄 Certificado
- `GET    /sys/certificado/<nro_legajo>/docx`  
  Genera y descarga un **Certificado de Alumno Regular** en formato **Word (.docx)**.  
  El archivo se construye dinámicamente a partir de una plantilla.

Ejemplo:

http://127.0.0.1:5000/sys/certificado/5/docx

Descargará un archivo DOCX con los datos del alumno de legajo **5**.

## 6. Licencia
Este proyecto se desarrolló con fines académicos en la UTN.

## Alumnos
Andino Nicolás , Legajo N°9935
Assenza Ezequiel , Legajo N° 9943
Lopez Matias , Legajo N° 10097
Orella Lucas , Legajo N° 10163


Luego de descargar , eliminar la carpeta de/Scripts
