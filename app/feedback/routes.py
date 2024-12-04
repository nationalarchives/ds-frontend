import uuid
from urllib.parse import parse_qsl, urlparse

from app.feedback import bp
from app.lib.template_filters import qs_toggler
from flask import redirect, request


@bp.route("/submit/", methods=["POST"])
def submit():
    # TODO: After submitting the first response, get the group ID so we can post more responses in the same set
    id = request.form.get("feedback_id") or str(uuid.uuid4())
    current_index = int(request.form.get("index") or "1")
    print(request.form)
    if return_path := request.args.get("return"):
        parsed_url = urlparse(return_path)
        query_params = dict(parse_qsl(parsed_url.query))
        if "feedback_id" not in query_params:
            query_params["feedback_id"] = id
        new_query_params = qs_toggler(
            query_params, "feedback_index", current_index + 1
        )
        return_url = f"{parsed_url.path.rstrip('?')}?{new_query_params}#{id}"
        return redirect(return_url)
    return "Thank you for your feedback"
