import datetime
import logging
import os.path
import shutil
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
logging.basicConfig(level=logging.getLevelName(LOG_LEVEL))
logger = logging.getLogger('joplin-backup')


class Backup:
    tmp_fp: str = '/tmp/jolpin_db.sqlite'  # Make sure process user has access to this directory
    original_fp: str = None  # <User directory>/.config/joplin-desktop/database.sqlite'
    email: str = None
    password: str = None
    port: int = 465  # For SSL

    def __init__(self, email: str, password: str, database_fp: str):
        assert email is not None
        assert password is not None
        assert database_fp is not None
        self.sender_email = email
        self.password = password
        self.original_fp = database_fp

    def do_backup(self):
        logger.info('Doing backup...')
        logger.info('Copying database file...')
        self._copy_file_to_tmp()
        logger.info('Finished to copy database file.')
        logger.info('Sending email...')
        self._send_file_via_email()
        logger.info('Finished sending email.')
        logger.info('Backup done!')

    def _copy_file_to_tmp(self):
        assert os.path.isfile(self.original_fp)
        shutil.copyfile(self.original_fp, self.tmp_fp)

    def _send_file_via_email(self):
        # Create a secure SSL context
        context = ssl.create_default_context()

        email_message = self._create_email_msg()

        with smtplib.SMTP_SSL("smtp.gmail.com", self.port, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, self.sender_email, msg=email_message)

    def _create_email_msg(self) -> str:
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = self.sender_email
        message["Subject"] = f'[{datetime.date.today()}] Joplin backup'

        body = "This is an email with attachment sent from Python"
        # Add body to email
        message.attach(MIMEText(body, "plain"))

        part = self._generate_attachment()
        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        return text

    def _generate_attachment(self) -> MIMEBase:
        # Open PDF file in binary mode
        with open(self.tmp_fp, "rb") as attachment_file:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment_file.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(self.tmp_fp)}",
            )
            return part


if __name__ == '__main__':
    email = os.environ.get('EMAIL')
    password = os.environ.get('PASSWORD')  # App password for Google
    database_fp = os.environ.get('DATABASE_FP')  # App password for Google
    Backup(
        database_fp=database_fp,
        email=email,
        password=password
    ).do_backup()
