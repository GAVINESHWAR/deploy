from fastapi import FastAPI, Form
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
sender_email = os.getenv("EMAIL_ID")
passkey = os.getenv("PASSKEY")

@app.get("/")
def read_root():
    return {"message": "🚀 FastAPI is successfully running on Render!"}

@app.get("/hello/{name}")
def read_item(name: str):
    return {"message": f"Hello, {name}! Welcome to FastAPI on Render."}


@app.post("/send-mail/")
async def send_mail(
    Name: str = Form(...),
    Email: str = Form(...),
    MobileNumber: str = Form(...),
    PickupLocation: str = Form(...),
    DropLocation: str = Form(...),
    AmbulanceType: str = Form(...),
    EstimatedCost: str = Form(...),
    Timestamp: str = Form(...)
):
    try:
        # Create the email content
        subject = f"🚑 Ambulance Booking Confirmation for {Name}"
        body = f"""
        <h2>Ambulance Booking Details</h2>
        <p><b>Name:</b> {Name}</p>
        <p><b>Email:</b> {Email}</p>
        <p><b>Mobile Number:</b> {MobileNumber}</p>
        <p><b>Pickup Location:</b> {PickupLocation}</p>
        <p><b>Drop Location:</b> {DropLocation}</p>
        <p><b>Ambulance Type:</b> {AmbulanceType}</p>
        <p><b>Estimated Cost:</b> {EstimatedCost}</p>
        <p><b>Timestamp:</b> {Timestamp}</p>
        """

        # Setup MIME
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = Email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, "html"))

        # Send email using SMTP (Gmail)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, passkey)
            server.send_message(msg)

        return {"status": "success", "message": "Email sent successfully"}

    except Exception as e:
        return {"status": "error", "message": str(e)}