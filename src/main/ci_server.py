from flask import Blueprint, jsonify, render_template, request, current_app
from .webhook_handler import Webhook_handler
import os

bp = Blueprint('ci_server', __name__, url_prefix='/server')

@bp.route('/', methods=["GET"])
def home():
    current_app.logger.info("Home page loaded")
    return render_template('base.html')

@bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint to handle incoming webhooks.
    """
    handler = Webhook_handler(os.environ.get('WEBHOOK_SECRET'))
    handler.verify(request.headers, request.data)
    data = handler.parse_data(request.get_json())
    #
    # Call other functions that use the data here, I think... :)
    #
    return jsonify(data), 200

@bp.errorhandler(500)
def handle_500(error):
    """
    Handle internal server errors.
    """
    return jsonify({'status': 'error', 'message': str(error)}), 500