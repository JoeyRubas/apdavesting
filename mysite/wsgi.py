import os
import sys

# Get project and virtual environment paths from environment variables
PROJECT_PATH = os.getenv("DJANGO_PROJECT_PATH", os.path.dirname(os.path.abspath(__file__)))
VENV_PATH = os.getenv("DJANGO_VENV_PATH", os.path.join(PROJECT_PATH, "venv/lib/python3.12/site-packages"))

# Add project and virtual environment paths to sys.path
sys.path.append(PROJECT_PATH)
sys.path.append(VENV_PATH)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
