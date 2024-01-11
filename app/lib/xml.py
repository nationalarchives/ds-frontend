from pyquery import PyQuery


def parse_cdata(val):
    document = PyQuery(val)
    for tag in ("foa", "function"):
        if doc_value := document(tag).text():
            return doc_value
    return val
