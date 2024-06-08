# Youtube Video Downloader

## Using pytube to download videos and playlists from Youtube, using the lib `pytube`

### How to use

- For CLI tool: `vid https://www.youtube.com/watch?v=1234` or `vidp https://www.youtube.com/playlist?list=PLo9Vi5B84_dfAuwJqNYG4XhZMrGTF3sBx`

#### Download Videos

- You can run the command passing the video as a argument. Like this: `python video_download.py https://www.youtube.com/watch?v=1234`
- Or if you want to download more than one video at a time, you can change the `videos.txt` file and add all the youtube links, one by one, each line at a time.

##### CLI

- You can run the command passing the video as an argument. Like this: `python video_download.py https://www.youtube.com/watch?v=1234`
- Or if you installed the CLI tool `vid`, you can run the command passing the video as a link. Like this: `vid https://www.youtube.com/watch?v=1234`

#### Download Playlists

- You can run the command passing the playlist as a argument. Like this: `python playlist_download.py https://www.youtube.com/watch?v=Mph0cWZsoV4&list=1234`

### Where are the videos downloaded?

- The videos will be downloaded in the `Videos` folder
- The playlists will be downloaded in the `Videos/Playlists` folder

### TODO

- [X] Add a progress bar
- [X] Add a way to download the videos in the best quality
- [X] Make a CLI
