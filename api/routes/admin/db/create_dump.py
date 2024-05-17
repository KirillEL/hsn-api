import subprocess
import os
from datetime import datetime

from loguru import logger
from starlette.responses import FileResponse

from infra import config
from .router import db_router
from api.exceptions import ExceptionResponseSchema
from shared.db.db_session import db_session, SessionContext
from fastapi import Request, HTTPException


@db_router.get(
    "/get_dump",
    responses={"400": {"model": ExceptionResponseSchema}}
)
@SessionContext()
async def admin_db_get_dump(request: Request):
    try:


        env = os.environ.copy()
        env["PGPASSWORD"] = config.DB_PASSWORD

        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        dump_file_path = f"/tmp/db-dump-{current_time}.dump"

        command = f"pg_dump -U {config.DB_USER} -h {config.DB_SERVER} -p {config.DB_PORT} -F c -b -v -f {dump_file_path} {config.DB_NAME}"

        process = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, env=env)
        if not os.path.exists(dump_file_path):
            raise HTTPException(status_code=500, detail="Ошибка при создании дампа базы данных")

        return FileResponse(dump_file_path, filename=f"db-dump-{current_time}.dump")

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при выполнении команды: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Непредвиденная ошибка: {str(e)}")
