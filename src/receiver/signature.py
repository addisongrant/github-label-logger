import os
import hmac

GH_SIG_HEADER_1 = 'HTTP_X_HUB_SIGNATURE_256'
GH_SIG_HEADER_2 = 'X-Hub-Signature-256'
SECRET_TOKEN_NAME = 'SECRET_TOKEN'
HASH_TYPE = 'sha256'
ENCODING = 'utf-8'

def verify(request):
    """Verify webhook request signature
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        Whether or not request has valid signature
    """
    secret = bytearray(os.environ.get(SECRET_TOKEN_NAME), ENCODING)
    payload_body = request.data

    signature = HASH_TYPE + '=' + hmac.new(secret, payload_body, HASH_TYPE).hexdigest()

    hhub = request.headers.get(GH_SIG_HEADER_1)
    xhub = request.headers.get(GH_SIG_HEADER_2)

    provided = hhub or xhub
    return hmac.compare_digest(signature, provided)

