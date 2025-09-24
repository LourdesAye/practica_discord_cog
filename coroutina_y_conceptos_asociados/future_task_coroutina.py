# PYTHON: ASYNCIO + FUTURE + TASK + COROUTINA
    # En este archivo encontraremos ejmplo de: 
        # Future puro (Future() + set_result)
        # Future con await
        # Task como ejecutor de corutina

# FUTURE
    # Un Future es un objeto que representa un resultado que estará disponible en el futuro.
    # suele ser el resultado de una operación asincrónica (por ejemplo, una consulta a una API).
    # Es como una caja vacía que promete tener un resultado en el futuro (o un error).
    # Dice: “acá voy a guardar el resultado cuando esté listo”.

# Diferencia entre Future y Task
    # Future = contenedor del resultado.
    # Task = ejecuta una corutina en el event loop y expone su resultado como un Future. 
        # toda Task es un Future, pero no todo Future es una Task. 
        # raramente se instancia un Future directamente con Future(). Lo más habitual es trabajar con asyncio.create_task() 
        # o funciones de asyncio (asyncio.sleep, asyncio.gather, etc.) que ya manejan los Future internamente.

# LIBRERIAS NECESARIAS PARA LOS PRÓXIMOS DOS EJEMPLOS
import asyncio # se importa el módulo asyncio completo
from asyncio import Future # se importa la clase Future del módulo asyncio

# EJEMPLO BÁSICO FUTURE
# se declara la corutina main con async def
async def main(): 
    my_future = Future() # se crea un objeto Future, que todavía no posee un valor
    print(my_future.done())  # done() controla el estado del Future: devuelve False porque no tiene valor
    my_future.set_result('Bright') # se le carga de valor al future  (lo recibe generalmente luego de una operación asincrónica)
    print(my_future.done())  # done() controla el estado del Future: Devuelve True porque está listo al tener un valor
    print(my_future.result()) # result() para obtener el contenido que guardó el Future
#asyncio.run() crea el event loop que gestiona la ejecución de corutinas 
asyncio.run(main())

# EJEMPLO USANDO AWAIT FUTURE Y TASK COMO EJECUTOR DE CORUTINAS
# Se declara una corutina llamada 'plan' que recibe un objeto Future como argumento
async def plan(my_future): 
    print('Planning my future...')
    await asyncio.sleep(1)  # se suspende la ejecución de esa corutina por 1 segundo (se simula una tarea asincrónica): no bloquea el hilo completo sino que permite que otras operaciones puedan ejecutarse en forma concurrente
    my_future.set_result('Bright') # se establece el resultado del Future como 'Bright', lo que desbloquea a quien esté esperando ese resultado

# Se define una función que crea y retorna un objeto Future
def create() -> Future: 
    my_future = Future() # se instancia un objeto Future manualmente
    # create_task(corutina) permite que varias corutinas se ejecuten de manera concurrente (para ejecución de corutinas en segundo plano)
    asyncio.create_task(plan(my_future)) # task es un tipo de future, que se crea a partir de una corutina y se encarga de ejecutarla
    return my_future # con la ejecución de la corutina, my_future se carga con algún valor


async def main(): # se define una corutina en la que se puede usar await para invocar a otra corutina
    my_future = create() # se crear el future, se le asigna un valor mediante una corutina
    result = await my_future # se pausa el future hasta que tenga un valor
    print(result) # se muestra contenido del future

asyncio.run(main()) # para poder ejecutar una corutina creando el event loop (gestionardor de corutinas)

# Por pantalla
    # Planning my future...
    # Bright