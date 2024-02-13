from flask import Blueprint, jsonify, render_template, request, current_app
from .webhook_handler import Webhook_handler
from .db import query_builds, query_build
from .builder import Builder
from dotenv import load_dotenv
from .discord_bot import CI_notificator
import os
import threading

bp = Blueprint('ci_server', __name__, url_prefix='/server')
notificator = CI_notificator()
notificator_thread = threading.Thread(target=notificator.bot.run, args=(notificator.token,))
notificator_thread.start()

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
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    handler = Webhook_handler(os.getenv('WEBHOOK_SECRET'))
    handler.verify(request.headers, request.data)
    data = handler.parse_data(request.headers, request.get_json())
    ci_process(data, token)
    return jsonify(data), 200

def ci_process(data, token):
    builder = Builder(data)
    build = builder.build()
    builder.send_status(data, build, token)
    notificator.send_notification(f"Build {build['id']} finished with status {build['test_result']}")

@bp.errorhandler(500)
def handle_500(error):
    """
    Endpoint to handle internal server errors.
    """
    return jsonify({'status': 'error', 'message': str(error)}), 500