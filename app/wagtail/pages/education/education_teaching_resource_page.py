import re

from flask import make_response, render_template, request
from pydash import objects


# @cacheable_duration(3600)
def education_teaching_resource_page(page_data):
    if "markdown" in request.args:
        markdown = render_template(
            "education/teaching_resource_markdown.html",
            page_data=page_data,
        )
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        response = make_response(markdown)
        response.headers["Content-Type"] = "text/plain; charset=utf-8"
        response.headers["Content-Disposition"] = (
            f"attachment; filename={objects.get(page_data, 'meta.slug')}.md"
        )
        return response
    if "source_media" in request.args:
        source_media = []
        source_media.append(objects.get(page_data, "hero_image.jpeg.full_url"))
        for source in page_data.get("sources", []):
            for media in [
                media
                for media in source.get("media", [])
                if media.get("type") == "image"
            ]:
                source_media.append(objects.get(media, "value.image.jpeg.full_url"))
        return source_media
    return render_template(
        "education/teaching_resource.html",
        page_data=page_data,
    )
