import requests
from io import BytesIO
from PIL import Image
from PIL import ImageOps
from discord.ext import commands
import discord

bot = commands.Bot(command_prefix='.') # feel free to set your own prefix command like ! or + whatever you want

def num_there(s):
    return any(i.isdigit() for i in s) # check if the user entered a number

@bot.command()
async def crop(ctx, *, arg):
    """
    Please adjust to your own collection and change however you like. On this step the bot opens the .cache file and finds the arweave link associated to the entered NFT number.
    """
    with open('mainnet-beta-temp') as f:
        d = f.read()
        try:
            if num_there(arg) == True:
                meta = d.split(f'","name":"Golem #{arg}')[0].split('"link":"')[-1] # for normal NFTs which is just the NFT name + number
            else:
                meta = d.split(f'","name":"{arg}')[0].split('"link":"')[-1] # for more specific names which just consist of letters
        except:
            await ctx.send('Wrong input, try again.')

    try:
        r = requests.get(meta) # gets metadata by arweave link
        url = r.json()['image'] # picks out the image url
        r = requests.get(url) # gets the arweave image link
        img = Image.open(BytesIO(r.content)) # formats the image into the right object

        new = ImageOps.crop(img, (155, 80, 204, 279)) # format: (left, top, right, bottom) feel free to set your own measures

        with BytesIO() as image_binary:
            new.save(image_binary, 'PNG') # method to not save on your local pc
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='image.png')) # send the image straight as a response
    except:
        await ctx.send('Something went wrong, please try again.')

bot.run('') # enter your own discord token in here to run your bot