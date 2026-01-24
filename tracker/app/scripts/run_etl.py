import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from transactions.etl.pipeline import run_pipeline

User = get_user_model()
CSV_DIR = "/app/scripts/user_transactions"

for user in User.objects.all():
    csv_file = os.path.join(
        CSV_DIR, f"fake_transactions_{user.username}.csv"
    )

    if os.path.exists(csv_file):
        print(run_pipeline(csv_file, user))
    else:
        print(f"CSV not found for {user.username}")
