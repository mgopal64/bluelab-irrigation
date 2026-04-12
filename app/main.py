from fastapi import FastAPI
from app.routers.resend import router as twilio_router

app = FastAPI()
app.include_router(twilio_router)