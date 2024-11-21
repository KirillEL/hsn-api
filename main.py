import os
import uvicorn
from infra import config


def main():
    uvicorn.run(
        app="api.api_server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True,
        workers=1,
    )


if __name__ == "__main__":
    main()
