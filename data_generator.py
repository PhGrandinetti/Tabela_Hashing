
import csv
import random
from pathlib import Path


DATA_DIR = Path("data")
SIZES = [10_000, 100_000, 300_000]


def generate_csv(quantity):
    DATA_DIR.mkdir(exist_ok=True)

    file_path = DATA_DIR / f"products_{quantity}.csv"
    rng = random.Random(42)

    ids = rng.sample(range(1, quantity * 10 + 1), quantity)

    with file_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["id", "name", "price"])

        for product_id in ids:
            name = f"Produto {product_id}"
            price = round(rng.uniform(1.0, 5000.0), 2)

            writer.writerow([product_id, name, price])

    print(f"Arquivo gerado: {file_path} ({quantity} produtos)")


def main():
    for size in SIZES:
        generate_csv(size)


if __name__ == "__main__":
    main()
