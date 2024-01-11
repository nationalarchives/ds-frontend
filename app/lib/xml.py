from pyquery import PyQuery


def strip_scope_and_content(markup):
    document = PyQuery(markup)
    return str(document("span.scopecontent").contents().eq(0))
