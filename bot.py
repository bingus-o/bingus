import asyncio
import math
import random
from io import BytesIO
import os
import names
import requests
from PIL import Image, ImageDraw
import discord
from bs4 import BeautifulSoup
from discord.ext import commands
import pymongo
from udpy import UrbanClient
from random import gauss, seed
from math import sqrt, exp
import matplotlib.pyplot as plt

uclient = UrbanClient()

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
client = commands.Bot(command_prefix="bb ", intents=discord.Intents.all())
client.db = myclient["baseball-sim"]
client.color = discord.Color.blue()

@client.event
async def on_ready():
    print(f"{client.user.name}#{client.user.discriminator} is online.")

async def load_cogs():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
asyncio.run(load_cogs())

async def embed_builder(top_def):
    embed = discord.Embed(title=f"{top_def.word}",
                          description=top_def.definition, color=discord.Color.blue())

    try:
        embed.url = f"https://www.urbandictionary.com/define.php?term={top_def.word.replace(' ', '+')}"
    except:
        pass

    embed.add_field(name="Example", value=top_def.example)
    embed.set_footer(text=f"{top_def.upvotes} upvotes | {top_def.downvotes} downvotes")
    return embed

@client.command()
async def im(ctx):
    async for message in ctx.channel.history(limit=None):
        if message.author == ctx.author:
            await message.delete()


@client.command()
async def urban(ctx, *, term):
    definitions = list(uclient.get_definition(term.lower()))
    if len(definitions) == 0:
        return await ctx.reply("No definitions for that word.")
    sorted_defs = sorted(definitions, key=lambda x: x.upvotes, reverse=True)
    top_def = sorted_defs[0]
    view = Toggle(ctx, sorted_defs)
    msg = await ctx.reply(embed=await embed_builder(top_def), view=view)
    view.message = msg


def create_GBM(s0, mu, sigma):
    def generate_value():
        nonlocal s0
        s0 *= exp((mu - 0.5 * sigma ** 2) * (1. / 365.) + sigma * sqrt(1./365.) * gauss(mu=0, sigma=1))
        return s0

    return generate_value

gbm = create_GBM(100, 0.0, 0.05)
client.stock_prices = [gbm() for _ in range(365)]

@client.command()
async def advance(ctx, amount: int=1):
    client.stock_prices.append(gbm())
    await ctx.reply(f"{amount} day(s) advanced. Type `bb graph` to see the stock graph!")

@client.command()
async def graph(ctx, days: int=-1):
    if days < 7 and days != -1:
        return await ctx.reply("`days` must be greater or equal to 7.")

    if days == -1: stock_prices = client.stock_prices
    else: stock_prices = client.stock_prices[-days:]

    y = [x for x in range(len(stock_prices))]
    plt.plot(y, stock_prices)
    plt.title(f'Stock Price Over {len(stock_prices)} Days')
    plt.xlabel('Time')
    plt.ylabel('Stock Price')

    buffer = BytesIO()
    plt.savefig(buffer)
    buffer.seek(0)

    f = discord.File(buffer, filename="image.png")
    await ctx.reply(file=f)
    plt.close()

class Toggle(discord.ui.View):
    def __init__(self, ctx, defs):
        super().__init__(timeout=30)
        self.message = None
        self.ctx = ctx
        self.defs = defs
        self.index = 0

        self.children[0].disabled = True
        if len(defs)==1: self.children[1].disabled = True

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.blurple)
    async def previous(self, interaction, button):
        self.index -= 1
        if self.index == 0: button.disabled = True
        if self.index == len(self.defs)-2: self.children[1].disabled = False
        await interaction.response.edit_message(embed=await embed_builder(self.defs[self.index]), view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.blurple)
    async def next(self, interaction, button):
        self.index += 1
        if self.index == len(self.defs)-1: button.disabled = True
        if self.index == 1: self.children[0].disabled = False
        await interaction.response.edit_message(embed=await embed_builder(self.defs[self.index]), view=self)

    async def interaction_check(self, interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.response.send_message("You can't interact with this.", ephemeral=True)
            return False
        return True

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)



client.run("OTk2MjQ3NzExMDU5ODA0MjQx.GjG58I._Cv2Ea8yr-Xz35sdfHCwADOWSF8-uUTduBUI7I")