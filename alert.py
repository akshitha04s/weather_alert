
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
par = {
    "appid": "7c12fd8f6610ceb39b051f2ae84743ff",
    "lat": 17.385044,
    "lon": 78.486671,
    "cnt": 4,
}
endpoint = "https://api.openweathermap.org/data/2.5/forecast"

# 2. Email Configuration
SENDER_EMAIL = "surakantiakshithareddy04@gmail.com"
RECEIVER_EMAIL = "surakantiakshithareddy04@gmail.com"  # Sending to yourself
# Use the 16-character Google App Password here (no spaces)
APP_PASSWORD = "qtvq swxj xvnb adyo"  

# 3. Fetch Weather Data

try:
    response = requests.get(endpoint, params=par, timeout=15)
    response.raise_for_status()
    weatherdata = response.json()

except requests.exceptions.Timeout:
    print("Weather API connection timed out. Please try again.")

except requests.exceptions.ConnectionError:
    print("Check your internet connection.")

except requests.exceptions.RequestException as e:
    print("Error:", e)
weatherdata = response.json()

# Flag to check if we need to send an email
trigger_email = False
trigger_code = None

# Loop through the 4 forecast intervals
for hourdata in weatherdata["list"]:
    condcode = hourdata["weather"][0]["id"]
    if condcode < 850:
        trigger_email = True
        trigger_code = condcode
        break  # Exit loop early since we found a matching condition

# 4. Send Email if condition is met
if trigger_email:
    print(f"Condition code {trigger_code} is less than 850! Sending email...")
    
    # Create the email structure
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "⚠️ Weather Alert: Action Required!"
    
    body = f"Hello,\n\nYour weather script detected a condition code of {trigger_code}, which is below 850.\n\nPlease check the weather forecast."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Connect to Gmail's secure SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()  # Encrypt the connection
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
        
    except Exception as e:
        print(f"Failed to send email. Error: {e}")