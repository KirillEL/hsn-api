import os
import shutil
import subprocess

from fastapi import UploadFile, File, HTTPException
from loguru import logger
from starlette.responses import JSONResponse

from api.exceptions import ExceptionResponseSchema
from infra import config
from .router import db_router
from shared.db.db_session import SessionContext

UPLOAD_DIR = "/tmp/uploads"

# Ensure the upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)


@db_router.post(
    "/upload_dump",
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_db_upload_dump(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        env = os.environ.copy()
        env["PGPASSWORD"] = config.DB_PASSWORD

        restore_command = (
            f"pg_restore -U {config.DB_USER} -h {config.DB_SERVER} -p {config.DB_PORT} "
            f"-d {config.DB_NAME} --clean --if-exists {file_location}"
        )

        restore_process = subprocess.run(restore_command, shell=True, check=True, text=True, capture_output=True,
                                         env=env)
        logger.debug(f'restore_process: {restore_process}')

        if restore_process.returncode != 0:
            raise HTTPException(status_code=500, detail="Ошибка при применении дампа базы данных")

        return JSONResponse(content={"filename": file.filename, "location": file_location})

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при выполнении команды: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Непредвиденная ошибка: {str(e)}")
