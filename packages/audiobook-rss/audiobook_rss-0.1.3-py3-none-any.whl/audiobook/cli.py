from ebooklib import epub
import io
import time
from pathlib import Path
import rich.table
import typer
import typer.rich_utils
from audiobook.config import Config
from audiobook.servant import FeedServant
from audiobook.generate import (
    parse_book,
    generate_book,
)
from opendal import Operator
import tomli
from rich.progress import track
from tempfile import NamedTemporaryFile
import rich

app = typer.Typer()


class State:
    config: Config
    op: Operator
    servant: FeedServant


@app.callback()
def before_command(config: str = "config.toml"):
    with open(config, "rb") as f:
        State.config = Config.model_validate(tomli.load(f))
    State.op = Operator(**State.config.audiobook.opendal)
    State.servant = FeedServant(op=State.op)


@app.command()
def create(epubfile: str):
    # Parse epub
    book = parse_book(epub.read_epub(epubfile), Path(epubfile).stem)

    # Select chapters
    console = rich.console.Console()
    table = rich.table.Table("No.", "Name", "Count", "Preview", title="Chapters")
    for idx, info in enumerate(book.chapters):
        preview = info.text.strip().replace("\n", "")[:15] + "..."
        cnt = len(info.text)
        table.add_row(
            f"[green]{str(idx)}[/green]",
            info.title,
            f"[bold red]{cnt}[/bold red]" if cnt > 20000 else f"{cnt}",
            preview,
        )
    console.print(table)

    user_input = typer.prompt("Select chapters (e.g. 1, 2-3)")
    selected_chaps = parse_int_range(user_input)

    # Generate audio and write to opendal
    for idx, audio in track(
        generate_book(book, selected_chaps, State.config.inferpool),
        total=len(selected_chaps),
    ):
        with io.BytesIO() as in_memory_file:
            audio.export(in_memory_file, format="mp3")
            State.op.write(
                f"{book.name}/{book.chapters[idx].title}.mp3", in_memory_file.read()
            )
        State.op.write(
            f"{book.name}/{book.chapters[idx].title}.txt",
            book.chapters[idx].text.encode(),
        )


@app.command()
def listbook():
    for entry in State.servant.all_books():
        print(entry)


def parse_int_range(input_str: str):
    ranges = input_str.split(",")
    result = []
    for part in ranges:
        if "-" in part:
            start, end = map(int, part.split("-"))
            result.extend(range(start, end + 1))
        else:
            result.append(int(part))
    return result


def main():
    app()


if __name__ == "__main__":
    main()
