import os
import uvicorn
from infra import config
from loguru import logger

def main():
    uvicorn.run(
        app="api.api_server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True,
        workers=1
    )
    log_file = os.getenv("LOG_FILE_PATH", "logs/errors.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger.add(
        log_file,
        level="ERROR",
        rotation="1 week",
        retention="1 month",
        compression="zip",
        backtrace=True,
        diagnose=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
    )


if __name__ == "__main__":
    main()
