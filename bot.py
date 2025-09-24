# Código principal que arranca el bot y carga las extensiones (cogs)
import os                          # Interactua con el SO para obtener la información de las variables de entorno. 
import asyncio                     # Para ejecutar la función main() asíncrona
from dotenv import load_dotenv     # Para leer .env (donde se tendrán las variables de entorno configuradas)
import discord                     # Importa la librería principal de discord
from discord.ext import commands   # Extensiones para comandos

# Cargamos en esta aplicación las variables de entorno desde el .env (si existe)
load_dotenv()                      # Lee un archivo .env y carga sus pares de clave-valor como variables de entorno en la aplicación Python.
TOKEN = os.getenv("BOT_TOKEN")     # con esto se logra NO poner el token en el código (esto es una práctica segura)
GUILD_ID = os.getenv("GUILD_ID")   # con esto se logra NO poner el ID del GUILD (del servidor) en el código (práctica segura)

if not TOKEN:
    # Si no hay token no funciona la aplicación por eso se va a recibir un mensaje de error
    raise RuntimeError("Falta BOT_TOKEN en .env — se debe copiar .env.example a .env y poner el token")

# Intents: indica qué eventos queremos recibir.
# message_content es necesario para leer el contenido de cada mensaje (para comandos con prefijo y detección de texto).
intents = discord.Intents.default()
intents.message_content = True

# Prefijo: es lo que el usuario escribe para comandos 'tradicionales' (ej: !hola).
    # Se puede usar string, lista de strings, o funciones.
        # 1 - Lista de Strings :   
            # bot = commands.Bot(command_prefix=["!", ".", "?"], intents=intents) 
            # el bot responde a !comando, .comando, o ?comando. 
        # 2 -  Funciones
            # def obtener_prefijo(bot, message):
            #     if message.guild and message.guild.id == 123456789:
            #         return "?"
            #     return "!"
            # si el mensaje viene de un servidor específico, el prefijo será "?", si no, será "!".
            # bot = commands.Bot(command_prefix=obtener_prefijo, intents=intents) 
                # cómo python puede procesar una función sin pasarle explícitamente los parámetros? 
                    # las funciones son objetos de primera clase en python : 
                        # se las puede pasar como argumentos a otras funciones
                        # asignarlas a variables,
                        # se pueden retornar desde funciones,
                        # se pueden almacenar en estructura de datos (listas, diccionarios, etc)
                        # es decir, usarlas como cualquier otro dato.
                        # Esto es porque Python es multipradigma
                            # soporta paradigma orientado a objetos, funcional y procedimental (imperativo) , 
                            # no es un leguaje lógico pero posee bibliotecas que intentan emularlo.
                            # Se puede tener código en Python que sea: 
                                # Muy estructurado y orientado a objetos
                                # Minimalista y funcional
                                # Procedimental y directo. 
                                # O incluso mezclar estilos. Por ejemplo, usar clases para modelar datos y funciones puras para procesarlos. 
                    # lo que ocurre internamente en la librería discord.py
                        # 1- prefix = command_prefix(bot, message) no se ve en el código fuente pero si esta en la librería:  
                            # if callable(self.command_prefix):
                            # prefix = await utils.maybe_coroutine(self.command_prefix, self, message). 
                            # self.command_prefix es lo que se le pasa al bot (en este caso, la función obtener_prefijo).
                            # callable(...) verifica si eso es una función. utils.maybe_coroutine(...) llama a esa función 
                            # con los argumentos self (el bot) y message.
            # 3 - String
bot = commands.Bot(command_prefix="!", intents=intents, help_command=commands.DefaultHelpCommand())

# Evento: cuando el bot está listo
@bot.event # decorador que se aplica a funciones que manejan eventos del bot, proviene de la librería discord.py
async def on_ready():
    # on_ready se llama cuando el bot está conectado y listo.
    print(f"Bot conectado como {bot.user} (id: {bot.user.id})")

# Cómo funciona la sincronización de slash/híbridos? 
# Cuando se define @commands.hybrid_command, ese comando tiene que registrarse en la API de Discord.
# Esa "sincronización" (el famoso await bot.tree.sync()) puede hacerse:
    # Globalmente → tarda hasta 1 hora en aparecer en todos los servidores. 
        # Si se hace seguido, puede ocurrir límites de rate-limit.
            # rate-limit se traduce como limitado por tasa o restricción de frecuencia
            # mecanismo de los sistemas informáticos para controlar cuántas veces se puede hacer una acción 
            # en un período de tiempo (con el objetivo de evitar spam y sobrecargas).
            # mensaje “You are being rate limited” (discord) aparece cuando intentas hacer una acción demasiadas veces 
            # en poco tiempo, como: enviar muchos mensajes seguidos, intentar verificar el número de teléfono repetidamente, 
            # hacer clic en botones de verificación sin esperar. 
            # Discord bloquea al usuraio temporalmente (desde unos segundos hasta varios minutos) para proteger el sistema. 
    # Por servidor (guild-specific) → aparece al instante, ideal para pruebas, casi sin riesgo de rate-limit.

# NO conviene sincronizar siempre en on_ready porque cada vez que reiniciás el bot, va a intentar registrar todo de nuevo. 
# Lo correcto: sincronizar sólo cuando cambiaste comandos o manualmente con un comando oculto para vos. 
# En desarrollo, debería sincronizar para un solo GUILD (1 servidor)
# En producción, debería ser global (una vez que está todo probado) 
# también esta la opción de sincronizar algunos servidores (más de 1)

# @commands.is_owner() : para que el comando pueda ser utilizado únicamente por el dueño del bot
    # No se necesita poner el ID owner manualmente.
    # Funciona automáticamente con el dueño de la aplicación del bot (la cuenta que creó la app en el Developer Portal)
    # no hace falta ponger algo en .env (solo valida 1 dueño oficial)

# @commands.command(name="..."): define un comando llamado name que puede ser ejecutado por todos los usuarios en Discord.

# SPLIT, MAP e INT
# string.split("separador"): print("hola,cómo,estás,?".split(",")): ['hola', 'cómo', 'estás', '?']
# "string".split("separador") : print("manzana,banana,pera".split(",")) -> ['manzana', 'banana', 'pera']
# map(funcion_aplicar_por_elemento,iterable_con_muchos_elementos) : print (map(int, ["1", "2", "3"] ) ) -> [1, 2, 3] 
# int(numero_flotante_o_string) : convierte a entero cada elemento del iterable (puede ser lista, diccionario,etc)

# async/await es como pedirle a alguien que haga una tarea y que te avise al finalizar 
# (para hacer algo en el mientras se espera el resultado y sin quedarte parado mirando).
# async def : declara una coroutine (función asíncrona).
# await : se usa dentro de una coroutine para "esperar" otra coroutina sin bloquear todo el hilo. 

# await ctx.bot.tree.sync()
# ctx: contexto de una interacción o comando (contine información como quién ejecutó el comando, en qué canal, qué bot lo recibió, etcétera)
# bot: atributo de ctx. Representa la instancia del bot que está ejecutando el comando.
# bot.tree : se refiere a una estructura jerárquica (árbol) que se enecraga de gestionar y organizar los comandos de interacción en Discord. 
# bot.tree va a permitir registrar, sincronizar y organizar los comandos. 
    # los comandos se registran en tree mediante decoradores o métodos como @commands.command(name=...). 
    # tree gestiona los comandos y con async() se sincroniza los comandos con Discord 
    # (se manda los comandos a discord para que estén disponibles en los servidores)
# .sync(): Es el método que sincroniza los comandos registrados en el árbol con los servidores de Discord.
    # guild=guild: Le indica que la sincronización debe hacerse solo en ese servidor específico (no globalmente).
# await : sync() es una corutina (una función async), que espera operaciones asincrónicas (como comunicarse con la API de Discord) y devuelve un objeto tipo Coroutine

# synced = await ctx.bot.tree.sync()?
# Ejecuta el método sync() para sincronizar los comandos del bot. Espera a que termine esa operación (porque puede tardar).
# Guarda el resultado (por ejemplo, una lista de comandos sincronizados) en la variable synced.


# SINCRONIZAR TODOS LOS SERVIDORES QUE TENGO CON COMANDOS HÍBRIDOS
# 🔹 Comando para sincronizar GLOBALMENTE
@commands.command(name="sync_global") # Define un comando llamado sync_global que puede ser ejecutado por los usuarios en Discord.
@commands.is_owner()  # Solo el dueño del bot puede ejecutarlo. Si otro usuario lo intenta, se le denegará el acceso.
async def sync_global(self, ctx): # async def: función asincrónica (corutina) que se ejecuta cuando se llama al comando y ctx = contexto de la invocación: autor, canal, guild, message, etc
    try: # para el manejo de errores
        # Sincroniza los comandos globales del bot con la API de Discord.
        synced = await ctx.bot.tree.sync()
        # ctx.send() para enviar un mensaje al canal donde se ejecutó el comando.
        # es una corutina (una función async). Al interactuar con la API de Discord (que es asincrónica), necesita que el programa espere a que se complete la operación. 
        # El mensaje se envía al canal de texto donde el usuario ejecutó el comando.
        # Discord lo muestra como si el bot hubiera escrito ese mensaje. ctx representa el contexto de ese comando.
        # ctx.send() envía el mensaje al canal correspondiente.
        await ctx.send(f"✅ Sincronizados {len(synced)} comandos globales.\n" # Envía un mensaje al canal informando cuántos comandos fueron sincronizados.
                        f"(Puede tardar hasta 1 hora en propagarse).") # porque es para todos los servidores en el que esté el bot
    except Exception as e: # Si ocurre algún error, se captura en la variable e
        await ctx.send(f"⚠️ Error al sincronizar global: {e}") # Envía un mensaje al canal con el detalle del error ocurrido.

# SINCRONIZAR SOLO UN SERVIDOR CON COMANDOS HÍBRIDOS
# 🔹 Comando para sincronizar SOLO en un GUILD (más rápido)
@commands.command(name="sync_guild") # Declara un comando de texto llamado sync_guild. 
# Se ejecuta escribiendo (prefijo)name_comando
@commands.is_owner() # Restringe el uso del comando solo al dueño del bot. Si otro usuario lo intenta, se le denegará el acceso.
async def sync_guild(self, ctx): # función asincrónica que se ejecuta cuando se llama el comando. 
    # ctx es el contexto del comando, contiene información sobre el mensaje, el canal, el autor, etc.
    """Sincroniza slash/híbridos en un servidor específico (instantáneo). 
    Uso: !sync_guild
    """ # Es un docstring que explica qué hace el comando y cómo se usa.
    try:
        guild_id = GUILD_ID or ctx.guild.id  # Usa el guild del .env o del server donde estás
        # podría haber una lista de guild? qué cambios hay que incorporar respecto de lo actual?
        guild = discord.Object(id=guild_id) # crea un objeto de tipo Guild usando el id_guild. 
        # Este objeto se usa para indicar a Discord en qué servidor se deben sincronizar los comandos.
        synced = await ctx.bot.tree.sync(guild=guild) # # Sincroniza los comandos slash del bot solo en ese servidor.  
        # Contiene una lista de los comandos sincronizados. 
        await ctx.send(f"✅ Sincronizados {len(synced)} comandos en el servidor {guild_id}.") # Envía un mensaje al canal 
        # confirmando cuántos comandos fueron sincronizados en ese servidor.
    except Exception as e:
        await ctx.send(f"⚠️ Error al sincronizar guild: {e}")

# VARIOS SERVIDORES QUE NECESITAN ACTUALIZAR COMANDOS HÍBRIDOS
# Evita la espera de hasta 1 hora de la sincronización global.
# Se controla exactamente en qué servidores se actualizan los comandos.
# Se mantiene una lista dinámica en .env sin tocar el código.
@commands.command(name="sync_selected_guilds") # Declara un comando de texto llamado sync_selected_guilds 
@commands.is_owner() # Restringe el uso del comando solo al dueño del bot. Si otro usuario lo intenta, se le denegará el acceso.
async def sync_selected_guilds(self, ctx): # función asincrónica que se ejecuta cuando se llama el comando.
    """Sincroniza comandos slash en múltiples servidores definidos en .env"""
    try:
       
        guild_ids = os.getenv("GUILD_IDS").split(",")        # Obtiene los IDs como lista de enteros
        guild_ids = [int(gid.strip()) for gid in guild_ids]  # Son IDs de servidores específicos seleccionados para actualizar comandos
        total_synced = 0 # variable para contar el total de comandos sincronizados en todos los servidores
        for gid in guild_ids:
            # Crea un objeto Guild usando el ID actual para indicarle a Discord en qué servidor se deben sincronizar los comandos.
            guild = discord.Object(id=gid) 
            # Sincroniza los comandos slash del bot solo en ese servidor. 
            # synced es una lista con los comandos que fueron sincronizados en ese servidor.
            synced = await ctx.bot.tree.sync(guild=guild)
            total_synced += len(synced) # Suma la cantidad de comandos sincronizados en este servidor al total acumulado.
            await ctx.send(f"✅ {len(synced)} comandos sincronizados en el servidor `{gid}`.")

        # Una vez terminado el bucle, envía un mensaje resumen cuántos servidores fueron sincronizados 
        # y cuántos comandos se sincronizaron en total.
        await ctx.send(f"🎯 Sincronización completa en {len(guild_ids)} servidores. Total de comandos sincronizados: {total_synced}")

    except Exception as e:
        await ctx.send(f"⚠️ Error al sincronizar múltiples servidores: {e}")


OWNERS = list(map(int, os.getenv("OWNERS").split(",")))

def is_in_owners():
    async def predicate(ctx):
        return ctx.author.id in OWNERS
    return commands.check(predicate)

class Admin(commands.Cog):
    @commands.command(name="sync_global")
    @is_in_owners()
    async def sync_global(self, ctx):
        await ctx.send("Solo ciertos dueños pueden usar esto.")

def has_admin_role():
    async def predicate(ctx):
        return any(role.name == "Administrador" for role in ctx.author.roles)
    return commands.check(predicate)

class Admin(commands.Cog):
    @commands.command(name="sync_guild")
    @has_admin_role()
    async def sync_guild(self, ctx):
        await ctx.send("Este comando solo lo pueden usar los que tengan rol Admin.")


# Cargar extensiones (cogs). Esto es asíncrono y por eso usamos await.
# asíncrono : forma de ejecutar código sin bloquear el flujo principal.
# Permite que el programa siga funcionando mientras espera que algo termine 
# (como leer un archivo, esperar una respuesta de red, etc.).
# Se usa mucho en bots, servidores web, y apps que manejan múltiples tareas al mismo tiempo.
# await: indica que hay que esperar a la tarea que se esta procesando, pero permite seguir con otras tareas
# se usa dentro de funciones asíncronas (async def) para esperar el resultado de otra función asíncrona.

# load_extensions(): función que viene por defecto en commands.Bot. Sirve para cargar un módulo externo (llamado cog) 
# que contiene comandos, eventos, etc. útil para organizar tu bot en archivos separados, manteniendo el código limpio y modular. 
# "cogs.ejemplo" no es una ruta de archivo tradicional con barras (/ o \). Es una ruta estilo módulo de Python.

# "cogs.ejemplo" significa: → Hay un archivo llamado ejemplo.py dentro de una carpeta llamada cogs.

# En Python, los módulos se importan así: from cogs import ejemplo Por eso se usa el punto (.) en vez de la barra.

# Elemento	¿Qué es?
# async def	Define una función asíncrona.
# await	Espera una tarea sin bloquear el programa.
# bot.load_extension()	Carga un módulo externo (cog) al bot.
# "cogs.ejemplo"	Ruta estilo módulo: archivo ejemplo.py dentro de carpeta cogs.



async def load_extensions():
    # "cogs.ejemplo" corresponde al archivo cogs/ejemplo.py (ruta estilo módulo Python)
    # Esto le dice al bot: “Cargá esta extensión, pero no bloquees todo el programa mientras lo hacés.”
    await bot.load_extension("cogs.ejemplo")

# Usamos un patrón 'async main' moderno para manejar bien el ciclo de vida del bot.
async def main():
    # 'async with bot' abre el bot como contexto asíncrono: hace inicializaciones y asegura limpieza al salir.
    async with bot:
        await load_extensions()      # cargamos los cogs antes de iniciar la conexión
        await bot.start(TOKEN)      # inicia la conexión con Discord (websocket, loop, eventos)

# Punto de entrada del script
if __name__ == "__main__":
    # asyncio.run crea un loop, ejecuta main() y cierra el loop al terminar.
    asyncio.run(main())
 