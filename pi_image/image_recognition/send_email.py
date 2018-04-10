#############################################################################
# send_email.py
#
# By: Joey-Michael Fallone
#
# Sends email with the visibility image if below the threshold
# based on this tutorial: http://naelshiab.com/tutorial-send-email-python/
#
#############################################################################
import camera
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

fromaddr = "sensorhubalpha@gmail.com"
with open("/home/thor/.email.dat") as email_file:
	toaddr = email_file.readline().strip("\n")

msg = MIMEMultipart()

msg['From']    = fromaddr
msg['To']      = toaddr
msg['Subject'] = "sensor hub - LOW VISIBILITY"

body = "Hi, we noticed a visbility rating of less than 60%..." + \
		"here's a photo, please take a look."

msg.attach(MIMEText(body, 'plain'))

camera = Camera()
filename = "lastest_image.jpg"
attachment = open(camera.get_latest_photo_filename(), "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename=%s" % filename)

msg.attach(part)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "s3ns0r12")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
