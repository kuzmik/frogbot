import time
from slackclient import SlackClient
from RIBBIT.client import RIBBITClient

class FrogBot():
    def __init__(self, bot_id, oauth_token):
        # FIRE UP A FROG WORMHOLE
        self.frog = RIBBITClient()

        # The actual slack client
        self.slack = SlackClient(oauth_token)

        # This is what the bot listens for in order to know that it is being addressed.
        self.ACHTUNG = "<@{}>".format(bot_id)        
        if self.slack.rtm_connect():
            # the real time messages is a nightmare firehose of JSON messages.
            while True:
                text, channel = self.decode_slack(self.slack.rtm_read())
                if text and channel:
                    self.command_received(text, channel)
                time.sleep(1)
        else:
            print("Connection failed. Please see your Frog customer support rep for help.")    

    def command_received(self, text, channel):
        if text == "tip":
            response = self.frog.frog_tip()
        elif text == ":frog:":
            response = "That's racist. #notallfrogs look the same."
        else:
            response = "I'm not sure what I'm supposed to do with that. Sorry."    
        self.slack.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    # slack sends back a mess of json. we only want to deal with messages
    def decode_slack(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and self.ACHTUNG in output['text']:
                    return output['text'].split(self.ACHTUNG)[1].strip().lower(), output['channel']
        return None, None
 

# Get these variables by following the directions at https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
# a lot of this code is from there
if __name__ == "__main__":
    frog = FrogBot('BOT USER ID', 'BOT OAUTH TOKEN. GET YOURS TODAY AT HTTP://SLACK.COM')