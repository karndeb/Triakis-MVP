import os
from os.path import join, dirname, abspath
from dotenv import load_dotenv

load_dotenv()


SMTP_SERVER_ADDRESS = os.getenv('SMTP_SERVER_ADDRESS')
PORT = os.getenv('PORT')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
SENDER_ADDRESS = os.getenv('SENDER_ADDRESS')
