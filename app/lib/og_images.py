import os
from dataclasses import dataclass
from html.parser import HTMLParser
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


class ContentExtractor(HTMLParser):
    def __init__(self, max_length=None):
        super().__init__()
        self.max_length = max_length

    def escape_and_truncate(self, content):
        content = content.strip()
        content = escape(Markup(content).striptags())
        if self.max_length is not None and len(content) > self.max_length:
            content = f"{content[: self.max_length].strip()}..."
        return content


class StrictSupertitleExtractor(ContentExtractor):
    def __init__(self):
        super().__init__()
        self.supertitle_text = []
        self._in_hgroup = False
        self._has_h1 = False
        self._in_supertitle = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "").split()

        if tag == "hgroup":
            self._in_hgroup = True

        if self._in_hgroup:
            if tag == "h1":
                self._has_h1 = True
            if "tna-hgroup__supertitle" in classes:
                self._in_supertitle = True

    def handle_endtag(self, tag):
        if tag == "hgroup":
            self._in_hgroup = False
        elif tag == "p" or tag == "span":
            self._in_supertitle = False

    def handle_data(self, data):
        if self._in_hgroup and self._in_supertitle:
            self.supertitle_text.append(data)

    def get_supertitle(self):
        # Only return the text if an <h1> was confirmed inside the <hgroup>
        if self._has_h1:
            combined = "".join(self.supertitle_text).strip()
            return combined if combined else None
        return None


class TitleExtractor(ContentExtractor):
    def __init__(self):
        super().__init__(current_app.config["OG_EXTERNAL_CONTENT_MAX_TITLE_LENGTH"])
        self.og_title = None
        self.h1_text = []
        self.title_text = []
        self._current_tag = None

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attr_dict = dict(attrs)
            if attr_dict.get("property") == "og:title":
                self.og_title = attr_dict.get("content")
        elif tag in ("h1", "title"):
            self._current_tag = tag

    def handle_endtag(self, tag):
        if tag in ("h1", "title"):
            self._current_tag = None

    def handle_data(self, data):
        if self._current_tag == "h1":
            self.h1_text.append(data)
        elif self._current_tag == "title":
            self.title_text.append(data)

    def get_title(self):
        # 1. First priority: og:title
        if self.og_title:
            return self.escape_and_truncate(self.og_title)

        # 2. Second priority: <h1>
        h1_combined = "".join(self.h1_text).strip()
        if h1_combined:
            return self.escape_and_truncate(h1_combined)

        # 3. Third priority: <title>
        title = "".join(self.title_text).strip()
        if title:
            return self.escape_and_truncate(title)

        return None


class DescriptionExtractor(ContentExtractor):
    def __init__(self):
        super().__init__(current_app.config["OG_EXTERNAL_CONTENT_MAX_BODY_LENGTH"])
        self.og_description = None
        self.meta_description = None
        self._current_tag = None

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            attr_dict = dict(attrs)
            if attr_dict.get("property") == "og:description":
                self.og_description = attr_dict.get("content")
            elif attr_dict.get("name") == "description":
                self.meta_description = attr_dict.get("content")

    def get_description(self):
        if self.og_description:
            return self.escape_and_truncate(self.og_description)
        if self.meta_description:
            return self.escape_and_truncate(self.meta_description)
        return None


def generate_external_og_image(page_path):
    try:
        response = requests.get(
            f"{current_app.config['OG_CONTENT_BASE_URL']}/{page_path.strip('/')}/",
            timeout=3,
        )
    except Exception:
        current_app.logger.exception(
            f"Failed to fetch page data for external OG image: {page_path}"
        )
        return generate_blank_og_image()

    if not response.ok:
        current_app.logger.info(
            f"Failed to fetch page data for external OG image: {page_path}"
        )
        return generate_blank_og_image()

    try:
        content = response.content.decode("utf-8")
    except UnicodeDecodeError:
        current_app.logger.exception(
            f"Failed to decode page content for external OG image: {page_path}"
        )
        return generate_blank_og_image()

    supertitle_parser = StrictSupertitleExtractor()
    supertitle_parser.feed(content)
    supertitle = supertitle_parser.get_supertitle()

    title_parser = TitleExtractor()
    title_parser.feed(content)
    title = title_parser.get_title()

    description_parser = DescriptionExtractor()
    description_parser.feed(content)
    description = description_parser.get_description()

    if title and description:
        return generate_og_image(
            supertitle,
            title,
            description,
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
            if not response.ok:
                current_app.logger.error(f"Failed to fetch teaser image: {image}")
            else:
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
