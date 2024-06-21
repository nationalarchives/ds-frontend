import urllib.parse


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
                value
                for value in args_dict[key_to_remove]
                if value != value_to_remove
            ]
    return (
        args_dict
        if return_dict
        else f"?{urllib.parse.urlencode(args_dict, doseq=True)}"
    )
