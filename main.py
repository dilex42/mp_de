import asyncio
import script


async def periodic():
    sleep_min = 1
    while True:
        try:
            script.parse()
            print(f"Going to sleep for {sleep_min} minute(s)")
        except Exception as err:
            print(err)
            print(
                f"!!! Something went wrong !!! Retrying in {sleep_min} minute(s)"
            )
        await asyncio.sleep(sleep_min * 60)


loop = asyncio.get_event_loop()
task = loop.create_task(periodic())

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass
