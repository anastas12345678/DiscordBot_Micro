from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import logging

import random
from discord import ui

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix = '!', intents=intents)


@client.event
async def on_ready():
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='On Developing!'))
    await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name='On Developing!'))
    print('Services are Online!')


#Microlab Commands
@client.command()
async def rnumb(ctx):
    await ctx.message.delete()
    r = random.randint(1, 100)
    await ctx.send(r)

class RandomNumbModal(discord.ui.Modal, title="Random Number"):
    def __init__(self):
        super().__init__(timeout=None)
        self.start_first =  discord.ui.TextInput(
            label = "First Number",
            placeholder = "e.g. 1",
            equired = True
        )
        self.end_last =  discord.ui.TextInput(
            label = "Last Number",
            placeholder = "e.g. 10",
            required = True
        )
        self.add_item(self.start_first)
        self.add_item(self.end_last)
    
    async def on_submit(self, interaction: discord.Interaction):
        start = int(self.start_first.value)
        end = int(self.end_last.value)
        r = random.randint(start, end)
        await interaction.response.send_message(r)

@client.command()
async def rnumbers(ctx):
    embed = discord.Embed(
        title="Random Number",
        color=discord.Color.green()
    )
    embed.add_field(name = "Press the Button for to input the numbers", value = "", inline = False)

    verify_button = discord.ui.Button(label="Press", style=discord.ButtonStyle.green, custom_id="random_button")

    async def verify_button_callback(interaction: discord.Interaction):
        await interaction.response.send_modal(RandomNumbModal())

    verify_button.callback = verify_button_callback
    button = discord.ui.View()
    button.add_item(verify_button)

    await ctx.send(embed=embed, view=button)


# Commands
@client.command()
async def clear(ctx, amount=1):
    await ctx.message.delete()
    await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await ctx.message.delete()
    await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
    await ctx.message.delete()
    await member.ban(reason=reason)


# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client.run (token)
