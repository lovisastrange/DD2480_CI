from flask import Blueprint, jsonify, render_template, request, current_app
from .webhook_handler import Webhook_handler
from .db import query_builds, query_build
import os

bp = Blueprint('ci_server', __name__, url_prefix='/server')

@bp.route('/', methods=["GET"])
def home():
    """
    Front-end of the app.
    Displays the list of previous builds.
    """
    current_app.logger.info("Home page loaded")
    build_hist = query_builds()
    return render_template('base.html', build_hist=build_hist)

@bp.route('/<int:build_id>', methods=["GET"])
def specific_build(build_id):
    """
    Route accessing a specific build in
    the build history.
    """
    data = query_build(build_id)
    return render_template('specific_build.html', data=data)


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
    Endpoint to handle internal server errors.
    """
    return jsonify({'status': 'error', 'message': str(error)}), 500