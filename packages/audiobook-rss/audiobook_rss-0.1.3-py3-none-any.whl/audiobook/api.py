from fastapi import FastAPI, Response, Request
from fastapi.responses import PlainTextResponse
from audiobook.servant import FeedServant
from opendal import Operator
from audiobook.config import Config
from jinja2 import Template
import tomli
import os
import click


class State:
    config: Config
    op: Operator
    servant: FeedServant


def on_startup():
    with open(os.getenv("AUDIOBOOK_CONFIG", "config.toml"), "rb") as f:
        State.config = Config.model_validate(tomli.load(f))
    State.op = Operator(**State.config.audiobook.opendal)
    State.servant = FeedServant(op=State.op)


TEMPLATE = Template(
    """<html>
    <style>
        p {
            font-size: 2.5em;
        }
    </style>
    <div>
    {% for i in items %}<p>{{ i }}</p>{% endfor %}
    </div>
</html>"""
)

app = FastAPI(on_startup=[on_startup])


@app.get("/")
def health():
    return {"Hello": "World"}


@app.get("/books")
def list_books(request: Request):
    return Response(
        TEMPLATE.render(
            items=[
                f'- <a href="{request.base_url}feed/{book}">{book}</a>'
                for book in State.servant.all_books()
            ]
        ),
        media_type="text/html",
    )


@app.get("/feed/{book}")
def read_feed(book: str, request: Request):
    return Response(
        content=State.servant.get_book_feed(book, str(request.base_url)),
        media_type="application/rss+xml",
    )


@app.get("/file/{book}/{ep_audio}")
def read_ep_file(book: str, ep_audio: str):
    path = f"{book}/{ep_audio}"
    meta = State.op.stat(path)
    content = State.op.read(path)
    return Response(
        content=content,
        media_type=meta.content_type,
    )


@app.get("/text/{book}/{ep_text}")
def read_ep_text(book: str, ep_text: str):
    path = f"{book}/{ep_text}"
    content: str = State.op.read(path).decode()
    return Response(
        TEMPLATE.render(items=content.split("\n")),
        media_type="text/html",
    )


@click.command()
@click.option("--config", default="config.toml")
@click.option("--port", default=8000)
def start(config: str = "config.toml", port: int = 8000):
    import uvicorn

    os.environ["AUDIOBOOK_CONFIG"] = config
    uvicorn.run(app, port=port)
