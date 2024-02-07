from flask import request, abort
import hmac, hashlib

class Webhook_handler:
    def __init__(self, secret_key):
        self.__secret_key = secret_key
        self.test_flag = False

    def verify(self):
        signature_header = request.headers.get('X-Hub-Signature-256')
        if not signature_header:
            if not self.test_flag:
                abort(400, description='Missing Signature')
            else:
                raise ValueError('Missing Signature')
        
        signature = signature_header.split('sha256=')[-1]
        hash = hmac.new(key=self.__secret_key.encode(), msg=request.data, digestmod=hashlib.sha256)
        
        if not hmac.compare_digest(hash.hexdigest(), signature):
            if not self.test_flag:
                abort(400, description='Invalid Signature')
            else:
                raise ValueError('Invalid Signature')
        
    def parse_data(self):
        data = request.get_json()
        if not data:
            if not self.test_flag:
                abort(400, description='Missing Data')
            else:
                raise ValueError('Missing Data')
        
        return {
            "repo": data.get('repository', {}).get('name', 'unknown'),
            "commit": data.get('after', 'unknown'),
            "branch": data.get('ref', 'unknown').split('/')[-1]
        }
