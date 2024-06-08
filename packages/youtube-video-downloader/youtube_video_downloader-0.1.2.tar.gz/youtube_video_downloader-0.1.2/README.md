# Youtube Video Downloader

## Using pytube to download videos and playlists from Youtube, using the lib `pytube`

### How to use

- For CLI tool: `vid https://www.youtube.com/watch?v=1234` for a single video or `vidp https://www.youtube.com/playlist?list=PLo9Vi5B84_dfAuwJqNYG4XhZMrGTF3sBx` for a playlist.
- If you want to download multiple videos at once you can use: `vid https://www.youtube.com/watch?v=1234 https://www.youtube.com/watch?v=1234 https://www.youtube.com/watch?v=1234` **OR** `vid -f videos.txt` with a text file containing the links one by line.

### Where are the videos downloaded?

- The videos will be downloaded in the `Videos` folder, unless you specify a different path with `vid --path /path/to/videos`
- The playlists will be downloaded in the `Videos/Playlists` folder unless you specify a different path with `vidp --path /path/to/videos`

### TODO

- [X] Add a progress bar
- [X] Add a way to download the videos in the best quality
- [X] Make a CLI
