import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime, timedelta
import subprocess

def get_previous_date():
    # Get the current date
    current_date = datetime.now()

    # Subtract one day to get the previous date
    previous_date = current_date - timedelta(days=1)

    # Convert to string in the format 'YYYY-MM-DD'
    previous_date_str = previous_date.strftime('%Y-%m-%d')

    return previous_date_str


def send_email_with_files(recipients, file_path):
    print("Sending email...")
    msg = MIMEMultipart()
    msg['From'] = 'awetzel@lionpowerusa.com'
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = 'Auto Reports for ' + get_previous_date()

    # Here is the email body
    body = "This email was sent automatically.\nPlease respond to it if you would like to be removed from the email list."
    msg.attach(MIMEText(body, 'plain'))

    # Get the directory of the fnames.txt file
    file_dir = os.path.dirname(file_path)
    
    # Read the file paths from the text file and attach each file
    with open(file_path, 'r') as f:
        for line in f:
            # Join the directory of fnames.txt with the file name
            file_to_attach = os.path.join(file_dir, line.strip())
            if os.path.isfile(file_to_attach):
                part = MIMEBase('application', "octet-stream")
                with open(file_to_attach, "rb") as file:
                    part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_to_attach))
                msg.attach(part)
                

    # Connect to the mail server
    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()

    # Login to your email account
    server.login('awetzel@lionpowerusa.com', '8R2vBi_7,ui^j;d')  # get password from environment variable

    # Send the email
    for recipient in recipients:
        del msg['To']
        msg['To'] = recipient
        server.send_message(msg)
    
    server.quit()


def generate_reports(executable_path):
    print("Generating reports...")
    # Get the current date
    current_date = datetime.now()

    # Subtract one day to get the previous date
    previous_date = current_date - timedelta(days=1)

    # Subtract another 16 days for the start date
    start_date = datetime(2023, 7, 7)

    # Prepare the command with arguments
    cmd = [
        executable_path,
        start_date.strftime('%Y'),
        start_date.strftime('%m'),
        start_date.strftime('%d'),
        previous_date.strftime('%Y'),
        previous_date.strftime('%m'),
        previous_date.strftime('%d'),
    ]

    # Run the executable
    subprocess.run(cmd, check=True, cwd=os.path.dirname(executable_path))

def main():
    generate_reports("/home/andrew/Desktop/internal/LpReportGenerator")
    recipients = ["jsleconich@lionpowerusa.com", "mwalker@lionpowerusa.com", "awetzel@lionpowerusa.com"] #
    send_email_with_files(recipients, '/home/andrew/Desktop/internal/fnames.txt')

# Test the function
if __name__ == '__main__':
    main()


