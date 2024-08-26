import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio

# Configurar intents
intents = discord.Intents.default()
intents.message_content = True  # Esto permite que el bot pueda leer los mensajes del contenido de los comandos

# Configuración del bot de Discord
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuración de yt_dlp para extraer el audio
youtube_dl.utils.bug_reports_message = lambda: ''
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Evita problemas de IPv6
}

# Comando del bot para reproducir música
@bot.command(name='playy')
async def play(ctx, url: str):
    try:
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Debes estar en un canal de voz para usar este comando.")
            return

        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client is None:
            voice_client = await voice_channel.connect()

        # Descargar el audio desde YouTube
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']

        # Reproduce el audio en el canal de voz
        voice_client.play(discord.FFmpegPCMAudio(executable='C:\\Python Project\\Proyectos\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe', source=url2))
        await ctx.send(f"Reproduciendo: {info.get('title')}")

    except Exception as e:
        await ctx.send(f"Ha ocurrido un error: {str(e)}")

# Comando para que el bot salga del canal de voz
@bot.command(name='stop')
async def stop(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.send("Desconectado del canal de voz.")

# Ejecuta el bot
bot.run('Discord-Key-Token')  # Añade tu token de Discord aquí
