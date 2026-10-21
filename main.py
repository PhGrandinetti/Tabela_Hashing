
import csv
import random
import statistics
import time
from pathlib import Path

from structures.sequential_list import SequentialList
from structures.hash_chaining import HashChaining
from structures.hash_open_addressing import HashOpenAddressing


# Configurações do experimento
DATA_DIR = Path("data")
RESULTS_DIR = Path("results")

SIZES = [10_000, 100_000, 300_000]
QUERY_COUNT = 50
REPEATS = 3

# Ordem em que as operações aparecerão no CSV
OPERATION_ORDER = [
    "insercao",
    "busca_existente_por_consulta",
    "busca_inexistente_por_consulta",
    "remocao_amostra",
    "tempo_total_experimento",
]

# Nomes mais amigáveis para o relatório TXT
OPERATION_LABELS = {
    "insercao": "Inserção de todos os produtos",
    "busca_existente_por_consulta":
        "Busca de produto existente (por consulta)",
    "busca_inexistente_por_consulta":
        "Busca de produto inexistente (por consulta)",
    "remocao_amostra": f"Remoção de {QUERY_COUNT} produtos",
    "tempo_total_experimento": "Tempo total do experimento",
}


def load_products(file_path):
    """Carrega os produtos do arquivo CSV."""
    products = []

    with file_path.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            products.append({
                "id": int(row["id"]),
                "name": row["name"],
                "price": float(row["price"]),
            })

    return products


def insert_all(structure, products):
    """Insere todos os produtos em uma estrutura existente."""
    for product in products:
        structure.insert(product)

    return structure


def measure_median(operation, repeats=REPEATS):
    """Executa uma operação várias vezes e retorna a mediana em ms."""
    times = []

    for _ in range(repeats):
        start = time.perf_counter()
        operation()
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return statistics.median(times) * 1000


def benchmark_insertion(structure_factory, products):
    """Mede somente a inserção de todos os produtos."""
    times = []

    for _ in range(REPEATS):
        # A criação da estrutura fica fora da medição.
        structure = structure_factory()

        start = time.perf_counter()
        insert_all(structure, products)
        elapsed = time.perf_counter() - start

        times.append(elapsed)

    return statistics.median(times) * 1000


def benchmark_search(structure, queries):
    """Retorna o tempo mediano médio por consulta, em ms."""
    def operation():
        for product_id in queries:
            structure.search(product_id)

    total_ms = measure_median(operation)

    return total_ms / len(queries)


def benchmark_removal(
    structure_factory, products, ids_to_remove
):
    """Mede a remoção da amostra, sem contar a preparação."""
    times = []

    for _ in range(REPEATS):
        # Cria e preenche uma estrutura nova antes de cronometrar.
        structure = structure_factory()
        insert_all(structure, products)

        start = time.perf_counter()

        for product_id in ids_to_remove:
            structure.remove(product_id)

        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return statistics.median(times) * 1000


def benchmark_total(
    structure_factory,
    products,
    existing_ids,
    missing_ids,
    ids_to_remove,
):
    """
    Mede uma execução completa:
    inserção, buscas existentes, buscas inexistentes e remoção.
    """
    times = []

    for _ in range(REPEATS):
        # Cada repetição começa com uma estrutura vazia.
        structure = structure_factory()

        # O cronômetro começa imediatamente antes da primeira inserção.
        start = time.perf_counter()

        insert_all(structure, products)

        for product_id in existing_ids:
            structure.search(product_id)

        for product_id in missing_ids:
            structure.search(product_id)

        for product_id in ids_to_remove:
            structure.remove(product_id)

        # O cronômetro termina após a última remoção.
        elapsed = time.perf_counter() - start
        times.append(elapsed)

    return statistics.median(times) * 1000


def validate_structure(
    structure_factory,
    products,
    existing_ids,
    missing_ids,
    ids_to_remove,
):
    """Confere a corretude antes das medições de desempenho."""
    structure = structure_factory()
    insert_all(structure, products)

    assert all(
        structure.search(product_id) is not None
        for product_id in existing_ids
    ), "Falha ao buscar um ou mais produtos existentes."

    assert all(
        structure.search(product_id) is None
        for product_id in missing_ids
    ), "Uma busca por produto inexistente retornou resultado."

    for product_id in ids_to_remove:
        assert structure.remove(product_id) is not None, (
            f"Falha ao remover o produto {product_id}."
        )

        assert structure.search(product_id) is None, (
            f"O produto {product_id} continuou na estrutura."
        )


def save_results(measurements, structure_names):
    """Salva os resultados em CSV, agrupados por operação."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "benchmark_results.csv"

    rows = []

    # Primeiro, todas as linhas de uma operação; depois, a próxima.
    for operation_name in OPERATION_ORDER:
        for quantity in SIZES:
            for structure_name in structure_names:
                elapsed_ms = measurements[
                    (quantity, structure_name, operation_name)
                ]

                rows.append({
                    "operacao": operation_name,
                    "quantidade": quantity,
                    "estrutura": structure_name,
                    "tempo_ms": round(elapsed_ms, 6),
                })

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "operacao",
                "quantidade",
                "estrutura",
                "tempo_ms",
            ],
        )

        writer.writeheader()
        writer.writerows(rows)

    print(f"\nResultados CSV salvos em: {output_path}")


def save_readable_results(measurements, structure_names):
    """Gera um relatório TXT organizado por tamanho e estrutura."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "benchmark_readable.txt"

    with output_path.open("w", encoding="utf-8") as file:
        for quantity in SIZES:
            formatted_quantity = f"{quantity:,}".replace(",", ".")

            file.write(
                f"\n===== {formatted_quantity} produtos =====\n"
            )

            for structure_name in structure_names:
                file.write(f"\n------ {structure_name} ------\n\n")

                for operation_name in OPERATION_ORDER:
                    elapsed_ms = measurements[
                        (quantity, structure_name, operation_name)
                    ]

                    formatted_time = f"{elapsed_ms:.6f}".replace(
                        ".", ","
                    )

                    label = OPERATION_LABELS[operation_name]

                    file.write(
                        f"{label}: {formatted_time} ms\n"
                    )

                file.write(
                    "\n----------------------------------------\n"
                )

            file.write(
                "\n====================================================\n"
            )

    print(f"Relatório TXT salvo em: {output_path}")


def main():
    measurements = {}

    for quantity in SIZES:
        file_path = DATA_DIR / f"products_{quantity}.csv"
        products = load_products(file_path)

        # Uma semente fixa permite reproduzir as mesmas consultas.
        rng = random.Random(42)

        existing_ids = [
            product["id"]
            for product in rng.sample(
                products, min(QUERY_COUNT, len(products))
            )
        ]

        # O gerador utiliza IDs entre 1 e quantity * 10.
        # Portanto, estes IDs não devem existir nos arquivos gerados.
        missing_ids = list(
            range(
                quantity * 10 + 1,
                quantity * 10 + QUERY_COUNT + 1,
            )
        )

        # Removeremos uma amostra de produtos que existem.
        ids_to_remove = existing_ids[:]

        capacity = quantity * 2 + 1

        structure_configs = [
            ("Lista sequencial", SequentialList),
            (
                "Hash com encadeamento",
                lambda: HashChaining(capacity),
            ),
            (
                "Hash com enderecamento aberto",
                lambda: HashOpenAddressing(capacity),
            ),
        ]

        print(f"\nTestando {quantity:,} produtos...")

        for structure_name, structure_factory in structure_configs:
            print(f"  {structure_name}...")

            # Confere se as operações funcionam corretamente.
            # Esta etapa não faz parte dos tempos medidos.
            validate_structure(
                structure_factory,
                products,
                existing_ids,
                missing_ids,
                ids_to_remove,
            )

            # 1. Inserção de todos os produtos.
            insertion_ms = benchmark_insertion(
                structure_factory, products
            )

            # Prepara uma estrutura para medir as buscas.
            search_structure = structure_factory()
            insert_all(search_structure, products)

            # 2. Busca de produtos existentes.
            existing_search_ms = benchmark_search(
                search_structure, existing_ids
            )

            # 3. Busca de produtos inexistentes.
            missing_search_ms = benchmark_search(
                search_structure, missing_ids
            )

            # 4. Remoção da amostra de produtos.
            removal_ms = benchmark_removal(
                structure_factory, products, ids_to_remove
            )

            # 5. Experimento completo, cronometrado separadamente.
            total_ms = benchmark_total(
                structure_factory,
                products,
                existing_ids,
                missing_ids,
                ids_to_remove,
            )

            measurements[
                (quantity, structure_name, "insercao")
            ] = insertion_ms

            measurements[
                (
                    quantity,
                    structure_name,
                    "busca_existente_por_consulta",
                )
            ] = existing_search_ms

            measurements[
                (
                    quantity,
                    structure_name,
                    "busca_inexistente_por_consulta",
                )
            ] = missing_search_ms

            measurements[
                (quantity, structure_name, "remocao_amostra")
            ] = removal_ms

            measurements[
                (
                    quantity,
                    structure_name,
                    "tempo_total_experimento",
                )
            ] = total_ms

            print("    Concluído.")

    structure_names = [
        "Lista sequencial",
        "Hash com encadeamento",
        "Hash com enderecamento aberto",
    ]

    save_results(measurements, structure_names)
    save_readable_results(measurements, structure_names)


if __name__ == "__main__":
    main()
