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