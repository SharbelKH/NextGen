import csv
prices = {}
with open("data/product.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        prices[row["product_id"]] = int(row["price"])
total = 0
with open("data/orders.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["product_id"] in ("a", "b", "c"):
            total += int(row["quantity_product"]) * prices[row["product_id"]]
print(total)