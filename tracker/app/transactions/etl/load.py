from transactions.models import Transaction, Category
from django.db import transaction as db_transaction
from django.utils.dateparse import parse_datetime

def load_transactions(df, user):
    transactions_to_create = []

    for _, row in df.iterrows():
        category_obj = None

        if row["transaction_type"] == "EXPENSE":
            category_name = row["category"]

            if not category_name or str(category_name).strip() == "":
                category_name = "Miscellaneous"

            category_obj, _ = Category.objects.get_or_create(
                name=category_name,
                user=user
            )

        t = Transaction(
            user=user,
            transaction_type=row["transaction_type"],
            amount=row["amount"],
            category=category_obj,
            description=row["description"],
            date=row["date"],
        )

        transactions_to_create.append(t)

    with db_transaction.atomic():
        Transaction.objects.bulk_create(transactions_to_create)

    return len(transactions_to_create)
