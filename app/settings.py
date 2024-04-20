from os import getenv
from dotenv import load_dotenv


load_dotenv()


URL_DATABASE= getenv("URL_DATABASE")
URL_LOCAL_DATABASE= getenv("URL_LOCAL_DATABASE")
PERMISSIONS= getenv("PERMISSIONS")
SECRET_KEY_JWT= getenv("SECRET_KEY_JWT")
DURATION_DAYS_TOKEN= getenv("DURATION_DAYS_TOKEN")