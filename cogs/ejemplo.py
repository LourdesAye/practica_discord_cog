# cogs/ejemplo.py
import discord
from discord.ext import commands

class EjemploCog(commands.Cog):
    """Un cog de ejemplo con un comando y un listener"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot  # Guardamos referencia al bot

    @commands.command(name="hola")  # Definimos un comando normal con decorador
    async def hola(self, ctx):
        await ctx.send("¡Hola! Soy un bot con Cogs 👋")

    @commands.Cog.listener()  # Definimos un listener (oyente de eventos)
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return  # Ignora los mensajes del propio bot
        if "chau" in message.content.lower():
            await message.channel.send("¡Hasta luego!")

# Función obligatoria para que el bot registre este Cog
async def setup(bot: commands.Bot):
    await bot.add_cog(EjemploCog(bot))
