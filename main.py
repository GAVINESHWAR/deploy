from fastapi import FastAPI, Form
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
sender_email = os.getenv("SENDER_EMAIL")
passkey = os.getenv("PASSKEY")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify "http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        <html>
        <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f7f8fa; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 30px auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="background-color: #0056b3; padding: 20px; color: white; text-align: center;">
                    <h1 style="margin: 0; font-size: 24px;">AmbuCare Services</h1>
                    <p style="margin: 5px 0 0; font-size: 14px;">Emergency Response | Anytime, Anywhere</p>
                </div>
                
                <div style="padding: 25px;">
                    <h2 style="color: #333;">Booking Confirmation</h2>
                    <p style="font-size: 15px; color: #555;">
                        Dear <b>{Name}</b>,<br><br>
                        Thank you for choosing <b>Ambigo</b>. Your ambulance booking has been successfully received.
                    </p>

                    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Name:</b></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{Name}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Email:</b></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{Email}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Mobile Number:</b></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{MobileNumber}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Pickup Location:</b></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{PickupLocation}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Drop Location:</b></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{DropLocation}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Ambulance Type:</b></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">{AmbulanceType}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;"><b>Estimated Cost:</b></td>
                            <td style="padding: 8px; border-bottom: 1px solid #ddd;">₹{EstimatedCost}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px;"><b>Booking Time:</b></td>
                            <td style="padding: 8px;">{Timestamp}</td>
                        </tr>
                    </table>

                    <p style="margin-top: 25px; color: #444;">
                        Our team will contact you shortly to confirm the details.  
                        For urgent assistance, please call our 24/7 helpline: <b>+91-8985138102-AMBULANCE</b>
                    </p>
                </div>

                <div style="background-color: #0056b3; color: #fff; text-align: center; padding: 15px; font-size: 13px;">
                    © 2025 Ambigo Services | Safe • Reliable • Fast
                </div>
            </div>
        </body>
        </html>
        """

        # Setup MIME
        msg = MIMEMultipart("alternative")
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