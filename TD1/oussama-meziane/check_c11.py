import csv
from datetime import date

ref = date(2026, 12, 1)

def age(birth, on):
    return on.year - birth.year - ((on.month, on.day) < (birth.month, birth.day))

prices = {}
with open("data/product.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        prices[row["product_id"]] = int(row["price"])

age25 = set()
with open("data/customers.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if age(date.fromisoformat(row["birth_date"]), ref) == 25:
            age25.add(row["customer_id"])

total = 0
with open("data/orders.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["customer_id"] in age25:
            total += int(row["quantity_product"]) * prices[row["product_id"]]

print(len(age25), "clients de 25 ans")
print(total)