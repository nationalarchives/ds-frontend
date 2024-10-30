from app.lib.pagination import pagination_object
from app.wagtail.api import breadcrumbs
from flask import render_template, request


def person_page(page_data):
    page = (
        int(request.args.get("page"))
        if request.args.get("page") and request.args.get("page").isnumeric()
        else 0
    )
    pages = 0  # TODO
    if page > pages:
        return render_template("errors/page-not-found.html"), 404
    return render_template(
        "people/person.html",
        breadcrumbs=breadcrumbs(page_data["id"]),
        page_data=page_data,
        pagination=pagination_object(page, pages, request.args),
        page=page,
        pages=pages,
    )
