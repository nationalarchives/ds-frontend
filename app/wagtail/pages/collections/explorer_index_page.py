from flask import current_app, render_template


def explorer_index_page(page_data):
    print(current_app.config)
    print(current_app.config.get("FEATURE_NEW_ETC_HOMEPAGE"))
    return render_template(
        (
            "explore_the_collection/index-NEW.html"
            if current_app.config.get("FEATURE_NEW_ETC_HOMEPAGE")
            else "explore_the_collection/index.html"
        ),
        page_data=page_data,
    )
