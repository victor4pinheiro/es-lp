from flask import Response, make_response


def format_messages(messages=None, status=200) -> Response:
    return make_response({"message": messages}, status)
