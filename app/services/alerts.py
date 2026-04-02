# Sends SMS alerts to TC via Twilio API

# - Create a free Twilio account and get a phone number.
# - Put Twilio credentials in your .env file.
# - Build alerts.py with a send_alert() function.
# - Test by sending yourself an SMS from a simple Python script.
# - Write formatting functions for different alert types
#   (irrigation started, sensor offline, system error).

import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

twilio_key = os.environ.get('TWILIO_KEY')
twilio_secret = os.environ.get('TWILIO_SECRET')
twilio_account = os.environ.get('TWILIO_ACC')
client = Client(twilio_key, twilio_secret, twilio_account)

def send_alert(message,type, moisture_val, et):
    if type == "permission":
        message = client.messages.create(
            body= "Do you want to water Willow Run Acres? Reply \"YES\" or \"NO\"",
            from_="+18445023045",
            to="+18505599011",
        )
    elif type == "startIrrigation":
        message = client.messages.create(
            body= "Valve opened, soil at 24%, ETA 4.2 mm/day':" + message,
            from_="+18445023045",
            to="+18505599011",
        )
    elif type == "offlineSensor":
        message = client.messages.create(
            body= "The sensor went offline at " + message,
            from_="+18445023045",
            to="+18505599011",
        )
    elif type == "systemerror":
        message = client.messages.create(
            body= "There was a system error:" + message,
            from_="+18445023045",
            to="+18505599011",
        )
    return message.sid

# might need receive function from Tc for approval
