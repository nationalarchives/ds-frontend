def pick_top_two(a, b):
    if len(a) and len(b):
        return [a[0], b[0]]
    elif len(a):
        return [a[0], a[1]] if len(a) > 1 else [a[0]]
    elif len(b):
        return [b[0], b[1]] if len(b) > 1 else [b[0]]
    return []


def pages_to_index_grid_items(pages):
    return [
        {
            "href": page["url"],
            "label": page["type_label"],
            "title": page["title"],
            "src": page["teaser_image"]["jpeg"]["url"],
            "alt": "",
            "width": page["teaser_image"]["jpeg"]["width"],
            "height": page["teaser_image"]["jpeg"]["height"],
        }
        for page in pages
    ]
