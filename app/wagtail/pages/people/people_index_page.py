from app.wagtail.api import page_children
from flask import current_app, render_template


def people_index_page(page_data):
    # try:
    #     children = page_children(
    #         page_data["id"],
    #         {
    #             "type": "people.PersonPage",
    #             # "fields": "_,title,image,role,url,image",
    #             "order": "last_name",
    #         },
    #     )
    # except ConnectionError:
    #     current_app.logger.error(
    #         f"API error getting children for page {page_data['id']}"
    #     )
    #     return render_template("errors/api.html"), 502
    # except Exception:
    #     current_app.logger.error(
    #         f"Exception getting children for page {page_data['id']}"
    #     )
    #     return render_template("errors/server.html"), 500
    return render_template(
        "people/index.html",
        # people=children["items"],
        # people_total=children["meta"]["total_count"],
        page_data=page_data,
    )
