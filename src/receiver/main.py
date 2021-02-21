from flask import abort
import signature

ACTION = 'action'
ISSUE = 'issue'
PR = 'pull_request'
PR_TO_S = 'pull request'
NUMBER = 'number'

def getActionSubject(payload):
    """Extract webhook type and related number
    Args:
        payload: JSON string of request body
    Returns:
        webhook type, issue or PR number
    """
    if ISSUE in payload:
        action_type = ISSUE
        number = payload[ISSUE][NUMBER]
    elif PR in payload:
        action_type = PR_TO_S
        number = payload[PR][NUMBER]
    else:
        action_type = ''
        number = 0
    return action_type, number

def receive(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if not signature.verify(request):
        return abort(403)

    payload = request.get_json()

    action = payload[ACTION]
    action_type, number = getActionSubject(payload)

    if action and action_type and number:
        return f'Thanks for the webhook for "{action}" on {action_type} {number}!'
    elif action:
        return f'Thanks for the "{action}" webhook'
    else:
        return abort(404)
