import discord
from discord.ext import commands, tasks
import giphy_client
from giphy_client.rest import ApiException
import random

# Define the bot's intents
intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

# Create the bot instance with the required intents
bot = commands.Bot(command_prefix="!", intents=intents)
channel_id = "channel id"

@tasks.loop(hours=24)
async def daily_routine(q="gif name"):
    message_channel = bot.get_channel(channel_id)
    print(f"Got channel {message_channel}")
    api_key = "giphy api key"
    api_instance = giphy_client.DefaultApi()
    try:
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='r')
        lst = list(api_response.data)
        giff = random.choice(lst)
        embed_link = discord.Embed(title=q)
        embed_link.set_image(url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")
    except ApiException:
        print("Exception when calling API")
    await message_channel.send("you can type your custom message here if you want (comment this line if it is opposite)")
    await message_channel.send(giff.embed_url)  # this line sends your gif

@daily_routine.before_loop
async def before():
    await bot.wait_until_ready()
    print("Finished waiting")

# Start the task loop when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not daily_routine.is_running():
        daily_routine.start()

bot.run("bot token here")
