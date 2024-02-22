import urllib.parse


def pagination_list(current_page, total_pages, boundaries=1, around=1):
    assert current_page >= 0, "current_page is less than zero"
    assert total_pages >= 0, "total_pages is less than zero"
    assert boundaries >= 0, " boundaries is less than zero"
    assert around >= 0, "around is less than zero"
    assert (
        current_page <= total_pages
    ), "current_page is bigger than total_pages"

    start_initial_chunk = 1
    end_initial_chunk = min(boundaries, total_pages) + 1

    start_middle_chunk = max(end_initial_chunk, current_page - around, 1)
    end_middle_chunk = min(current_page + around, total_pages) + 1
    start_final_chunk = max(
        end_middle_chunk, total_pages - boundaries + 1, boundaries + 1
    )
    end_final_chunk = total_pages + 1

    initial_chunk_numbers = list(range(start_initial_chunk, end_initial_chunk))
    middle_chunk_numbers = list(range(start_middle_chunk, end_middle_chunk))
    final_chunk_numbers = list(range(start_final_chunk, end_final_chunk))

    prev_linker = (
        end_initial_chunk
        if end_initial_chunk == 2 and current_page - (around + 1) == 2
        else (
            "..."
            if end_initial_chunk < start_middle_chunk
            and len(middle_chunk_numbers) > 0
            else ""
        )
    )
    next_linker = (
        end_middle_chunk
        if end_middle_chunk == (total_pages - 1)
        and current_page + (around + 1) == (total_pages - 1)
        else (
            "..."
            if end_middle_chunk < start_final_chunk
            else "" if boundaries + 1 <= end_middle_chunk else ""
        )
    )

    pagination_items = (
        initial_chunk_numbers
        + [prev_linker]
        + middle_chunk_numbers
        + [next_linker]
        + final_chunk_numbers
    )

    return [item for item in pagination_items if item]


def generate_new_page_query_string(args, page):
    args_dict = args.to_dict(flat=False) | {"page": page}
    return f"?{urllib.parse.urlencode(args_dict, doseq=True)}"


def pagination_object(
    current_page, total_pages, current_args, boundaries=1, around=1
):
    if total_pages == 0:
        return {}
    current_page = int(current_page)
    pagination_object = {}
    pagination_object["items"] = [
        (
            {"ellipsis": True}
            if item == "..."
            else {
                "number": item,
                "href": generate_new_page_query_string(current_args, item),
                "current": item == current_page,
            }
        )
        for item in pagination_list(
            current_page, total_pages, boundaries, around
        )
    ]
    if current_page > 1:
        pagination_object["previous"] = {
            "href": generate_new_page_query_string(
                current_args, current_page - 1
            )
        }
    if current_page < total_pages:
        pagination_object["next"] = {
            "href": generate_new_page_query_string(
                current_args, current_page + 1
            )
        }
    return pagination_object
