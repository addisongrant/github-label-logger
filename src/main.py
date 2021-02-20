import os
import hmac

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
        return abort(500)

    request_json = request.get_json()
    action = request_json['action']
    number = request_json['number']
    message = create_message(action, number)

    if message != '':
        return 'Thanks for the webhook!'
    else:
        return abort(404)

def verify_signature(request):
    secret = os.getenv("SECRET_TOKEN")
    payload_body = request.get_json()
    h = 'sha256=' + hmac.new(secret, payload_body, 'sha256').hexdigest()
    return hmac.compare_digest(signature, request.env['HTTP_X_HUB_SIGNATURE_256'])

def create_message(action, number):
    message = ''
    if action:
        message = action
        if number:
            message = message + f' on {number}'
    return message

