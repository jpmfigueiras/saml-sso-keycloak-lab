from fastapi import Request

def prepare_fastapi_request(request: Request, form_data=None):
    url = request.url
    return {
        "https": "on" if url.scheme == "https" else "off",
        "http_host": request.headers.get("host"),
        "server_port": url.port or (443 if url.scheme == "https" else 80),
        "script_name": request.url.path,
        "get_data": dict(request.query_params),
        "post_data": form_data or {}
    }