import os
import re
import logging
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_bolt import App, Say

from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

logging.basicConfig(level=os.environ["LOG_LEVEL"])

def no_bot_messages(message) -> bool:
    return message.get("bot_id") is None if message else True

def no_message_changed(event) -> bool:
    return event.get("subtype") != "message_changed" and event.get("edited") is None

#########################################
# Event Handlers
#########################################

slack_app = App()

event = {"type": re.compile("(message)|(app_mention)"), "subtype": None}
matchers = [no_bot_messages, no_message_changed]

@slack_app.event(event=event, matchers=matchers)
def handle_app_mention(event, say: Say):
    channel = event.get("channel")
    text = event.get("text")
    thread_ts = event.get("thread_ts")
    try:
        # Check if message is already in a thread, if it is, reply to that thread, else reply to the message directly
        thread_to_reply = thread_ts if thread_ts else None

        say(
            channel=channel,
            thread_ts=thread_to_reply,
            text="Response logic is not implemented yet.",
            token=SLACK_BOT_TOKEN
        )
    except Exception as error:
        # Improve error handling
        print(error)
        return

@slack_app.event("message")
def handle_message_events(body, logger):
    logger.debug(body)

@slack_app.event("app_mention")
def handle_message_events(body, logger):
    logger.debug(body)

@slack_app.event("app_uninstalled")
def handle_app_uninstalled_events(body, logger):
    logger.debug(body)

if __name__ == "__main__":
    SocketModeHandler(app=slack_app, app_token=SLACK_APP_TOKEN).start()
