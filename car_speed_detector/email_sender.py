# Import smtplib for the actual sending function
import smtplib

# And imghdr to find the types of our images
import imghdr

# Import pandas for making the exel file
import pandas as pd

# Here are the email package modules we'll need
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email.mime.image
import os
from car_speed_logging import logger
from speed_validator import *

class EmailSender:
    # TODO make this as a CLI configurable param. 
    username = 'speeddetector101@gmail.com'
    password = 'LearnIOT06!'
    rcptlist = ['srinivassriram06@gmail.com', 'arjunsikka05@gmail.com', 'kr.reddy.kaushik@gmail.com', 'adityaanand.muz@gmail.com', 'ssriram.78@gmail.com', 'abhisar.muz@gmail.com', 'raja.muz@gmail.com']
    
    @classmethod
    def send_email(cls, temp_file, image_name):
        """
        1.defines the receivers as all the email address give above
        2.the msg sets the paremeter for the subject, from, and to in the email
        3.adds text with the picture of the speeding car
        4.makes sure that the email was sent
        """
        Dataframe = pd.Dataframe(speed_dataframe)
        Dataframe.to_excel("speedExcel.xls")
        
        logger().debug("Sending Email")
        receivers = ','.join(cls.rcptlist)

        msg = MIMEMultipart('mixed')
        msg['Subject'] = 'From GVW speed detector camera - Speeding car in GVW'
        msg['From'] = cls.username
        msg['To'] = receivers

        alternative = MIMEMultipart('alternative')
        textplain = MIMEText('Captured a picture of a speeding car.')
        alternative.attach(textplain)
        msg.attach(alternative)
        with open(temp_file.path, 'rb') as fp:
            #jpgpart = MIMEApplication(fp.read())
            jpgpart = email.mime.image.MIMEImage(fp.read())
            jpgpart.add_header('Content-Disposition', 'attachment', filename=image_name)
            msg.attach(jpgpart)
            
        fp = open('tmp/'+speedExcel 'rb')
        xls = MIMEBase('application','vnd.ms-excel')
        xls.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(xls)
        xls.add_header('Excel file of Speeding cars', 'attachment', filename=speedExcel)
        msg.attach(xls)

        client = smtplib.SMTP('smtp.gmail.com', 587)
        client.starttls()
        #client = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        #client.ehlo()
        client.login(cls.username, cls.password)
        client.sendmail(cls.username, cls.rcptlist, msg.as_string())
        logger().debug("Email Sent")
        client.quit()
        os.remove(temp_file.path)
