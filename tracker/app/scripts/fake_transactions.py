from faker import Faker
import csv
import random

fake = Faker()

EXPENSE_CATEGORIES = [
    "Food",
    "Transportation",
    "Utilities",
    "Entertainment",
    "Healthcare",
    "Education",
    "Clothing",
    "Shopping",
    "Travel",
    "Miscellaneous",
]


def random_data():
    return fake.date_time_between(start_date="-1y", end_date="now")


def generate_transactions():
    is_expense = random.choice([True, False])

    if is_expense:
        amount = round(random.uniform(10, 500), 2) * -1
        category = random.choice(EXPENSE_CATEGORIES)
        description = fake.sentence(nb_words=6)
    else:
        amount = round(random.uniform(50, 1000), 2)
        category = ""
        description = random.choice(
            [
                "Salary payment",
                "Freelance project",
                "Gift received",
                "Sold old items",
                "Bonus from work",
            ]
        )

    return {
        "date": random_data().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "category": category,
        "description": description,
    }


def generate_csv(filename, rows=1000):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["date", "amount", "category", "description"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for _ in range(rows):
            writer.writerow(generate_transactions())

    print(f"Generated {rows} transactions in {filename}")


if __name__ == "__main__":
    generate_csv("fake_transactions.csv", rows=1000)
