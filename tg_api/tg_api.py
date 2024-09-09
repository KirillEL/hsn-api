from loguru import logger

from infra import config
import requests


def send_telegram_message(message: str):
    if config.IS_BOT_ENABLED:
        url = f"https://api.telegram.org/bot{config.TG_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': config.TG_CHAT_ID,
            'text': message
        }
        try:
            requests.post(url, data=payload)
        except Exception as e:
            logger.error(f"Не удалось отправить сообщение в Telegram: {e}")
