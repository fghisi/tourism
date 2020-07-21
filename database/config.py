import asyncpg

from fastapi import FastAPI

from environment import (
    get_host,
    get_database,
    get_port,
    get_user,
    get_password
)


async def connect_database(application: FastAPI) -> None:
    application.state.pool = await asyncpg.create_pool(
        host=get_host(),
        port=get_port(),
        user=get_user(),
        password=get_password(),
        database=get_database(),
    )


async def close_database_connection(application: FastAPI) -> None:
    await application.state.pool.close()