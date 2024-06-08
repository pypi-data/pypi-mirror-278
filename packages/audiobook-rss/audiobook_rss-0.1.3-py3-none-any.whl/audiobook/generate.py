import re
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from pydub import AudioSegment
from typing import Optional, List
from pathlib import Path
from audiobook.config import Config, InferPoolConfig
from pydantic import BaseModel


def chapter_to_str(soup: BeautifulSoup):
    all_text = ""
    for child in soup.children:
        if child.name in {None, "a", "span", "strong", "em"}:
            text = child.get_text(strip=True)
            text = re.sub(r"\[\d+\]", "", text)  # Replace like [1]
            all_text += text
        else:
            all_text += "\n" + chapter_to_str(child)
    return all_text


def extract_title(soup: BeautifulSoup):
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text(separator=",", strip=True)

    for header_tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        header = soup.find(header_tag)
        if header:
            return header.get_text(separator=",", strip=True)

    return "Unknown"


def make_filename_safe(input_str):
    cleaned_str = re.sub(r'[\\/*?:"<>|]', " ", input_str)
    cleaned_str = " ".join(cleaned_str.split())[:255]
    return cleaned_str


def load_infer_pool(config: InferPoolConfig):

    from gpt_sovits.infer.inference_pool import GPTSoVITSInferencePool

    path_base = Path(config.path_base)
    with open(path_base / "prompts" / f"{config.prompt_name}.txt") as f:
        prompt_text = f.read().strip()
    return GPTSoVITSInferencePool(
        bert_path=str(path_base / "chinese-roberta-wwm-ext-large"),
        cnhubert_base_path=str(path_base / "chinese-hubert-base"),
        gpt_path=str(path_base / "models" / f"{config.tts_model_name}.ckpt"),
        sovits_path=str(path_base / "models" / f"{config.tts_model_name}.pth"),
        prompt_text=prompt_text,
        prompt_audio_path=str(path_base / "prompts" / f"{config.prompt_name}.wav"),
        device=config.device,
        is_half=config.is_half,
        max_workers=config.max_workers,
    )


class ChapterInfo(BaseModel):
    href: str
    title: str
    text: str


class BookInfo(BaseModel):
    name: str
    chapters: List[ChapterInfo]


def parse_book(book: epub.EpubBook, name: str):
    chapters = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
    cnt_chap = len(chapters)
    max_length = len(str(cnt_chap - 1))
    tmp = [
        (
            idx,
            chapter.file_name,
            BeautifulSoup(chapter.get_body_content(), "html.parser"),
        )
        for idx, chapter in enumerate(chapters)
    ]
    return BookInfo(
        name=name,
        chapters=[
            ChapterInfo(
                href=href,
                text=chapter_to_str(soup),
                title=f"{str(idx).zfill(max_length)}"
                "-"
                f"{make_filename_safe(extract_title(soup))}",
            )
            for idx, href, soup in tmp
        ],
    )


def generate_book(
    book: BookInfo,
    selected_chaps: List[int],
    inferpool_conf: InferPoolConfig,
):
    # Load inference pool

    infer = load_infer_pool(inferpool_conf)

    try:
        for idx in selected_chaps:
            text = book.chapters[idx].text
            sr, data = infer.get_tts_wav(text)
            audio = AudioSegment(
                data=data.tobytes(),
                sample_width=data.dtype.itemsize,
                frame_rate=sr,
                channels=1,
            )
            yield idx, audio
    except Exception as e:
        raise e
    finally:
        infer.pool.shutdown()
