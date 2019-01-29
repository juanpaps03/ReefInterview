import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT_CONF = {
    "HUBSTAFF_APP_TOKEN": os.getenv("hubstaff_app_token"),
    "HUBSTAFF_AUTH_TOKEN": os.getenv("hubstaff_auth_token"),
    "HUBSTAFF_API_URL": os.getenv("hubstaff_api_url"),
    "HUBSTAFF_ORGANIZATION_ID": os.getenv("hubstaff_organization_id"),
}

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
FLASK_PORT = os.getenv("flask_port")