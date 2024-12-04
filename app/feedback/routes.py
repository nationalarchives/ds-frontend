from urllib.parse import parse_qsl, urlparse
import uuid

from app.feedback import bp
from flask import redirect, request
from app.lib.template_filters import qs_toggler


@bp.route("/submit/", methods=["POST"])
def submit():
    current_index = int(request.form.get("index") or "1")
    print(request.form)
    if return_path := request.args.get("return"):
        parsed_url = urlparse(return_path)
        query_params = dict(parse_qsl(parsed_url.query))
        if "feedback_id" not in query_params:
            query_params["feedback_id"] = str(uuid.uuid4())
        new_query_params = qs_toggler(query_params, "feedback_index", current_index + 1)
        return_url = f"{parsed_url.path.rstrip('?')}?{new_query_params}#feedback"
        return redirect(return_url)
    return "Thank you for your feedback"
