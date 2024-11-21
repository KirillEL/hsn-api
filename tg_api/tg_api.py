from typing import Any

from loguru import logger

from infra import config
import requests


class TelegramBot:
    def __init__(self, bot_token: str, chat_id: str, is_enabled: bool = False) -> None:
        """
        Инициализация бота Telegram.
        :param bot_token: Токен бота Telegram.
        :param chat_id: ID чата или пользователя, куда будут отправляться сообщения.
        :param is_enabled: Включен ли бот (по умолчанию False).
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.is_enabled = is_enabled
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_message(self, message: str, parse_mode: str = "Markdown") -> None:
        if self.is_enabled:
            url: str = f"{self.base_url}/sendMessage"
            payload: dict[str, Any] = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode,
            }
            try:
                response = requests.post(url, data=payload)
                response.raise_for_status()
                logger.info(f"Message successfully sent: {message}")
            except requests.exceptions.RequestException as re:
                logger.error(f"Не удалось отправить сообщение: {re}")
                raise re
        else:
            logger.warning(f"Bot is disabled, message didnt send")


tg_bot: TelegramBot = TelegramBot(
    bot_token=config.TG_BOT_TOKEN,
    is_enabled=config.IS_BOT_ENABLED,
    chat_id=config.TG_CHAT_ID,
)
