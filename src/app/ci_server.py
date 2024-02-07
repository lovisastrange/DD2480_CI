from flask import Flask, jsonify 
from app import create_app

application = create_app()

@application.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint to handle incoming webhooks.
    """

    return jsonify({'status': 'success', 'message': 'process started'}), 200

@application.errorhandler(500)
def handle_500(error):
    """
    Handle internal server errors.
    """
    return jsonify({'status': 'error', 'message': str(error)}), 500

def start_server():
    """
    Start the CI server.
    """
    application.run(port=8080, debug=True)

if __name__ == '__main__':
    start_server()