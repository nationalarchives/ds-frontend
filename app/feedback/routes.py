import urllib.parse
from urllib.parse import parse_qs, urlparse

from app.feedback import bp
from flask import redirect, request


@bp.route("/submit/", methods=["POST"])
def submit():
    print(request.form)
    response = "Thank you for your feedback"
    more_questions = True
    if return_path := request.args.get("return"):
        parsed_url = urlparse(return_path)
        query_params = parse_qs(parsed_url.query, keep_blank_values=True)
        return_url = f"{return_path.rstrip('?')}{'&' if query_params else '?'}feedback_response={urllib.parse.quote(response)}"
        if more_questions:
            return_url = f"{return_url}&feedback_additional=true"
        return_url = f"{return_url}#feedback"
        return redirect(return_url)
    return response
