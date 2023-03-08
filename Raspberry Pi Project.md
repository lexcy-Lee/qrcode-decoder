# Raspberry Pi Project
## QRcode decoder
### Student Number 2739672

#### Introduction
This project is a QR code decoder, he has two modes of operation, which are to recognise attachments in emails, or to recognise captured images by taking pictures with the webcame, his trigger condition is to send keywords through the fragrant target email, the Raspberry Pi will recognise the keywords and execute the corresponding program, after recognition, the Raspberry Pi will send the result to the target email.

### Physical - Construction
The Raspberry Pi is a miniature single board computer that runs on Linux.
A SD card for storing the Raspberry Pi system and for use as additional storage space.
A USB camera for taking pictures.
A display for debugging and making it easier to use the Raspberry Pi.

### Virtual - The Code
The following libraries were used in this project: os, smtplib, pyzbar, PIL, mail.mime.text, email.parser, email.header, poplib, time.
os: Running Linux commands via python
smtplib: Receive mail via SMTP
pyzbar: Decode the qrcode
PIL: Open jpg images
mail.mime.text, email.parser, email.header: Read and decode the content of emails
poplib: Send mail via POP3
time: Set program cycle interval

### Instruction manual
Step 1: Connect the webcam to the Raspberry Pi via USB
Step 2: Run /home/pi/main.py on the Raspberry Pi
Step 3: Then send an email to "qrcodescan@163.com" via any email address with the keywords "scan by webcam" and "scan the annex" (note: the keywords must be entered in the subject line). If the keyword sent is "scan by webcam", the webcam will be pointed at the target qrcode, the webcam will take a picture and decode it and send the result to the target email address. If the keyword sent is 'scan the annex', add the image of the qrcode to the email attachment (note: please change the name of the image to 'image.jpg') and the Raspberry Pi will download the attachment when it receives the email and After receiving the email, Raspberry Pi will download the attachment and decode it and send the result to the target email address.

### Note
The program will automatically cycle every 5 seconds once started, if you wish to exit the program, please do so manually.

### Ideas For Version 2
In version2, I want the Raspberry Pi to take the URL sent from the email, convert it to qrcode and send the qrcode image to the target email address.

### Conclusion
This project can successfully decode the qrcode required by the client, but currently only supports qrcode with content as URLs and runs slowly.

### Code
```python
import os
import smtplib
from pyzbar.pyzbar import decode
from PIL import Image
from email.mime.text import MIMEText
from email.parser import Parser
from email.header import decode_header
import poplib
import time

def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec

second = sleep_time(0, 0, 5)

while True:
    try:
        email = 'qrcodescan@163.com'
        password = 'FFFFAXPRNJCGNIHN'
        pop3_server = 'pop.163.com'

        server = poplib.POP3(pop3_server)
        server.user(email)
        server.pass_(password)
        resp, mails, octets = server.list()
        index = len(mails)
        resp, lines, octets = server.retr(index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)

        def decode_str(s):
            value, charset = decode_header(s)[0]
            if charset:
                value = value.decode(charset)
            return value

        def print_info(msg, indent=0):
            if indent == 0:
                for header in ['From', 'To', 'Subject']:
                    value = msg.get(header, '')
                    if value:
                        if header == 'Subject':
                            value = decode_str(value)
            return value
        print()
        def save_att_file(save_path):
            for part in msg.walk():
                file_name = part.get_filename()
                attachment_files =[]
                if file_name:
                    file_name = decode_str(file_name).lower()
                    data = part.get_payload(decode = True)
                    att_file = open(os.path.join(save_path, file_name), 'wb')
                    attachment_files.append(file_name)
                    att_file.write(data)
                    att_file.close()

        save_att_file('/home/pi')
        print("email received, rasberry pi should", print_info(msg, indent=0))
        server.dele(index)

        if print_info(msg, indent=0) == 'scan by webcam':
            os.system('fswebcam -d /dev/video0 --no-banner -r 1980*620 -s 3 ~/image.jpg')
            img = '/home/pi/image.jpg'

            decocdeQR = decode(Image.open(img))
            val = decocdeQR[0].data.decode('ascii')

            mail_host = 'smtp.163.com'
            mail_user = 'qrcodescan'
            mail_pass = 'FFFFAXPRNJCGNIHN'
            sender = 'qrcodescan@163.com'
            receivers = ['lexcy_lee@icloud.com']
            message = MIMEText(val, 'plain', 'utf-8')
            message['Subject'] = 'QR code decoding result'
            message['From'] = sender
            message['To'] = receivers[0]
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(mail_host, 25)
                smtpObj.login(mail_user, mail_pass)
                smtpObj.sendmail(
                    sender, receivers, message.as_string())
                smtpObj.quit()
                print('success')
            except smtplib.SMTPException as e:
                print('error', e)

        elif print_info(msg, indent = 0) == 'scan the annex':
            img = '/home/pi/image.jpg'

            decocdeQR = decode(Image.open(img))
            val = decocdeQR[0].data.decode('ascii')

            mail_host = 'smtp.163.com'
            mail_user = 'qrcodescan'
            mail_pass = 'FFFFAXPRNJCGNIHN'
            sender = 'qrcodescan@163.com'
            receivers = ['lexcy_lee@icloud.com']
            message = MIMEText(val, 'plain', 'utf-8')
            message['Subject'] = 'QR code decoding result'
            message['From'] = sender
            message['To'] = receivers[0]
            try:
                smtpObj = smtplib.SMTP()
                smtpObj.connect(mail_host, 25)
                smtpObj.login(mail_user, mail_pass)
                smtpObj.sendmail(
                    sender, receivers, message.as_string())
                smtpObj.quit()
                print('success')
            except smtplib.SMTPException as e:
                print('error', e)
        time.sleep(second)
    except:
        time.sleep(second)
        print("no email")
```

### Video Presentation

<iframe height=498 width=510 src="https://www.youtube.com/watch?v=4Cn53-utECw">