import urllib
from shutil import copyfileobj

import discord
import os
import random
import requests

from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='ppb ')

#add to github
#requirements.txt file: explicit dependency list
#check new pics/folders: validation
#

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command(name='random', help='This will randomly generate a photo from the list of pets.')
async def random_pet_pic(ctx):
    if ctx.author == bot.user:
        return
    image_directory = "./Images"
    random_pet = path_to_a_file(image_directory)
    await ctx.channel.send(f"Here is your pet pic!", file=discord.File(f'{random_pet}'))


@bot.command(name='list', help='This list is of available pets who have pictures to view.')
async def list_of_pets(ctx):
    if ctx.author == bot.user:
        return

    image_directory = "./Images"
    list1 = os.listdir(image_directory)

    await ctx.channel.send(f"List of pet names: {list1}")  # prints pet names


@bot.command(name='addpet', help='Adds the name of a folder to ppb.')
async def add_pet_name(ctx, pet_name):
    if ctx.author == bot.user:
        return
    image_directory = "./Images"
    directory = pet_name

    try:
        # Path
        path = os.path.join(image_directory, directory)
        # Create the directory
        os.mkdir(path)
        await ctx.channel.send(f"Directory {pet_name} created")
    except FileExistsError:
        await ctx.channel.send("Pet already exists, please choose another.")
    except:
        await ctx.echannel.send("Something else went wrong when making that directory.")


@bot.command(name='addpic', help='Adds a pic to a pet directory. -petname--petpic-')
async def add_pet_pic(ctx, pet_name, *args):
    for attachment in ctx.message.attachments:
        save_image(attachment.url, pet_name)

    for arg in args:
        save_image(arg, pet_name)

    await ctx.channel.send(f"Picture of {pet_name} added")


def save_image(url, pet_name):
    image_directory = "./Images"
    url_split = urllib.parse.urlsplit(url, scheme='', allow_fragments=True)
    split = urllib.parse.urlsplit(url, "/")
    file = f"{image_directory}/{pet_name}/{split.path.split('/')[-1]}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(file, 'wb') as out_file:
        copyfileobj(response, out_file)


@bot.command(name='picof', help='To get a list of pet names is "ppb list". '
                                 'Only pet names that are listed will work.')
async def specific_pet_pic(ctx, pet_name):
    if ctx.author == bot.user:
        return

    image_directory = "./Images"
    list1 = os.listdir(image_directory)

    try:
        file_path = path_to_a_pet(pet_name)
        await ctx.channel.send(f"Here is your {pet_name} pic!", file=discord.File(f'{file_path}'))
    except NameError:
        await ctx.channel.send("This pet does not exist. Please type: ppb list -to see pet names.")
    except:
        await ctx.channel.send("Something else went wrong when looking for that file.")

def path_to_a_pet(pet_name):  # method that creates a path to a file
    n = 0
    random.seed()
    for root, dirs, files in os.walk(f'./Images/{pet_name}'):
        for name in files:
            n = n + 1
            if random.uniform(0, n) < 1: rfile = os.path.join(root, name)
    return rfile


def path_to_a_file(directory):  # method that creates a path to a file
    n = 0
    random.seed()
    for root, dirs, files in os.walk(f'{directory}'):
        for name in files:
            n = n + 1
            if random.uniform(0, n) < 1: rfile = os.path.join(root, name)
    return rfile


bot.run(token)

#get, put, post, etc through html
#get request is standard view webpage.
#put request is ???
#post request is use in login system.
#rest calls, ^^^
#get request on url get back just a jpeg. or image

