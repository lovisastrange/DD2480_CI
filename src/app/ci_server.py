from flask import Flask, jsonify
from webhook_handler import Webhook_handler
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint to handle incoming webhooks.
    """
    handler = Webhook_handler(os.environ.get('WEBHOOK_SECRET'))
    handler.verify()
    data = handler.parse_data()
    #
    # Call other functions that use the data here, I think... :)
    #
    return jsonify({'status': 'success', 'message': 'Webhook processed'}), 200


@app.errorhandler(500)
def handle_500(error):
    """
    Handle internal server errors.
    """
    return jsonify({'status': 'error', 'message': str(error)}), 500

def start_server():
    """
    Start the CI server.
    """
    app.run(port=8080, debug=True)

if __name__ == '__main__':
    start_server()