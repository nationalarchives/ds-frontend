import os
import re
from dataclasses import dataclass
from io import BytesIO

import requests
from flask import current_app, send_file
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pydash import objects


@dataclass
class SegmentFont:
    image_font: ImageFont.FreeTypeFont
    color: str
    line_height: int
    background_color: str = None
    padding: int = 0
    margin_top: int = 0


OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
OG_IMAGE_BACKGROUND_COLOR = "#dde5d5"


def generate_static_paths():
    static_dir = os.path.join(current_app.root_path, "static", "assets")
    logo_path = os.path.join(static_dir, "images", "icon-1024x1024.png")
    heading_font_path = os.path.join(static_dir, "fonts", "OpenSans-Bold.ttf")
    body_font_path = os.path.join(static_dir, "fonts", "OpenSans-Regular.ttf")
    monospace_font_path = os.path.join(static_dir, "fonts", "RobotoMono-Regular.ttf")
    return logo_path, heading_font_path, body_font_path, monospace_font_path


def generate_blank_og_image():
    LOGO_SIZE = 350

    logo_path, _heading_font_path, _body_font_path, _monospace_font_path = (
        generate_static_paths()
    )

    canvas = Image.new(
        "RGB", (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT), color=OG_IMAGE_BACKGROUND_COLOR
    )

    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((LOGO_SIZE, LOGO_SIZE))
    canvas.paste(
        logo,
        ((OG_IMAGE_WIDTH - LOGO_SIZE) // 2, (OG_IMAGE_HEIGHT - LOGO_SIZE) // 2),
        logo,
    )

    buffer = BytesIO()
    canvas.save(buffer, format="WEBP", quality=80)
    buffer.seek(0)
    return send_file(buffer, mimetype="image/webp")


def generate_external_og_image(page_path):
    try:
        response = requests.get(
            f"https://www.nationalarchives.gov.uk/{page_path.strip('/')}/",
            timeout=3,
        )
        response.raise_for_status()
        content = response.content.decode("utf-8")

        title_match = re.search(r"<h1.*?>(.*?)</h1>", content, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                title_suffixes = [
                    " - The National Archives",
                    " | The National Archives",
                ]
                for title_suffix in title_suffixes:
                    if title.endswith(title_suffix):
                        title = title[: -len(title_suffix)].strip()
            else:
                title = "Untitled"

        description_match = re.search(
            r'<meta\s+name="description"\s+content="(.*?)"\s*/?>',
            content,
            re.IGNORECASE,
        )
        if description_match:
            teaser_text = description_match.group(1).strip()
        else:
            teaser_text = ""
    except Exception:  # noqa: BLE001
        current_app.logger.warning(
            "Failed to fetch page data for external OG image: %s", page_path
        )
        return generate_blank_og_image()

    if title and teaser_text:
        return generate_og_image(
            "",
            title,
            teaser_text,
            "https://www.nationalarchives.gov.uk/media/images/dz-grounds-of-the-_NkT30gt.976d85da.fill-1800x720.format-webp.webpquality-70.bgcolor-fff.webp",
        )
    return generate_blank_og_image()


def generate_og_image_from_page_data(page_data):
    supertitle = (page_data.get("type_label") or "").upper()
    title = page_data.get("short_title", "") or page_data.get("title", "")
    teaser_text = page_data.get("meta", {}).get("teaser_text", "")
    teaser_image = (
        objects.get(page_data, "meta.search_image.jpeg.full_url")
        or objects.get(page_data, "meta.teaser_image.jpeg.full_url")
        or objects.get(page_data, "hero_image.small_jpeg.full_url", "")
    ).replace("localhost", "host.docker.internal")

    return generate_og_image(supertitle, title, teaser_text, teaser_image)


def generate_og_image(supertitle, title, teaser_text, teaser_image):
    PADDING_X = 45
    PADDING_Y = 70
    LOGO_SIZE = 90

    logo_path, heading_font_path, body_font_path, monospace_font_path = (
        generate_static_paths()
    )

    supertitle_font = SegmentFont(
        ImageFont.truetype(monospace_font_path, 16), "#ffffff", 21, "#00623b", padding=6
    )
    heading_font = SegmentFont(ImageFont.truetype(heading_font_path, 44), "#010101", 50)
    body_font = SegmentFont(
        ImageFont.truetype(body_font_path, 22), "#343338", 36, margin_top=30
    )
    footer_font = SegmentFont(
        ImageFont.truetype(body_font_path, 18), "#343338", LOGO_SIZE // 3
    )

    canvas = Image.new(
        "RGB", (OG_IMAGE_WIDTH, OG_IMAGE_HEIGHT), color=OG_IMAGE_BACKGROUND_COLOR
    )
    draw = ImageDraw.Draw(canvas)

    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((LOGO_SIZE, LOGO_SIZE))
    canvas.paste(logo, (PADDING_X, OG_IMAGE_HEIGHT - PADDING_X - LOGO_SIZE), logo)
    draw.text(
        (
            PADDING_X + LOGO_SIZE + 20,
            OG_IMAGE_HEIGHT - PADDING_X - footer_font.line_height,
        ),
        "www.nationalarchives.gov.uk",
        font=footer_font.image_font,
        fill=footer_font.color,
    )

    if teaser_image:
        try:
            response = requests.get(teaser_image, timeout=3)
            response.raise_for_status()
            visitor_image = Image.open(BytesIO(response.content)).convert("RGB")
            resized_visitor_image = ImageOps.fit(
                visitor_image,
                (OG_IMAGE_WIDTH // 2, OG_IMAGE_HEIGHT),
                Image.Resampling.LANCZOS,
            )
            canvas.paste(
                resized_visitor_image,
                (OG_IMAGE_WIDTH // 2, 0),
            )
        except Exception:  # noqa: BLE001
            current_app.logger.warning(
                "Failed to fetch or process teaser image: %s", teaser_image
            )

    text_segments = []
    if supertitle:
        text_segments.append((supertitle, supertitle_font))
    text_segments.append((title, heading_font))
    if teaser_text:
        text_segments.append((teaser_text, body_font))

    max_text_width = (OG_IMAGE_WIDTH // 2) - (PADDING_X * 2)
    start_x, start_y = PADDING_X, PADDING_Y
    x, y = start_x, start_y
    words = []
    for text, font in text_segments:
        segment_words = [word for word in text.split(" ") if word]
        for index, word in enumerate(segment_words):
            is_first_word = index == 0
            is_last_word = index == len(segment_words) - 1
            words.append((word + " ", font, is_first_word, is_last_word))

    for word, font, is_first_word, is_last_word in words:
        if is_first_word:
            x = start_x
            y += font.margin_top

        word_width = draw.textlength(word, font=font.image_font)

        if x + word_width > start_x + max_text_width:
            x = start_x
            y += font.line_height

        has_background = font.background_color and word.strip()
        if has_background:
            draw.rectangle(
                [
                    (x, y),
                    (x + word_width, y + font.line_height),
                ],
                fill=font.background_color,
            )

        draw.text(
            (x + font.padding if has_background else x, y),
            word,
            font=font.image_font,
            fill=font.color,
        )

        if is_last_word:
            x = start_x
            y += font.line_height
        else:
            x += word_width

    buffer = BytesIO()
    canvas.save(buffer, format="WEBP", quality=80)
    buffer.seek(0)
    return send_file(buffer, mimetype="image/webp")
