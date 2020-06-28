import asyncio
import logging
import signal
from asyncio import CancelledError

from db import connect_db
from db import disconnect_db
from parsers.moex.bonds import parsers as moex_bond_parsers
from settings import PARSING_INTERVAL


logger = logging.getLogger('parser.app')


async def shutdown(signal, loop):
    logger.info(f'Received exit signal {signal.name}...')

    tasks = [
        t for t in asyncio.all_tasks()
        if t is not asyncio.current_task()
    ]

    for task in tasks:
        task.cancel()

    logger.debug(f'Cancelling {len(tasks)} outstanding tasks')

    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


def add_shutdown_handler():
    loop = asyncio.get_event_loop()
    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s,
            lambda s=s: asyncio.create_task(shutdown(s, loop))
        )


async def parsing_task(coro, interval):
    while True:
        await coro()
        await asyncio.sleep(interval)


async def background_parsing(interval):
    add_shutdown_handler()

    await connect_db()

    parsers = moex_bond_parsers

    parsing_tasks = [
        asyncio.create_task(parsing_task(coro, interval))
        for coro in parsers
    ]

    try:
        await asyncio.wait(parsing_tasks)
    except CancelledError:
        logger.debug(f'Parsing task cancelled, disconnecting db...')
        await disconnect_db()

asyncio.run(background_parsing(PARSING_INTERVAL))
