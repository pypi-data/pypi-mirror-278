import sys
from pathlib import Path
import typer
from pytube import Playlist


app = typer.Typer()


# make dir with playlistname
def download_playlist(link: str, path: Path):
    p = Playlist(link)
    to_path = path / p.title

    for i, video in enumerate(p.videos):
        print(video.title)
        video.register_on_progress_callback(progress_func)
        # save to dir
        video.streams.get_highest_resolution().download(
            to_path,
            filename_prefix=str(i) + "_",
        )
        print()


def progress_func(stream, chunk, bytes_remaining):
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    sys.stdout.write("\r[{}{}] ".format("=" * done, " " * (50 - done)))
    sys.stdout.flush()


@app.command()
def download(
    link: str,
    path: Path = Path.home() / "Videos" / "Playlists",
):
    """
    Downloads a YouTube playlist to the specified path.

    Args:
        link (str): The link of the YouTube playlist to be downloaded.
        path (Path): The path where the playlist will be saved. Defaults to "./Playlists".

    Returns:
        None

    This function uses the pytube library to download the playlist from the given link. It creates a directory with the playlist's title and saves each video in the playlist to that directory. The videos are saved with a prefix indicating their order in the playlist.

    Example:
        >>> download("https://www.youtube.com/playlist?list=PLo9Vi5B84_dfAuwJqNYG4XhZMrGTF3sBx", Path("./Playlists"))
        Downloading Video: Video Title 1
        Downloading Video: Video Title 2
        ...
    """

    download_playlist(link, path)


if __name__ == "__main__":
    app()
