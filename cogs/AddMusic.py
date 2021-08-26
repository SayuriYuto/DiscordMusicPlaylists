import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json


cid = 'your_cid'
secret = 'your_secret_token'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class AddMusic(commands.Cog):
  def __init__(self, doki):
    self.doki = doki

  @commands.command()
  @commands.guild_only()
  async def add(self,ctx,*,arg:str):
    if '|' not in arg:
      playlist_id = arg.split('/')
      playlist_id = playlist_id[4]
      playlist = sp.user_playlist_tracks(playlist_id = playlist_id)
      playlist_name = f"{playlist['name']}-{playlist['owner']['display_name']}"
      link = arg
      caller_id = ctx.message.author.id
      await self.open_account(ctx.message.author)
      users = await self.get_player_data()
      users[str(caller_id)]['musicplaylist'].append(str(f"{playlist['name']}-{playlist['owner']['display_name']}\n[SPOTIFY]({arg})"))
      with open('playerdata.json','w') as file:
          json.dump(users,file)
      # Specifiy your channel Id here for notifications about new playlists added.
      error_channel = 12345678910111213
      error_channel_channel = await self.doki.fetch_channel(error_channel)
      await error_channel_channel.send(f"New playlist added by {ctx.message.author.display_name}")
      await ctx.send(f"{playlist_name} <{link}> was added to the music playlist list")
      await ctx.message.add_reaction("✅")
      return

    count = 0
    for i in arg.lower():
      if i == '|':  
        count = count + 1
    if count != 2:
      await ctx.send(f"{arg} was an incomplete argument. Refer d.help.")
      return
    arg = arg.split('|')
    playlist_name = arg[0]
    site = arg[1]
    link = arg[2]
    await self.open_account(ctx.message.author)
    users = await self.get_player_data()
    caller_id = ctx.message.author.id
    users[str(caller_id)]['musicplaylist'].append(f"{playlist_name}\n[{site.upper()}]({link})")
    with open('playerdata.json','w') as file:
      json.dump(users,file)
    error_channel = 12345678910111213
    # Specifiy your channel Id here for notifications about new playlists added.
    error_channel_channel = await self.doki.fetch_channel(error_channel)
    await error_channel_channel.send(f"New playlist added by {ctx.message.author.display_name}")
    await ctx.send(f"{playlist_name} <{link}> was added to the music playlist list")
    await ctx.message.add_reaction("✅")

  async def open_account(self,user):
    users = await self.get_player_data()
    if str(user.id) in users:
      if 'musicplaylist' not in users[str(user.id)].keys():
        users[str(user.id)]['musicplaylist'] = []
        with open('playerdata.json','w') as file:
          json.dump(users,file)
        # Specifiy your channel Id here for notifications about new playlists added.
        error_channel = 12345678910111213
        error_channel_channel = await self.doki.fetch_channel(error_channel)
        await error_channel_channel.send(f"New player data for music {user.display_name}")
        return False
    else:
      users[str(user.id)]={}
      users[str(user.id)]['musicplaylist'] = []
      # Specifiy your channel Id here for notifications about new playerID added.
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
  doki.add_cog(AddMusic(doki))