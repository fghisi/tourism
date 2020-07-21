from fastapi import FastAPI, Form

from database.config import connect_database, close_database_connection

from controller import router


def start_application(application: FastAPI):
    async def start() -> None:
        await connect_database(application)
    return start


def stop_application(application: FastAPI):
    async def stop() -> None:
        await close_database_connection(application)
    return stop


def get_application() -> FastAPI:
    application = FastAPI()

    application.add_event_handler("startup", start_application(application))
    application.add_event_handler("shutdown", stop_application(application))

    application.include_router(router)
    
    return application

app = get_application()