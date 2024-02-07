from flask import Blueprint, jsonify, render_template
from main import create_app

bp = Blueprint('ci_server', __name__, url_prefix='/server')

@bp.route('/', methods=["GET"])
def home():
    return render_template('base.html')

@bp.route('/webhook', methods=['POST'])
def webhook():
    """
    Endpoint to handle incoming webhooks.
    """

    return jsonify({'status': 'success', 'message': 'process started'}), 200

@bp.errorhandler(500)
def handle_500(error):
    """
    Handle internal server errors.
    """
    return jsonify({'status': 'error', 'message': str(error)}), 500