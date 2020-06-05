import asyncio

import uvicorn
from asyncpgsa import pg
from fastapi import FastAPI
from sqlalchemy import select

import settings
from db import Security
from parsers.moex.bonds.parser import parse


app = FastAPI()


async def background_parsing(interval):
    while True:
        await asyncio.sleep(interval)
        await parse()


@app.on_event("startup")
async def startup():

    asyncio.create_task(background_parsing(5*60))

    await pg.init(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )


@app.on_event("shutdown")
async def shutdown():
    await pg.pool.close()


@app.get("/securities/{security_isin}")
async def root(security_isin):
    query = select([Security]).where(Security.isin == security_isin.upper())
    result = await pg.fetchrow(query)

    return result


if __name__ == "__main__":
    uvicorn.run("api.app:app", host="127.0.0.1", port=8080, access_log=False)
