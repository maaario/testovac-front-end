import os
import dotenv

dotenv.read_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testovac.settings.production")

application = get_wsgi_application()
