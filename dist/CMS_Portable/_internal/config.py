import os

APP_NAME = "CMSApp"

# Determine the base directory for application data
if os.name == 'nt':  # Windows
    APP_DATA_DIR = os.path.join(os.environ['LOCALAPPDATA'], APP_NAME)
else:  # macOS and Linux
    APP_DATA_DIR = os.path.join(os.path.expanduser('~/'), "." + APP_NAME.lower())

# Ensure the application data directory exists
os.makedirs(APP_DATA_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(APP_DATA_DIR, "cms_database.db")
APP_TITLE = "Contract Management System"