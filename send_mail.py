import os
from dotenv import load_dotenv
from pathlib import Path
import smtplib
from email.mime.text import MIMEText

dotenv_path = Path("./config/.env")
load_dotenv(dotenv_path=dotenv_path)


def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = "smtp.mailtrap.io"
    username = os.getenv("USER")
    password = os.getenv("PASSWORD")
    message = f"<h3>New Feedback Submission</h3>\
        <ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = os.getenv("SENDER")
    receiver_email = os.getenv("RECEIVER")
    msg = MIMEText(message, "html")
    msg["Subject"] = "Tesla Feedback"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(username, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
