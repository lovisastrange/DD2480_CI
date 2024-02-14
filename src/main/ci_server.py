from flask import Blueprint, jsonify, render_template, request, current_app
from .webhook_handler import Webhook_handler
from .database import BuildHistory
from .builder import Builder
from .notification import send_notification_webhook
from dotenv import load_dotenv
import os

bp = Blueprint('ci_server', __name__, url_prefix='/server')

@bp.route('/', methods=["GET"])
def home():
    """
    Front-end of the app.
    Displays the list of previous builds.
    """
    current_app.logger.info("Home page loaded")
    data = BuildHistory.query.all()
    build_hist= []
    for build in data:
        build_hist.append({
            "id": build.id,
            "date": build.date,
            "branch": build.branch,
            "event": build.event,
            "status": build.status
        })
    return render_template('base.html', build_hist=build_hist)

@bp.route('/<int:build_id>', methods=["GET"])
def specific_build(build_id):
    """
    Route accessing a specific build in
    the build history.
    """
    data = BuildHistory.query.get(build_id)
    data_dict={
        "id": data.id,
        "date": data.date,
        "branch": data.branch,
        "event": data.event,
        "status": data.status
        }
    return render_template('specific_build.html', data=data_dict)


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
    send_notification_webhook(f"Build {build['id']} finished with status {build['test_result']}")

@bp.errorhandler(500)
def handle_500(error):
    """
    Endpoint to handle internal server errors.
    """
    return jsonify({'status': 'error', 'message': str(error)}), 500