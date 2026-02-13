from faker import Faker
import os
import sys
import django

fake = Faker()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()

    from django.contrib.auth import get_user_model

    User = get_user_model()

    def generate_fake_users(num_users=5):
        users = []
        for _ in range(num_users):
            username = fake.user_name()
            email = fake.email()
            password = "password123"
            role = "user"

            user = User.objects.create_user(
                username=username, email=email, password=password, role=role
            )
            users.append(user)
        return users

    users = generate_fake_users(num_users=8)
    for user in users:
        print(f"Created user: {user.username}, email: {user.email}")
