# DiscordMusicPlaylists
### This is an Amateur code for a discord bot which can store music playlists for you. On calling a single command you can view your stored playlists or your friend's playlists.<br>
### **Features**:<br>
1. You can view your own (`<prefix><music>`) as well as your friends playlists by just mentioning  the member (`<prefix><music> <@member_mention>`).
2. Can store upto 25 Playlists. (planning to add more pages)
3. Can add (`<prefix><add> <playlist_name|site|playlist_url>`) and delete (`<prefix><delete> <rank_of_playlist>`) existing playlists.
4. Spotipy integration. No need to use the long plsylist add syntax(above), directly link the playlist (`<prefix><add> <spotify_playlist_url>`).

### **Additional Files and stuff needed**:<br>
1. playerdata.json<br>Please create a json file in the directory with the following name
2. SpotiPy<br>Please refer https://spotipy.readthedocs.io/en/2.19.0/ for spotify integration
3. Notification channel id (not mandatory, can be commented otherwise. Also can be any server, For eg. a logs channel)


PS: I am very new to discord python, and just experimenting with my skills. If you feel any changes regarding my code or anything in general please do suggest. Thank You!!<br>
    Also I am new to Github too. So please forgive my bad practices here.
