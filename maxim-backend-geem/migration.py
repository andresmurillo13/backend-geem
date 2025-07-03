import asyncio

from geem import run


async def run_migration():
    await run(generate_schemas=True)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_migration())
    loop.close()
