
from hash_chaining import HashChaining


def main():
    catalog = HashChaining(capacity=5)

    catalog.insert({"id": 12, "name": "Mouse", "price": 59.90})
    catalog.insert({"id": 17, "name": "Teclado", "price": 129.90})
    catalog.insert({"id": 8, "name": "Monitor", "price": 899.90})

    print("Quantidade:", len(catalog))
    print("Busca ID 12:", catalog.search(12))
    print("Busca ID 17:", catalog.search(17))
    print("Busca ID 99:", catalog.search(99))

    print("Remoção ID 12:", catalog.remove(12))
    print("Busca ID 12 após remoção:", catalog.search(12))
    print("Busca ID 17 após remoção:", catalog.search(17))
    print("Quantidade final:", len(catalog))


if __name__ == "__main__":
    main()
