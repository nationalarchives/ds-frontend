import os
import re
from dataclasses import dataclass
from io import BytesIO

import requests
from flask import current_app, send_file
from markupsafe import Markup, escape
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
OG_IMAGE_JPEG_QUALITY = 80
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
    canvas.save(buffer, format="JPEG", quality=OG_IMAGE_JPEG_QUALITY)
    buffer.seek(0)
    return send_file(buffer, mimetype="image/jpeg")


def generate_external_og_image(page_path):
    try:
        response = requests.get(
            f"{current_app.config['OG_CONTENT_BASE_URL']}/{page_path.strip('/')}/",
            timeout=3,
        )
        response.raise_for_status()
        content = response.content.decode("utf-8")

        supertitle = None
        title = None
        body = None

        supertitle_match = re.search(
            r'<hgroup class="tna-hgroup-xl">\s*<p class="tna-hgroup__supertitle">(.*)</p>\s*<h1[ >]',
            content,
            re.IGNORECASE | re.DOTALL,
        )
        if supertitle_match:
            supertitle = supertitle_match.group(1).strip().upper()
        else:
            supertitle_match_alt = re.search(
                r'<hgroup class="tna-hgroup-xl">\s*<h1>\s*<span class="tna-hgroup__supertitle">(.*)</span>',
                content,
                re.IGNORECASE | re.DOTALL,
            )
            if supertitle_match_alt:
                supertitle = supertitle_match_alt.group(1).strip().upper()
        if supertitle:
            supertitle = escape(Markup(supertitle).striptags())

        og_title_match = re.search(
            r'<meta\s+property="og:title"\s+content="(.*)"\s*/?>',
            content,
            re.IGNORECASE,
        )
        if og_title_match:
            title = og_title_match.group(1).strip()
        else:
            title_match = re.search(r"<h1.*>(.*)</h1>", content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
            else:
                title_match = re.search(r"<title>(.*)</title>", content, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    title_suffixes = [
                        " - The National Archives",
                        " | The National Archives",
                    ]
                    for title_suffix in title_suffixes:
                        if title.endswith(title_suffix):
                            title = title[: -len(title_suffix)].strip()
        if title:
            title = escape(Markup(title).striptags())
            if len(title) > current_app.config["OG_EXTERNAL_CONTENT_MAX_TITLE_LENGTH"]:
                title = f"{title[: current_app.config['OG_EXTERNAL_CONTENT_MAX_TITLE_LENGTH']].strip()}..."

        og_description_match = re.search(
            r'<meta\s+property="og:description"\s+content="(.*?)"\s*/?>',
            content,
            re.IGNORECASE,
        )
        if og_description_match:
            body = og_description_match.group(1).strip()
        else:
            description_match = re.search(
                r'<meta\s+name="description"\s+content="(.*?)"\s*/?>',
                content,
                re.IGNORECASE,
            )
            if description_match:
                body = description_match.group(1).strip()
        if body:
            body = escape(Markup(body).striptags())
            if len(body) > current_app.config["OG_EXTERNAL_CONTENT_MAX_BODY_LENGTH"]:
                body = f"{body[: current_app.config['OG_EXTERNAL_CONTENT_MAX_BODY_LENGTH']].strip()}..."

    except Exception:
        current_app.logger.exception(
            f"Failed to fetch page data for external OG image: {page_path}"
        )
        return generate_blank_og_image()

    if title and body:
        return generate_og_image(
            supertitle,
            title,
            body,
            current_app.config["OG_DEFAULT_IMAGE"],
        )
    return generate_blank_og_image()


def generate_og_image_from_page_data(page_data):
    supertitle = (page_data.get("type_label") or "").upper()
    title = (
        objects.get(page_data, "meta.seo_title", "")
        or page_data.get("short_title", "")
        or page_data.get("title", "")
    )
    body = objects.get(page_data, "meta.search_description", "") or objects.get(
        page_data, "meta.teaser_text", ""
    )
    image = (
        objects.get(page_data, "meta.search_image.jpeg.full_url")
        or objects.get(page_data, "meta.teaser_image.jpeg.full_url")
        or objects.get(page_data, "hero_image.small_jpeg.full_url", "")
    ) or current_app.config["OG_DEFAULT_IMAGE"]

    return generate_og_image(supertitle, title, body, image)


def generate_og_image(supertitle, title, body, image):
    PADDING_X = 45
    PADDING_Y = 70
    LOGO_SIZE = 90
    IMAGE_PADDING = PADDING_X

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

    if image:
        try:
            response = requests.get(image, timeout=3)
            response.raise_for_status()
            image_data = Image.open(BytesIO(response.content)).convert("RGB")
            resized_image = ImageOps.fit(
                image_data,
                (
                    (OG_IMAGE_WIDTH // 2) - (IMAGE_PADDING * 2),
                    OG_IMAGE_HEIGHT - (IMAGE_PADDING * 2),
                ),
                Image.Resampling.LANCZOS,
            )
            canvas.paste(
                resized_image,
                (OG_IMAGE_WIDTH // 2 + IMAGE_PADDING, IMAGE_PADDING),
            )
        except Exception:
            current_app.logger.exception(
                f"Failed to fetch or process teaser image: {image}"
            )

    text_segments = []
    if supertitle:
        text_segments.append((supertitle, supertitle_font))
    text_segments.append((title, heading_font))
    text_segments.append((body, body_font))

    max_text_width = (OG_IMAGE_WIDTH // 2) - (PADDING_X * 2) + IMAGE_PADDING
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
    canvas.save(buffer, format="JPEG", quality=OG_IMAGE_JPEG_QUALITY)
    buffer.seek(0)
    return send_file(buffer, mimetype="image/jpeg")
