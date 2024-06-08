import mimetypes
from opendal import Operator, EntryMode
from feedgen.feed import FeedGenerator
from pathlib import Path
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone


class Episode(BaseModel):
    name: str
    extension: str
    path: Path


class FeedServant:
    op: Operator

    def __init__(self, op: Operator):
        self.op = op

    def all_books(self):
        entries = [
            Path(entry.path)
            for entry in self.op.list("/")
            if self.op.stat(entry.path).mode.is_dir()
        ]
        return [entry.stem for entry in entries]

    def get_book_eps(self, book: str):
        extensions = {".mp3"}
        eps = [
            Path(entry.path)
            for entry in self.op.list(f"{book}/")
            if Path(entry.path).suffix in extensions
        ]
        eps.sort(key=lambda x: x.stem)
        return [
            Episode(
                name=entry.stem,
                extension=entry.suffix,
                path=entry,
            )
            for entry in eps
        ]

    def get_book_feed(self, book: str, url_base: str):
        eps = self.get_book_eps(book)
        book_link = f"{url_base}feed/{book}"
        fg = FeedGenerator()
        fg.load_extension("podcast")
        fg.id(book_link)
        fg.title(book)
        fg.description(book)
        fg.link(href=book_link)
        pub_time = datetime.fromtimestamp(0, tz=timezone.utc)
        for ep in eps[::-1]:
            ep_link = f"{url_base}file/{book}/{ep.name}{ep.extension}"
            fe = fg.add_entry(order="append")
            fe.id(ep_link)
            fe.title(ep.name)
            fe.description(
                f'<a href="{url_base}text/{book}/{ep.name}.txt">Origin Text</a>'
            )
            fe.enclosure(ep_link, 0, f"audio/{mimetypes.types_map[ep.extension]}")
            fe.published(pub_time)
            pub_time = pub_time + timedelta(days=1)

        return fg.rss_str(pretty=True)
