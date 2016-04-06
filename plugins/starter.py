Skip to content
This repository
Search
Pull requests
Issues
Gist
 @imuttschall
 Unwatch 1
  Star 0
  Fork 82 imuttschall/starter-python-bot
forked from BeepBoopHQ/starter-python-bot
 Code  Pull requests 0  Wiki  Pulse  Graphs  Settings
Branch: master Find file Copy pathstarter-python-bot/plugins/starter.py
1444031  on Jan 20
@randompi randompi Implemented lemonbot attachment command, through api_call.
1 contributor
RawBlameHistory     63 lines (51 sloc)  2.42 KB
import time
import re
import random
import logging
crontable = []
outputs = []
attachments = []
typing_sleep = 0

greetings = ['Hi friend!', 'Hello there.', 'Howdy!', 'Wazzzup!!!', 'Hi!', 'Hey.']
help_text = "{}\n{}\n{}\n{}\n{}\n{}".format(
    "I will respond to the following messages: ",
    "`lemonbot hi` for a random greeting.",
    "`lemonbot joke` for a question, typing indicator, then answer style joke.",
    "`lemonbot attachment` to see a Slack attachment message.",
    "`@<your bot's name>` to demonstrate detecting a mention.",
    "`lemonbot help` to see this again.")

# regular expression patterns for string matching
p_bot_hi = re.compile("lemonbot[\s]*hi")
p_bot_joke = re.compile("lemonbot[\s]*joke")
p_bot_attach = re.compile("lemonbot[\s]*attachment")
p_bot_help = re.compile("lemonbot[\s]*help")

def process_message(data):
    logging.debug("process_message:data: {}".format(data))

    if p_bot_hi.match(data['text']):
        outputs.append([data['channel'], "{}".format(random.choice(greetings))])

    elif p_bot_joke.match(data['text']):
        outputs.append([data['channel'], "Why did the python cross the road?"])
        outputs.append([data['channel'], "__typing__", 5])
        outputs.append([data['channel'], "To eat the chicken on the other side! :laughing:"])

    elif p_bot_attach.match(data['text']):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachments.append([data['channel'], txt, build_demo_attachment(txt)])

    elif p_bot_help.match(data['text']):
        outputs.append([data['channel'], "{}".format(help_text)])

    elif data['text'].startswith("lemonbot"):
        outputs.append([data['channel'], "I'm sorry, I don't know how to: `{}`".format(data['text'])])

    elif data['channel'].startswith("D"):  # direct message channel to the bot
        outputs.append([data['channel'], "Hello, I'm the BeepBoop python starter bot.\n{}".format(help_text)])

def process_mention(data):
    logging.debug("process_mention:data: {}".format(data))
    outputs.append([data['channel'], "You really do care about me. :heart:"])

def build_demo_attachment(txt):
    return {
        "pretext" : "We bring bots to life. :sunglasses: :thumbsup:",
		"title" : "Host, deploy and share your bot in seconds.",
		"title_link" : "https://beepboophq.com/",
		"text" : txt,
		"fallback" : txt,
		"image_url" : "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
		"color" : "#7CD197",
    }
Status API Training Shop Blog About
© 2016 GitHub, Inc. Terms Privacy Security Contact Help
