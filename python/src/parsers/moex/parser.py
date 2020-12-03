import asyncio
import functools
import logging
from concurrent.futures.process import ProcessPoolExecutor
from datetime import datetime

import aiohttp
from asyncpgsa import pg
from lxml import etree
from sqlalchemy.dialects import postgresql

from db import Security


logger = logging.getLogger('parser.app')


def parse_xml_data(xml_data):
    result = []

    root = etree.fromstring(xml_data)
    securities = root.xpath('/document/data[@id="securities"]/rows/row')
    for security in securities:
        code = security.get('SECID')
        data = dict(security.attrib)

        result.append((code, data))

    return result


async def process_response(response_data):
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, functools.partial(parse_xml_data, response_data)
        )

    return result


async def parse(url, description):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:

            logger.info(f'Parsing started: {description}')
            logger.debug(f'Parsing url: {url}')

            response_data = await resp.read()

            now = datetime.utcnow()

            values = [
                {
                    Security.isin.name: code,
                    Security.data.name: data,
                    Security.last_updated.name: now,
                    Security.currency.name: data['CURRENCYID'],
                }
                for code, data in await process_response(response_data)
            ]

            insert_stmt = postgresql.insert(Security).values(values)
            update_columns = {
                col.name: col
                for col in insert_stmt.excluded
                if col.name not in (Security.isin.name,)
            }
            on_conflict_update_stmt = insert_stmt.on_conflict_do_update(
                index_elements=[Security.isin, Security.currency],
                set_=update_columns,
            )

            await pg.fetchrow(on_conflict_update_stmt)

            logger.info(f'Parsing finished: {description}')
