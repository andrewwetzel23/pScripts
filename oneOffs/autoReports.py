import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd

def send_email_with_excel(recipient, file_path):
    msg = MIMEMultipart()
    msg['From'] = 'awetzel@lionpowerusa.com'
    msg['To'] = recipient
    msg['Subject'] = 'The subject of your mail'

    # Load the Excel file
    df = pd.read_excel(file_path)
    
    # Save dataframe to .csv for mailing
    df.to_csv('temp.csv', index=False)
    
    # Attach the file
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("temp.csv", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='data.csv')  # or .xlsx if you want
    msg.attach(part)
    
    # Connect to the mail server
    server = smtplib.SMTP('smtp.office365.com', 587)  # changed to Microsoft's server
    server.starttls()

    # Login to your email account
    server.login('awetzel@lionpowerusa.com', 'your_password')  # put your real password here

    # Send the email
    server.send_message(msg)
    server.quit()

# Test the function
send_email_with_excel('awetzel@lionpowerusa.com', 'file1.xlsx')
