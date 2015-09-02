from flask import Flask, request
from models import Slack


app = Flask(__name__)


@app.route("/")
def index():
    if not request.args:
        message = """
        Welcome to SlackTeX!
        Check me out on <a href="https://github.com/nicolewhite/slacktex">GitHub</a>.
        """

        return message

    slack = Slack()

    token = request.args["token"]
    latex = request.args["text"]
    channel_id = request.args["channel_id"]
    user_id = request.args["user_id"]

    if token != slack.SLASH_COMMAND_TOKEN:
        return "Unauthorized."

    url = "http://chart.apis.google.com/chart?cht=tx&chl={latex}".format(latex=latex)

    payload = {"text": url, "channel": channel_id}
    user = slack.find_user_info(user_id)
    payload.update(user)

    slack.post_latex_to_webhook(payload)

    return "Success!", 200