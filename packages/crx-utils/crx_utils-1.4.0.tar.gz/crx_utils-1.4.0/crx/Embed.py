from nextcord import Embed, Forbidden, Color

red = Color.from_rgb(255, 0, 0)
green = Color.from_rgb(0, 255, 0)
blue = Color.from_rgb(0, 0, 255)
yellow = Color.from_rgb(255, 255, 0)
transparent = Color.from_rgb(43, 45, 49)

async def send_embed(title, description, id, bot, emoji, content=None, guild=True, color=transparent):
    try:
        embed_data = Embed(color=color)
        embed_data.set_author(name=f"{emoji} {title}")
        embed_data.description = description

        if guild:
            sending = await bot.fetch_channel(id)
        else:
            sending = await bot.fetch_user(id)

        await sending.send(content=content, embed=embed_data)
    except Forbidden:
        pass

async def embed_success(title, description, id, bot, emoji="✅", content=None, guild=True):
    await send_embed(title, description, id, bot, emoji, content, guild, color=green)

async def embed_error(title, description, id, bot, emoji="❌", content=None, guild=True):
    await send_embed(title, description, id, bot, emoji, content, guild, color=red)
