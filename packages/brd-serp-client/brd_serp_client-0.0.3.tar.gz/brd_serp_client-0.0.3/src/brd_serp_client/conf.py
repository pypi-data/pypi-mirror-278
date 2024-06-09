import os

from dasida import get_secrets

SM_BRD_FOOD360 = os.getenv("SM_BRD_FOOD360", "brd-food360-eugene")
SM_BRD_FOOD360_TOKEN = os.getenv("SM_BRD_FOOD360", "brd-food360-usertoken")

# user account to access Bright Data Food360 Zone
secret = get_secrets(SM_BRD_FOOD360)
secret = secret if secret else {}
USERNAME = secret.get("username")
PASSWORD = secret.get("password")

# user token to access Bright Data
secret = get_secrets(SM_BRD_FOOD360_TOKEN)
secret = secret if secret else {}
API_TOKEN = secret.get("token")
