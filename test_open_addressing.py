
from hash_open_addressing import HashOpenAddressing


def main():
    catalog = HashOpenAddressing(capacity=5)

    catalog.insert({"id": 12, "name": "Mouse", "price": 59.90})
    catalog.insert({"id": 17, "name": "Teclado", "price": 129.90})
    catalog.insert({"id": 22, "name": "Monitor", "price": 899.90})

    print("Quantidade:", len(catalog))
    print("Busca ID 12:", catalog.search(12))
    print("Busca ID 17:", catalog.search(17))
    print("Busca ID 22:", catalog.search(22))
    print("Busca ID 99:", catalog.search(99))

    print("Remoção ID 12:", catalog.remove(12))
    print("Busca ID 12 após remoção:", catalog.search(12))
    print("Busca ID 17 após remoção:", catalog.search(17))

    catalog.insert({"id": 27, "name": "Webcam", "price": 199.90})

    print("Busca ID 27:", catalog.search(27))
    print("Quantidade final:", len(catalog))


if __name__ == "__main__":
    main()
