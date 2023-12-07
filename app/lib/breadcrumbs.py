from app.lib.wagtail import page_ancestors


def breadcrumbs(page_id):
    ancestors = page_ancestors(page_id)
    return (
        [
            {
                "text": "Home"
                if ancestor["meta"]["type"] == "home.HomePage"
                else ancestor["title"],
                "href": ancestor["meta"]["html_url"],
            }
            for ancestor in ancestors["items"]
        ]
        if ancestors
        else []
    )
