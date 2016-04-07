#!/usr/bin/env python

import sys
sys.dont_write_bytecode = True

import glob
import yaml
import json
import os
import sys
import time
import logging
import re
from argparse import ArgumentParser

from slackclient import SlackClient

HELPFUL = 0
SNARKY  = 1

def dbg(debug_string):
    if debug:
        logging.debug(debug_string)

class RtmBot(object):
    def __init__(self, token):
        self.last_ping = 0
        self.token = token
        self.bot_plugins = []
        self.slack_client = None
        self.bot_on = True
        self.mode = HELPFUL
    def connect(self):
        """Convenience method that creates Server instance"""
        self.slack_client = SlackClient(self.token)
        self.slack_client.rtm_connect()
        logging.info(u"Connected {} to {} team at https://{}.slack.com".format(
            self.slack_client.server.username,
            self.slack_client.server.login_data['team']['name'],
            self.slack_client.server.domain))
    def start(self):
        self.connect()
        self.load_plugins()
        while True:
            for reply in self.slack_client.rtm_read():
                self.input(reply)
            self.crons()
            self.output()
            self.autoping()
            time.sleep(.1)
    def autoping(self):
        #hardcode the interval to 60 seconds
        now = int(time.time())
        if now > self.last_ping + 60:
            self.slack_client.server.ping()
            self.last_ping = now
    def isBotMention(self, message):
        botUserName = self.slack_client.server.login_data['self']['id']
        if re.search("@{}".format(botUserName), message):
            return True
        else:
            return False
    def input(self, data):
        # Make sure we're not responding to ourselves
        if "user" in data and data['user'] != self.slack_client.server.login_data['self']['id']:
            
            # data is of proper form
            if "type" in data:
            
                # Not doing anything with this event yet
                if data[ "type" ] == "user_typing":
                    return
            
                function_name = "process_" + data["type"]
                dbg("got {}".format(function_name))
                dbg( "data {}".format( data ) )
                
                if "text" in data:
                
                    if self.mode == HELPFUL or self.mode == SNARKY:
                    
                        
                        if self.isBotMention( data[ 'text' ] ):
                            dbg( "mention")
                            function_name = "process_mention"
                            self.bot_on = True
                        
                        elif data[ 'text' ].startswith( "lemonbot" ):
                            dbg( "command")
                            function_name = "process_helpful"
                            
                            if( True in [ x in data[ "text" ] for x in [ " hush ", " shutup ", " shut up ", " quiet " ] ] ):
                                dbg( "helpful mode" )
                                self.mode = HELPFUL
                                function_name = "process_mode_helpful"
                                
                            elif( "snarky" in data[ "text" ] ):
                                dbg( "snarky mode" )
                                self.mode = SNARKY
                                function_name = "process_mode_snarky"
                                
                            
                        elif self.mode == SNARKY: 
                            dbg( "snarky")
                            function_name = "process_snarky" 
                                                
                    
                        for plugin in self.bot_plugins:
                            plugin.register_jobs()
                            plugin.do(function_name, data)
                            
    def output(self):
        for plugin in self.bot_plugins:
            limiter = False
            for output in plugin.do_output():
                channel = self.slack_client.server.channels.find(output[0])
                if channel != None and output[1] != None:
                    if limiter == True:
                        time.sleep(.1)
                        limiter = False
                    message = output[1].encode('ascii','ignore')
                    if message.startswith("__typing__"):
                        user_typing_json = { "type": "typing", "channel": channel.id}
                        logging.debug(user_typing_json)
                        self.slack_client.server.send_to_websocket(user_typing_json)
                        time.sleep(output[2])
                    else:
                        channel.send_message("{}".format(message))
                        limiter = True
            for attachment in plugin.do_attachment():
                channel = self.slack_client.server.channels.find(attachment[0])
                if channel != None and attachment[1] != None:
                    attachments = []
                    if attachment != None and attachment[2] != None:
                        attachments.append(attachment[2])
                    attachments_json = json.dumps(attachments)
                    resp = self.slack_client.api_call("chat.postMessage",
                        text="{}".format(attachment[1]),
                        channel="{}".format(channel.id),
                        as_user="true",
                        attachments=attachments_json,
                    )
                    logging.debug(resp)
    def crons(self):
        for plugin in self.bot_plugins:
            plugin.do_jobs()
    def load_plugins(self):
        for plugin in glob.glob(directory+'/plugins/*'):
            sys.path.insert(0, plugin)
            sys.path.insert(0, directory+'/plugins/')
        for plugin in glob.glob(directory+'/plugins/*.py') + glob.glob(directory+'/plugins/*/*.py'):
            logging.info(plugin)
            name = plugin.split('/')[-1][:-3]
#            try:
            self.bot_plugins.append(Plugin(name))
#            except:
#                print "error loading plugin %s" % name

class Plugin(object):
    def __init__(self, name, plugin_config={}):
        self.name = name
        self.jobs = []
        self.module = __import__(name)
        self.register_jobs()
        self.outputs = []
        if 'setup' in dir(self.module):
            self.module.setup()
    def register_jobs(self):
        if 'crontable' in dir(self.module):
            for interval, function in self.module.crontable:
                self.jobs.append(Job(interval, eval("self.module."+function)))
            logging.debug("crontable: {}".format(self.module.crontable))
            self.module.crontable = []
        else:
            self.module.crontable = []
    def do(self, function_name, data):
        if function_name in dir(self.module):
            #this makes the plugin fail with stack trace in debug mode
            if not debug:
                try:
                    eval("self.module."+function_name)(data)
                except:
                    dbg("problem in module {} {}".format(function_name, data))
            else:
                eval("self.module."+function_name)(data)
        if "catch_all" in dir(self.module):
            try:
                self.module.catch_all(data)
            except:
                dbg("problem in catch all")
    def do_jobs(self):
        for job in self.jobs:
            job.check()
    def do_output(self):
        output = []
        while True:
            if 'outputs' in dir(self.module):
                if len(self.module.outputs) > 0:
                    logging.debug("output from {}".format(self.module))
                    output.append(self.module.outputs.pop(0))
                else:
                    break
            else:
                self.module.outputs = []
        return output
    def do_attachment(self):
        attachment = []
        while True:
            if 'attachments' in dir(self.module):
                if len(self.module.attachments) > 0:
                    logging.debug("attachments from {}".format(self.module))
                    attachment.append(self.module.attachments.pop(0))
                else:
                    break
            else:
                self.module.attachments = []
        return attachment

class Job(object):
    def __init__(self, interval, function):
        self.function = function
        self.interval = interval
        self.lastrun = 0
    def __str__(self):
        return "{} {} {}".format(self.function, self.interval, self.lastrun)
    def __repr__(self):
        return self.__str__()
    def check(self):
        if self.lastrun + self.interval < time.time():
            if not debug:
                try:
                    self.function()
                except:
                    dbg("problem")
            else:
                self.function()
            self.lastrun = time.time()
            pass

class UnknownChannel(Exception):
    pass


def main_loop():

    logging.info(directory)
    try:
        bot.start()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        logging.exception('OOPS')


if __name__ == "__main__":

    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath("{}/{}".format(os.getcwd(),
                                directory
                                ))

    log_level = os.getenv("LOG_LEVEL", "DEBUG")
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=log_level)
    debug = False
    if log_level == "DEBUG":
        debug = True

    slack_token = os.getenv("SLACK_TOKEN", "")
    logging.info("token: {}".format(slack_token))
    if slack_token == "":
        logging.error("SLACK_TOKEN env var not set!")
        sys.exit(1)
    bot = RtmBot(slack_token)
    site_plugins = []
    files_currently_downloading = []
    job_hash = {}

    main_loop()
