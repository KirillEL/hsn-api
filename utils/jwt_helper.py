import jwt
from datetime import datetime, timedelta
from infra import config


def jwt_encode(payload: dict, expire_period: int = 36000) -> str:
    token = jwt.encode(payload={
        **payload,
        "exp": datetime.utcnow()
               + timedelta(seconds=expire_period)}, key=config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    return token


def jwt_decode(token: str) -> dict:
    try:
        return jwt.decode(token, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)
    except jwt.exceptions.DecodeError as e:
        raise e
    except jwt.exceptions.ExpiredSignatureError as ex:
        raise ex

