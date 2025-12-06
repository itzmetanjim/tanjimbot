import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request

# 1. Setup tokens
SLACK_BOT_TOKEN =os.environ.get("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET=os.environ.get("SLACK_SIGNING_SECRET")
print(SLACK_BOT_TOKEN,SLACK_SIGNING_SECRET)
# 2. Initialize Bolt
app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET
)

# 3. Handle a Mention
@app.event("app_mention")
def handle_mention(event, say):
    user = event["user"]
    say(f"Hello <@{user}>! I received your webhook via DuckDNS.")

# 4. Setup Flask to handle the incoming HTTP requests
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

# 5. Run the server
if __name__ == "__main__":
    # Ensure this port (3000) is forwarded in your router to this machine
    flask_app.run(host="0.0.0.0", port=4000)
