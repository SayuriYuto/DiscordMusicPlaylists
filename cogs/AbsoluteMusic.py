import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json

# Refer Spotipy documentations https://spotipy.readthedocs.io/en/2.19.0/
cid = 'your_c_id'
secret = 'your_secret_token'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

class AbsoluteMusic(commands.Cog):
  def __init__(self, doki):
    self.doki = doki

  @commands.cooldown(1, 10, commands.BucketType.user)
  @commands.command()
  @commands.guild_only()
  async def music(self,ctx,person:discord.Member = None):    
    if person != None:
      if person.bot:
        return
      caller_id = person.id
      caller = person
      await self.open_account(caller)
    else:
      caller_id = ctx.message.author.id
      caller = ctx.message.author
      await self.open_account(caller)
    users = await self.get_player_data()
    musiclist = users[str(caller_id)]['musicplaylist']
    emusic=discord.Embed(title=f"{caller.display_name}'s Saved Music Playlists",description="List below :arrow_double_down:", color = ctx.message.author.color)
    if len(musiclist) == 0:
      # You can have any default playlst here
      link = "[YOUTUBE](https://www.youtube.com/watch?v=K3Qzzggn--s)"
      emusic.add_field(name="You have no saved playlists. Here's my dear song" ,value=link,inline=True)
      await ctx.send(embed=emusic)
      await ctx.message.add_reaction("✅")
      return
    count=1
    for i in musiclist:
      n=i.split("[",1)
      link=f"[{n[1]}"
      emusic.add_field(name=f"{count}.{n[0]}",value=link,inline=True)
      count+=1
    emusic.set_footer(icon_url=ctx.author.avatar_url,text=f'Responsible motherfucker: {ctx.author.name} ID:{ctx.author.id}')
    await ctx.send(embed=emusic)
    await ctx.message.add_reaction("✅")
      
  async def open_account(self,user):
    users = await self.get_player_data()
    if str(user.id) in users:
      if 'musicplaylist' not in users[str(user.id)].keys():
        users[str(user.id)]['musicplaylist'] = []
        with open('playerdata.json','w') as file:
          json.dump(users,file)
        error_channel = 12345678910111213
        error_channel_channel = await self.doki.fetch_channel(error_channel)
        await error_channel_channel.send(f"New player data for music {user.display_name}")
        return False
    else:
      users[str(user.id)]={}
      users[str(user.id)]['musicplaylist'] = []
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
  doki.add_cog(AbsoluteMusic(doki))