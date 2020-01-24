import os
from dotenv import load_dotenv

# read .env file to get Hue Key
load_dotenv()


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    HUEKEY = os.getenv("HUEKEY")
    HUEIP = os.getenv("HUEIP")

