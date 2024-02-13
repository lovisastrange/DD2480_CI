from flask import abort, current_app
import hmac, hashlib

class Webhook_handler:
    """
    A class to handle webhooks received on the server.
    It verifies the signature of the request and parses
    the relevant data.

    Attributes
    ----------
    secret_key: str
        the secret key used by GitHub when sending webhooks

    Methods
    -------
    verify(headers, data):
        checks the signature in the request headers 
        to verify if it is a valid webhook.
    parse_data(data):
        parses the necessary data to clone and
        build the code.
    """
    def __init__(self, secret_key):
        self.__secret_key = secret_key

    def verify(self, headers, data):
        """
        Checks the signature in the request headers 
        to verify if it is a valid webhook.

        Parameters
        ----------
        headers: Headers
            the request headers
        data: bytes
            the request payload
        """
        signature_header = headers.get('X-Hub-Signature-256')
        if not signature_header:
            if not current_app.config["TESTING"]:
                abort(400, description='Missing Signature')
            else:
                raise ValueError('Missing Signature')

        signature = signature_header.split('sha256=')[-1]
        hash = hmac.new(key=self.__secret_key.encode(), msg=data, digestmod=hashlib.sha256)

        if not hmac.compare_digest(hash.hexdigest(), signature):
            if not current_app.config["TESTING"]:
                abort(400, description='Invalid Signature')
            else:
                raise ValueError('Invalid Signature')

    def parse_data(self, data):
        """
        Parses the necessary data to clone and
        build the code.

        Parameters
        ----------
        data: bytes
            the request payload
        """
        if not data:
            if not current_app.config["TESTING"]:
                abort(400, description='Missing Data')
            else:
                raise ValueError('Missing Data')

        return {
            "repo": data.get('repository', {}).get('name', 'unknown'),
            "clone_url": data.get('repository', {}).get('clone_url', 'unknown'),
            "commit": data.get('after', 'unknown'),
            "branch": data.get('ref', 'unknown').split('/')[-1]
        }