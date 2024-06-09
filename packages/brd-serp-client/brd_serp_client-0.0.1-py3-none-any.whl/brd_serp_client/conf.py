import os

from dasida import get_secrets

SM_BRD_FOOD360 = os.getenv("SM_BRD_FOOD360", "brd-food360-eugene")
if SM_BRD_FOOD360:
    secret = get_secrets(SM_BRD_FOOD360)
    USERNAME = secret.get("username")
    PASSWORD = secret.get("password")
else:
    USERNAME = None
    PASSWORD = None