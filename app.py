import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file if it exists
if os.path.exists('.env'):
    print("Loading environment variables from .env file")
    load_dotenv()
else:
    print("No .env file found, assuming environment variables are set in the system")

from_email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Function to send an email
def send_email(to_email, subject, body):
    print(f"Preparing to send email to {to_email}")
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        print("Connecting to email server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        print("Logged in to email server")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Function to check for replies
def check_for_replies(email_id):
    print(f"Checking for replies from {email_id}")
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(from_email, password)
    mail.select('inbox')

    result, data = mail.search(None, f'(FROM "{email_id}")')
    if data[0]:
        print(f"Reply found from {email_id}")
        return True
    print(f"No reply from {email_id} yet")
    return False

# Main function to start the email campaign
def start_campaign():
    global emails, follow_up_subjects, follow_up_bodies, follow_up_count
    print("Starting the email campaign")
    emails = input("Enter email addresses (separated by commas): ").split(',')
    subject = "Hello from Python!"
    body = "This is a test email."

    for email_id in emails:
        print(f"Sending initial email to {email_id.strip()}")
        send_email(email_id.strip(), subject, body)

    follow_up_subjects = [
        "Follow-up 1: Hello from Python!",
        "Follow-up 2: Just checking in!",
        "Follow-up 3: Final Reminder: Hello from Python!"
    ]

    follow_up_bodies = [
        "Just checking if you received my previous email.",
        "I hope this email finds you well. Following up on my previous message.",
        "This is the final reminder regarding my previous emails. Please get back to me."
    ]

    follow_up_count = {email_id.strip(): 0 for email_id in emails}

# Function to check and send follow-up emails
def check_and_follow_up():
    global emails, follow_up_subjects, follow_up_bodies, follow_up_count
    print("Executing scheduled task: check_and_follow_up")
    for email_id in emails:
        email_id = email_id.strip()
        print(f"Processing {email_id}")
        if follow_up_count[email_id] < 3:
            if check_for_replies(email_id):
                print(f"Received a reply from {email_id}")
                follow_up_count[email_id] = 3  # Stop further follow-ups
            else:
                if follow_up_count[email_id] > 0:
                    print(f"Sending follow-up email {follow_up_count[email_id]} to {email_id}")
                    send_email(email_id, follow_up_subjects[follow_up_count[email_id] - 1], follow_up_bodies[follow_up_count[email_id] - 1])
                follow_up_count[email_id] += 1
        else:
            print(f"No more follow-ups for {email_id}")

if __name__ == "__main__":
    start_campaign()
    check_and_follow_up()
