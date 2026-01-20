import pandas as pd
import math
from django.contrib.auth import get_user_model
import os, sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

User = get_user_model()

input_csv = "fake_transactions.csv"  
df = pd.read_csv(input_csv)

users = list(User.objects.all())
num_users = len(users)


df = df.sample(frac=1).reset_index(drop=True)

rows_per_user = math.ceil(len(df) / num_users)

output_dir = "/app/scripts/user_transactions"
os.makedirs(output_dir, exist_ok=True)

for i, user in enumerate(users):
    start_idx = i * rows_per_user
    end_idx = start_idx + rows_per_user
    user_df = df.iloc[start_idx:end_idx]
    
   
    output_csv = os.path.join(output_dir, f"fake_transactions_{user.username}.csv")
    user_df.to_csv(output_csv, index=False)
    print(f" {len(user_df)} transactions assigned to {user.username} -> {output_csv}")
