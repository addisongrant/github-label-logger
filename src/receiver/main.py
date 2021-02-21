import os
import hmac
from flask import abort

def receive(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if not verify_signature(request):
        return abort(403)

    payload = request.get_json()
    action = payload['action']
    if 'issue' in payload:
        action_type = 'issue'
        number = payload['issue']['number']
    elif 'pull_request' in payload:
        action_type = 'pull request'
        number = payload['pull_request']['number']
    else:
        number = 0

    if action and action_type and number:
        return f'Thanks for the webhook for "{action}" on {action_type} {number}!'
    elif action:
        return f'Thanks for the "{action}" webhook'
    else:
        return abort(404)

def verify_signature(request):
    secret = bytearray(os.environ.get("SECRET_TOKEN"), 'utf-8')
    payload_body = request.data
    signature = 'sha256=' + hmac.new(secret, payload_body, 'sha256').hexdigest()
    return hmac.compare_digest(signature, request.headers.get('HTTP_X_HUB_SIGNATURE'))

