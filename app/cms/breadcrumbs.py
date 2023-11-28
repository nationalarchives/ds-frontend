import requests


def breadcrumbs(page_id):
    ancestors = requests.get(
        "http://host.docker.internal:8000/api/v2/pages/?ancestor_of=%d"
        % page_id
    )
    return (
        [
            {
                "title": "Home"
                if ancestor["meta"]["html_url"] == "http://localhost:65535/"
                else ancestor["title"],
                "url": ancestor["meta"]["html_url"],
            }
            for ancestor in ancestors.json()["items"]
        ]
        if ancestors
        else []
    )
