from tna_utilities.urls import QueryStringTransformer


def qs_active(request, filter, by):
    qs = QueryStringTransformer(list(request.args.lists()))
    qs.is_value_in_parameter(filter, by)
    return qs.get_query_string()


def qs_toggler(request, filter, by):
    qs = QueryStringTransformer(list(request.args.lists()))
    qs.toggle_parameter_value(filter, by)
    return qs.get_query_string()


def qs_update(request, filter, value):
    qs = QueryStringTransformer(list(request.args.lists()))
    qs.update_parameter(filter, value)
    return qs.get_query_string()


def qs_remove(request, filter):
    qs = QueryStringTransformer(list(request.args.lists()))
    qs.remove_parameter(filter)
    return qs.get_query_string()
