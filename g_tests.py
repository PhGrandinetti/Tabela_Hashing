from structures.sequential_list import SequentialList
from structures.hash_chaining import HashChaining
from structures.hash_open_addressing import HashOpenAddressing


def create_products():
    """Cria produtos de teste com IDs que provocam colisões."""
    return [
        {"id": 10, "name": "Teclado", "price": 120.00},
        {"id": 17, "name": "Mouse", "price": 60.00},
        {"id": 24, "name": "Monitor", "price": 850.00},
        {"id": 5, "name": "Headset", "price": 150.00},
    ]


def test_structure(name, structure):
    products = create_products()

    print(f"\n{'=' * 45}")
    print(f"Testando: {name}")
    print("=" * 45)

    # 1. Inserção
    for product in products:
        structure.insert(product)

    print(f"Produtos inseridos: {len(structure)}")
    assert len(structure) == len(products)
    print("Inserção: OK")

    # 2. Busca de produtos existentes
    for product in products:
        found = structure.search(product["id"])
        assert found is not None
        assert found["name"] == product["name"]

    print("Busca de produtos existentes: OK")

    # 3. Busca de produto inexistente
    assert structure.search(999) is None
    print("Busca de produto inexistente: OK")

    # 4. Remoção
    removed = structure.remove(17)
    assert removed is not None
    assert removed["name"] == "Mouse"
    assert len(structure) == len(products) - 1
    print("Remoção de produto existente: OK")

    # 5. Busca depois da remoção
    assert structure.search(17) is None

    # Os outros produtos devem continuar acessíveis.
    for product_id in [10, 24, 5]:
        assert structure.search(product_id) is not None

    print("Busca após remoção: OK")

    # 6. Remoção de produto inexistente
    assert structure.remove(999) is None
    print("Remoção de produto inexistente: OK")

    print(f"Total final de produtos: {len(structure)}")
    print("Todos os testes passaram!")


def main():
    # Capacidade 7: os IDs 10, 17 e 24 colidem,
    # pois todos deixam resto 3 na divisão por 7.
    structures = [
        ("Lista sequencial", SequentialList()),
        ("Hash com encadeamento", HashChaining(capacity=7)),
        (
            "Hash com endereçamento aberto",
            HashOpenAddressing(capacity=7),
        ),
    ]

    for name, structure in structures:
        test_structure(name, structure)

    print("\nTodos os testes das três estruturas foram concluídos.")


if __name__ == "__main__":
    main()
