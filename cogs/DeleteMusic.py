import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

cid = 'your_cid'
secret = 'your_secret_token'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class DeleteMusic(commands.Cog):
  def __init__(self, doki):
    self.doki = doki
  
  @commands.command()
  @commands.guild_only()
  async def delete(self,ctx,number:int):
    await self.open_account(ctx.message.author)
    users = await self.get_player_data()
    caller_id = ctx.message.author.id
    musiclist = users[str(caller_id)]['musicplaylist']
    if number>=0 :
      if number<=len(musiclist):
        remind = musiclist[number-1]
        musiclist.pop(number-1)
        await ctx.send(f"<{remind} was removed from the playlist!!!>")
        await ctx.message.add_reaction("✅")
        with open('playerdata.json','w') as file:
          json.dump(users,file)
        # Specifiy your channel Id here for notifications
        error_channel = 12345678910111213
        error_channel_channel = await self.doki.fetch_channel(error_channel)
        await error_channel_channel.send(f"Playlist deleted by {ctx.message.author.display_name}")
      else:
        await ctx.send("The number you entered, does not exist in the list")
    else:
      await ctx.send("Please enter a positive integer!")

  async def open_account(self,user):
    users = await self.get_player_data()
    if str(user.id) in users:
      if 'musicplaylist' not in users[str(user.id)].keys():
        users[str(user.id)]['musicplaylist'] = []
        with open('playerdata.json','w') as file:
          json.dump(users,file)
        # Specifiy your channel Id here for notifications
        error_channel = 12345678910111213
        error_channel_channel = await self.doki.fetch_channel(error_channel)
        await error_channel_channel.send(f"New player data for music {user.display_name}")
        return False
    else:
      users[str(user.id)]={}
      users[str(user.id)]['musicplaylist'] = []
      # Specifiy your channel Id here for notifications
      error_channel = 12345678910111213
      error_channel_channel = await self.doki.fetch_channel(error_channel)
      await error_channel_channel.send(f"New player data {user.display_name}")
    with open('playerdata.json','w') as file:
      json.dump(users,file)

  async def get_player_data(self):
    with open('playerdata.json','r') as file:
      users = json.load(file)
      return users

def setup(doki):
  doki.add_cog(DeleteMusic(doki))