import discord
import os

client = discord.Client() # Connects to the discord client

@client.event #Callback to a unsychronous library of events
async def on_ready():
  # When the bot is ready to be used
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
# Each time a message is sent
  if message.author == client.user:
    return # Does Nothing if the message is sent by itself
  
  if message.content.startswith('&Devsearch'):
    # Command : '&Devsearch ....'
    await message.channel.send('1, 2, 3, do you copy?') # Returns a message to be sent by the bot

client.run(os.getenv('TOKEN')) # Runs the bot with the private bot token