import asyncio

from  _thread import get_ident
from greenlet import getcurrent as get_ident2
from asyncio import

def run():

    loop=asyncio.get_event_loop()
    loop.run_until_complete(init())

    return

async def init ():
    tasks=[asyncio.ensure_future(task()) for _ in range(10)]
    await asyncio.gather(*tasks)


async def task():
    print(get_ident())
    print(get_ident2())
    await asyncio.sleep(10)



run()