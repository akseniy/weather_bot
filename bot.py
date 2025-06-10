import asyncio
import logging


from middlewares.throttling import ThrottlingMiddleware
from database.data import data_router
from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from main_bot_handlers import handlers
from aiogram.fsm.storage.redis import RedisStorage, Redis
from asyncpg import create_pool



async def main():
    logging.basicConfig(level=logging.INFO, filename='py_log.log', filemode='w')

    # Загружаем конфиг в переменную config
    config: Config = load_config()


    # Инициализируем бот, диспетчер, redis и коннект к базе данных
    bot = Bot(token=config.tg_bot.token)
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)
    main_dp = Dispatcher(storage=storage)
    pool = await create_pool(user=config.db.db_user, database=config.db.database, host=config.db.db_host, port=config.db.db_port)


    # Добавляем пул для общей видимости по проекту
    main_dp.workflow_data.update({'admin_token': config.weather.token, 'pool': pool})



    # Подключаем middleware
    main_dp.message.middleware(ThrottlingMiddleware())


    # Регистриуем роутеры на диспетчере для основного бота

    main_dp.include_router(data_router)
    main_dp.include_router(handlers.base_router)


    await main_dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())