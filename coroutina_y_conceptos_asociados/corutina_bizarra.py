import asyncio  

async def esperar_cambio_de_canal():
    print("tic tac... tic tac... esperando...")
    await asyncio.sleep(5)  # segundos hasta que cambie
    print("¡Canal cambiado! 🎉")

asyncio.run(esperar_cambio_de_canal())
