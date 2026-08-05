import re

from flask import make_response, render_template, request
from pydash import objects


# @cacheable_duration(3600)
def education_teaching_resource_page(page_data):
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    if "sources" in request.args:
        sources = [
            {
                "source": f"{objects.get(page_data, 'meta.page_path')}?markdown",
                "target": "content.md",
            },
            {
                "source": objects.get(page_data, "hero_image.jpeg.url"),
                "target": "hero.jpg",
            },
        ]
        for source_index, source in enumerate(page_data.get("sources", [])):
            source_images = source.get("media", [])
            for media_index, media in enumerate(source_images):
                if (
                    media.get("type") != "image"
                    or objects.get(media, "value.image.copyright", None)
                    or not objects.get(media, "value.image.jpeg.url", None)
                ):
                    continue
                source_name = f"source-{source_index + 1}"
                if len(source_images) > 1:
                    source_name += f"{alphabet[media_index]}"
                sources.append(
                    {
                        "source": objects.get(media, "value.image.jpeg.url"),
                        "target": f"{source_name}.jpg",
                    }
                )
        return sources

    if "markdown" in request.args:
        markdown = render_template(
            "education/teaching_resource_markdown.html",
            page_data=page_data,
            alphabet=alphabet,
        )
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        response = make_response(markdown)
        response.headers["Content-Type"] = "text/plain; charset=utf-8"
        # response.headers["Content-Disposition"] = (
        #     f"attachment; filename={objects.get(page_data, 'meta.slug')}.md"
        # )
        return response

    return render_template(
        "education/teaching_resource.html", page_data=page_data, alphabet=alphabet
    )
