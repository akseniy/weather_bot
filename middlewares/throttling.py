import time
from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=3.0, key_prefix='antiflood_'):
        self.limit = limit  # Минимальное время между сообщениями в секундах
        self.key_prefix = key_prefix
        self.users = {}  # Словарь для хранения времени последнего сообщения
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
            event: types.Message,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = time.time()

        # Проверяем, когда пользователь последний раз отправлял сообщение
        last_time = self.users.get(user_id, 0)

        if current_time - last_time < self.limit:
            # Сообщение пришло слишком быстро - игнорируем
            await event.answer("Слишком много запросов! Пожалуйста, подождите...")
            return

        # Обновляем время последнего сообщения
        self.users[user_id] = current_time

        # Пропускаем сообщение в обработчик
        return await handler(event, data)