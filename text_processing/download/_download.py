from polyglot.downloader import downloader
from polyglot.load import locate_resource


def download(obj: str, lang: str) -> None:
    try:
        locate_resource(obj, lang=lang)
    except ValueError:
        print(f"Downloading {lang}-{obj}...")
        downloader.download(f"{obj}.{lang}", quiet=True)
