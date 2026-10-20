from sequential_list import SequentialList


def main():
    catalog = SequentialList()

    catalog.insert({
        "id": 1,
        "name": "Mouse",
        "price": 59.90
    })

    catalog.insert({
        "id": 2,
        "name": "Teclado",
        "price": 129.90
    })

    catalog.insert({
        "id": 3,
        "name": "Monitor",
        "price": 899.90
    })

    print("Quantidade:", len(catalog))

    print("Busca existente:", catalog.search(2))
    print("Busca inexistente:", catalog.search(99))

    print("Remoção:", catalog.remove(2))
    print("Busca após remoção:", catalog.search(2))
    print("Quantidade final:", len(catalog))


if __name__ == "__main__":
    main()
