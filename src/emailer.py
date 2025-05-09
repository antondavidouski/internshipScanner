import os
from pathlib import Path
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()   # Make .env keys available in os.environ

# Path to the recipient list file, relative to the project root
recipientFile = Path(__file__).parent.parent / "recipient_list.txt"

def getRecipients():
    """Read recipient email addresses from the text file."""
    if not recipientFile.exists():
        raise FileNotFoundError(f"Recipient list file not found: {recipientFile}")
    
    with open(recipientFile, 'r') as f:
        # Read each line and strip whitespace
        recipients = [line.strip() for line in f.readlines()]
    
    # Filter out empty lines
    recipients = [email for email in recipients if email]
    
    if not recipients:
        raise RuntimeError("No valid recipient emails found in recipient_list.txt")
    
    return recipients

def send_email(dateStr, maintext):
    subjectTemplate = "New opening date detected: {date}"
    bodyTemplate = (
    f"Hi,\n\nNew internship opening(s) detected:\n\n{maintext}\n\nPlease check the sheet for more details.\n\nBest regards,\nInternship Tracker Bot\nPlease do not reply to this email - this inbox is not monitored.\n\n"
)
    # Use getenv + check to avoid KeyError
    smtpUser = os.getenv("SMTP_USERNAME")
    smtpPass = os.getenv("SMTP_PASSWORD")
    smtpSrv = os.getenv("SMTP_SERVER")
    smtpPort = os.getenv("SMTP_PORT")

    for var, val in [("SMTP_USERNAME", smtpUser), ("SMTP_PASSWORD", smtpPass),
                     ("SMTP_SERVER", smtpSrv), ("SMTP_PORT", smtpPort)]:
        if not val:
            raise RuntimeError(f"{var} environment variable is not set")
    
    # Get recipients from text file
    recipients = getRecipients()
    
    # Connect to SMTP server once
    with smtplib.SMTP_SSL(smtpSrv, int(smtpPort)) as smtp:
        smtp.login(smtpUser, smtpPass)
        
        # Send individual email to each recipient
        for recipient in recipients:
            # Create a new message for each recipient
            msg = EmailMessage()
            msg["From"] = smtpUser
            msg["To"] = recipient  # Only one recipient per email
            msg["Subject"] = subjectTemplate.format(date=dateStr)
            msg.set_content(bodyTemplate.format(date=dateStr))
            
            # Send the message to this recipient
            smtp.send_message(msg)
            print(f"Email sent to: {recipient}")
