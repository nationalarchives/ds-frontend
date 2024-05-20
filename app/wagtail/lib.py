def pick_top_two(a, b):
    selection = []
    if len(a) and len(b):
        selection = [a[0], b[0]]
    elif len(a):
        selection = [a[0], a[1] or None]
    elif len(b):
        selection = [b[0], b[1] or None]
    return selection


def pages_to_index_grid_items(pages, label=""):
    return [
        {
            "href": page["url"],
            "label": label,
            "title": page["title"],
            "src": page["teaser_image"]["jpeg"]["full_url"],
            # TODO
            # "alt": page["teaser_image"]["alt_text"],
            "width": page["teaser_image"]["jpeg"]["width"],
            "height": page["teaser_image"]["jpeg"]["height"],
        }
        for page in pages
    ]
