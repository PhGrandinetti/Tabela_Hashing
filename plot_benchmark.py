
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# Caminhos dos arquivos
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "results" / "benchmark_results.csv"
OUTPUT_DIR = BASE_DIR / "results" / "graficos"

# Configuração dos gráficos
QUANTITIES = [10_000, 100_000, 300_000]

STRUCTURES = [
    "Lista sequencial",
    "Hash com encadeamento",
    "Hash com enderecamento aberto",
]

OPERATIONS = {
    "insercao": "Tempo de inserção",
    "busca_existente_por_consulta":
        "Tempo médio de busca de produto existente",
    "busca_inexistente_por_consulta":
        "Tempo médio de busca de produto inexistente",
    "remocao_amostra": "Tempo de remoção de 50 produtos",
    "tempo_total_experimento": "Tempo total do experimento",
}


def load_results():
    """Carrega as medições do CSV."""
    with CSV_PATH.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)
        results = []

        for row in reader:
            results.append({
                "operacao": row["operacao"],
                "quantidade": int(row["quantidade"]),
                "estrutura": row["estrutura"],
                "tempo_ms": float(row["tempo_ms"]),
            })

    return results


def plot_operation(results, operation, title):
    """Gera um gráfico de barras agrupadas para uma operação."""
    filtered = [
        row for row in results
        if row["operacao"] == operation
    ]

    if not filtered:
        print(f"Nenhum resultado encontrado para: {operation}")
        return

    # Posição de cada grupo no eixo X.
    x = np.arange(len(STRUCTURES))
    bar_width = 0.25

    fig, ax = plt.subplots(figsize=(11, 6))

    # Cada conjunto de dados terá uma barra em cada grupo.
    for i, quantity in enumerate(QUANTITIES):
        values = []

        for structure in STRUCTURES:
            matching = [
                row["tempo_ms"]
                for row in filtered
                if row["quantidade"] == quantity
                and row["estrutura"] == structure
            ]

            if not matching:
                raise ValueError(
                    f"Resultado ausente: operação={operation}, "
                    f"quantidade={quantity}, estrutura={structure}"
                )

            values.append(matching[0])

        positions = x + (i - 1) * bar_width

        bars = ax.bar(
            positions,
            values,
            bar_width,
            label=f"{quantity:,}".replace(",", ".")
                  + " produtos",
        )

        # Exibe o valor de cada barra.
        ax.bar_label(
            bars,
            fmt="%.4f",
            padding=3,
            fontsize=8,
            rotation=90,
        )

    ax.set_title(title)
    ax.set_xlabel("Estrutura de dados")
    ax.set_ylabel("Tempo (ms)")
    ax.set_yscale("log")

    ax.set_xticks(x)
    ax.set_xticklabels(
        [
            "Lista sequencial",
            "Hash com\nencadeamento",
            "Hash com\nendereçamento aberto",
        ]
    )

    ax.legend(title="Quantidade de produtos")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_axisbelow(True)

    # Dá espaço para os valores acima das barras.
    ax.margins(y=0.20)
    fig.tight_layout()

    # Salva cada gráfico em um arquivo PNG.
    filename = f"{operation}.png"
    output_path = OUTPUT_DIR / filename

    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Gráfico salvo em: {output_path}")

    plt.close(fig)


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Arquivo de resultados não encontrado: {CSV_PATH}"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = load_results()

    for operation, title in OPERATIONS.items():
        plot_operation(results, operation, title)

    print("\nTodos os gráficos foram gerados!")


if __name__ == "__main__":
    main()
