import os

from dotenv import load_dotenv
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import Response
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from app.services.orchestrator import start_irrigation  # adjust if needed

load_dotenv()

router = APIRouter(prefix="/twilio", tags=["twilio"])

twilio_key = os.environ.get('TWILIO_KEY')
twilio_secret = os.environ.get('TWILIO_SECRET')
twilio_account = os.environ.get('TWILIO_ACC')
from_number = os.getenv("TWILIO_FROM_NUMBER")
to_number = os.getenv("ALERT_TO_NUMBER")

client = Client(twilio_key, twilio_secret, twilio_account)

def handle_incoming_reply(message_body, sender):
    text = message_body.strip().upper()

    if text == "YES":
        start_irrigation()
        return "Approval received. Starting irrigation."
    elif text == "NO":
        return "Okay, irrigation canceled."
    else:
        return 'Reply "YES" or "NO".'

@router.post("/sms")
async def receive_sms(Body: str = Form(...), From: str = Form(...)):
    reply_text = handle_incoming_reply(Body, From)

    twiml = MessagingResponse()
    twiml.message(reply_text)

    return Response(content=str(twiml), media_type="application/xml")