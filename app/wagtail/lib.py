def pick_top_two(a, b):
    selection = []
    if a.len and b.len:
        selection = [a[0], b[0]]
    elif a.len:
        selection = [a[0], a[1] or None]
    elif b.len:
        selection = [b[0], b[1] or None]
    return selection


def pages_to_index_grid_items(pages, label=""):
    return [
        {
            "href": page["url"],
            "label": label,
            "title": page["title"],
            "src": page["teaser_image_jpeg"]["full_url"],
            "alt": page["teaser_image_jpeg"]["alt"],
            "width": page["teaser_image_jpeg"]["width"],
            "height": page["teaser_image_jpeg"]["height"],
        }
        for page in pages
    ]
