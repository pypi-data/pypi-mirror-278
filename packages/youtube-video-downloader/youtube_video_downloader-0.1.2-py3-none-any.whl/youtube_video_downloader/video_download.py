import sys
from pathlib import Path
import typer
import pytube

app = typer.Typer()


def download_video(video_link, path):
    """
    Downloads a video from the given video link and saves it to the specified path.

    Args:
        video_link (str): The link of the video to be downloaded.
        path (Path): The path where the video will be saved.

    Returns:
        None

    Raises:
        None

    This function uses the pytube library to download the video from the given video link.
    It displays a progress bar while downloading the video.
    The downloaded video is saved to the specified path.

    Example:
        >>> download("https://www.youtube.com/watch?v=uKyojQjbx4c", Path("./Videos"))
        Downloading Video:  Video Title
        Video Donwloaded:  Video Title
    """
    yt = pytube.YouTube(video_link, on_progress_callback=progress_func)
    print("Downloading Video: ", yt.title)
    yt.streams.get_highest_resolution().download(output_path=path)

    print("Video Donwloaded: ", yt.title)


def progress_func(stream, chunk, bytes_remaining):
    curr = stream.filesize - bytes_remaining
    done = int(50 * curr / stream.filesize)
    sys.stdout.write("\r[{}{}] ".format("=" * done, " " * (50 - done)))
    sys.stdout.flush()


@app.command()
def download(
    links: list[str] = typer.Argument(None, help="List of links to download"),
    path: Path = typer.Option(Path.home() / "Videos", help="Path to save the videos"),
    file: str = typer.Option(None, "-f", help="Name of the file with the links"),
):
    if file:
        with open(file, "r") as f:
            links = f.read().splitlines()

    for link in links:
        download_video(link, path)


if __name__ == "__main__":
    app()
