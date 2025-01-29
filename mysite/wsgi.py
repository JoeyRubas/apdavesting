import os
import sys

# Add the project directory to the system path
sys.path.append('/home/joey/apdavesting')

# Add the virtual environment’s site-packages
sys.path.append('/home/joey/apdavesting/venv/lib/python3.12/site-packages')

# Ensure the correct settings module is used
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
