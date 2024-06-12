import os
import datetime
import json
import textwrap
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging

logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


def get_json(path: str):
    # 치과의 json 파일을 불러온다.
    with open(os.path.join(path), 'r', encoding='UTF8') as f:
        json_data = json.load(f)
    logger.info(json_data)
    return json_data


def mail_to(title: str, text: str, mail_addr='hj3415@hanmail.net') -> bool:
    # 메일을 보내는 함수
    login_id_pass = ('hj3415@gmail.com', 'orlhfaqihcdytvsw')
    # 로그인 인자의 두번째 앱비밀번호는 구글계정 관리에서 설정함.
    smtp = ('smtp.gmail.com', 587)

    msg = MIMEMultipart()
    msg['From'] = login_id_pass[0]
    msg['Subject'] = title
    msg['To'] = mail_addr
    msg.attach(MIMEText(datetime.datetime.today().strftime('%I:%M%p') + '\n' + textwrap.dedent(text)))

    smtp = smtplib.SMTP(smtp[0], smtp[1])
    smtp.ehlo()
    try:
        smtp.starttls()
        smtp.login(login_id_pass[0], login_id_pass[1])
        smtp.sendmail(login_id_pass[0], mail_addr, msg.as_string())
        print(f'Sent mail to {mail_addr} successfully.')
        return True
    except:
        print(f'Unknown error occurred during sending mail to {mail_addr}.')
        return False
    finally:
        smtp.close()

