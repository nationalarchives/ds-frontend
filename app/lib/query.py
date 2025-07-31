from urllib.parse import urlencode


def qs_active(existing_qs, filter, by):
    """Active when identical key/value in existing query string."""
    qs_set = {(filter, str(by))}
    # Not active if either are empty.
    if not existing_qs or not qs_set:
        return False
    # See if the intersection of sets is the same.
    existing_qs_set = set(existing_qs.items())
    return existing_qs_set.intersection(qs_set) == qs_set


def qs_toggler(existing_qs, filter, by):
    """Resolve filter against an existing query string."""
    qs = {filter: by}
    # Don't change the currently rendering existing query string!
    rtn_qs = existing_qs.copy()
    # Test for identical key and value in existing query string.
    if qs_active(existing_qs, filter, by):
        # Remove so that buttons toggle their own value on and off.
        rtn_qs.pop(filter)
    else:
        # Update or add the query string.
        rtn_qs.update(qs)
    return urlencode(rtn_qs)


def qs_update(existing_qs, filter, value):
    rtn_qs = existing_qs.copy()
    try:
        rtn_qs.pop(filter)
    except KeyError:
        pass
    rtn_qs.update({filter: value})
    return urlencode(rtn_qs)


def qs_remove(existing_qs, filter):
    rtn_qs = existing_qs.copy()
    try:
        rtn_qs.pop(filter)
    except KeyError:
        pass
    return urlencode(rtn_qs)


def parse_args(args):
    args_dict = args.to_dict(flat=False)
    return_args = {}
    for arg_key in args_dict:
        if arg_key.endswith("[]"):
            arg_key_clipped = arg_key.removesuffix("[]")
            return_args[arg_key_clipped] = args_dict[arg_key]
        else:
            return_args[arg_key] = args_dict[arg_key][0]
    return return_args


def remove_arg(args, key_to_remove, value_to_remove=None, return_dict=False):
    args_dict = args.to_dict(flat=False)
    if value_to_remove:
        key_to_remove = f"{key_to_remove}[]"
    if key_to_remove in args_dict:
        if not value_to_remove:
            del args_dict[key_to_remove]
        else:
            args_dict[key_to_remove] = [
                value for value in args_dict[key_to_remove] if value != value_to_remove
            ]
    return args_dict if return_dict else f"?{urlencode(args_dict, doseq=True)}"
