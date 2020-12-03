import sqlalchemy as sa
import uvicorn
from asyncpgsa import pg
from fastapi import FastAPI
from starlette.responses import UJSONResponse

from db import Security
from db import connect_db
from db import disconnect_db


app = FastAPI(default_response_class=UJSONResponse)


@app.on_event('startup')
async def startup():
    await connect_db()


@app.on_event('shutdown')
async def shutdown():
    await disconnect_db()


@app.get('/securities/{security_isin}')
async def root(security_isin: str, currency: str = 'SUR'):
    query = sa.select([Security]).where(
        sa.and_(
            Security.isin == security_isin.upper(),
            Security.currency == currency.upper(),
        )
    )
    result = await pg.fetchrow(query)

    return result


if __name__ == '__main__':
    uvicorn.run('api.app:app', host='127.0.0.1', access_log=False, reload=True)
