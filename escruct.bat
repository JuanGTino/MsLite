@echo off
:: Trabajar en la carpeta actual
SET CURRENT_DIR=%cd%

:: Crear estructura de carpetas
mkdir app
mkdir app\core
mkdir app\db
mkdir app\models
mkdir app\schemas
mkdir app\crud
mkdir app\api
mkdir app\api\v1
mkdir app\utils
mkdir tests

:: Crear archivos base
echo from fastapi import FastAPI> app\main.py
echo from fastapi import APIRouter>> app\api\v1\auth.py
echo from fastapi import APIRouter>> app\api\v1\items.py
echo # Configuración y variables de entorno>> app\core\config.py
echo # Seguridad y hashing>> app\core\security.py
echo # Conexión a la base de datos>> app\db\session.py
echo # Modelos de base de datos>> app\models\user.py
echo # Modelos de base de datos>> app\models\item.py
echo # Schemas Pydantic>> app\schemas\user.py
echo # Schemas Pydantic>> app\schemas\item.py
echo # Funciones CRUD>> app\crud\user.py
echo # Funciones CRUD>> app\crud\item.py
echo # Funciones auxiliares>> app\utils\helpers.py

:: Crear archivo requirements.txt
echo fastapi==0.100.0> requirements.txt
echo uvicorn[standard]==0.23.2>> requirements.txt
echo python-dotenv==1.0.0>> requirements.txt
echo sqlalchemy==2.0.22>> requirements.txt
echo pydantic==2.3.0>> requirements.txt
echo alembic==1.12.0>> requirements.txt
echo psycopg2-binary==2.9.9>> requirements.txt

:: Crear archivo .env
echo POSTGRES_USER=postgres> .env
echo POSTGRES_PASSWORD=postgres>> .env
echo POSTGRES_DB=fastapi_db>> .env
echo POSTGRES_HOST=localhost>> .env
echo POSTGRES_PORT=5432>> .env
echo SECRET_KEY=change_this_secret>> .env

echo Proyecto FastAPI inicializado correctamente en %CURRENT_DIR%.
pause
