import asyncio
from datetime import datetime

async def coro_task(name, delay):
    print(f"{datetime.now().time()} - {name} start (async)")
    await asyncio.sleep(delay)
    print(f"{datetime.now().time()} - {name} end (async)")

async def run_concurrent():
    tasks = [
        asyncio.create_task(coro_task("Tarea A", 2)),
        asyncio.create_task(coro_task("Tarea B", 2)),
        asyncio.create_task(coro_task("Tarea C", 2)),
    ]
    await asyncio.gather(*tasks)

# en un script normal:
asyncio.run(run_concurrent())
# en algunos entornos interactivos (Jupyter) se usa: await run_concurrent()

# RUN SEQUENTIAL (blocking):
# 17:52:21.962 - Tarea A start (blocking)
# ... (fin Tarea A)
# ... (Tarea B start/end)
# ... (Tarea C start/end)
# Total elapsed: 0:00:06.00

# RUN CONCURRENT (async):
# 17:52:27.964 - Tarea A start (async)
# 17:52:27.965 - Tarea B start (async)
# 17:52:27.965 - Tarea C start (async)
# 17:52:29.966 - Tarea A end (async)
# 17:52:29.966 - Tarea B end (async)
# 17:52:29.966 - Tarea C end (async)
# Total elapsed: 0:00:02.00

