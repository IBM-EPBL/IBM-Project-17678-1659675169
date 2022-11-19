import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key=('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'))
from_email = Email("lmsprojectapplication@gmail.com")  # Change to your verified sender

def sendgridmail(TEXT, email):
    to_email = To(email)  # Change to your recipient
    subject = "ALERT FROM MONEYDEED$"
    content = Content("text/plain", TEXT)
    mail = Mail(from_email, to_email, subject, content)
    
    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()
    
    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
 