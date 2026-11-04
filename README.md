# Análise Comparativa de Estruturas de Dados: Tabelas Hash

## 1. Introdução

O armazenamento e a manipulação de grandes volumes de dados exigem estruturas capazes de realizar operações de maneira eficiente. Dependendo da estrutura utilizada, operações como inserção, busca e remoção podem apresentar custos diferentes, principalmente conforme aumenta a quantidade de elementos armazenados.

Este projeto tem como objetivo implementar e comparar três estruturas de dados em Python: uma lista sequencial, uma tabela hash com encadeamento separado e uma tabela hash com endereçamento aberto.

A comparação é realizada por meio de experimentos com diferentes quantidades de produtos, permitindo observar como cada estrutura se comporta durante as operações de inserção, busca e remoção.

## 2. O que é uma Tabela Hash?

Uma tabela hash é uma estrutura de dados que permite armazenar e localizar elementos a partir de uma chave. Para isso, utiliza uma função hash, responsável por transformar essa chave em um índice da tabela, indicando a posição inicial onde o elemento deve ser armazenado ou procurado.

Neste projeto, a chave utilizada é o ID de cada produto. A função hash implementada utiliza o método da divisão:

```python
indice = ID % capacidade
```

O resultado da operação determina o índice inicial do produto na tabela.

### 2.1. Colisões

Uma colisão acontece quando dois ou mais elementos diferentes produzem o mesmo índice ao aplicar a função hash. Como isso pode ocorrer durante a utilização da estrutura, é necessário adotar estratégias para armazenar esses elementos sem perder informações.

Neste projeto, foram implementadas duas estratégias de resolução de colisões:

- **Encadeamento separado:** armazena os elementos que colidem em uma mesma lista, associada ao índice calculado.
- **Endereçamento aberto:** procura outra posição disponível dentro da própria tabela, utilizando sondagem linear.

### 2.2. Capacidade da tabela

Durante os experimentos, a capacidade das tabelas hash é definida pela seguinte expressão:

```python
capacidade = 2 * quantidade_de_produtos + 1
```

Essa escolha mantém a tabela com mais posições do que elementos inseridos, reduzindo sua taxa de ocupação e favorecendo o desempenho das operações.

## 3. Estruturas de Dados Implementadas

### 3.1. Lista Sequencial

A lista sequencial utiliza a estrutura `list` nativa do Python para armazenar todos os produtos em sequência.

Cada produto é representado por um dicionário contendo seu ID, nome e preço.

As operações são implementadas da seguinte maneira:

- **Inserção:** utiliza o método `append()` para adicionar um produto ao final da lista.
- **Busca:** percorre os elementos sequencialmente até encontrar o ID procurado.
- **Remoção:** percorre a lista para localizar o produto e, em seguida, remove sua posição.

A busca e a remoção possuem complexidade \(O(n)\), pois podem exigir a verificação de todos os elementos. A inserção com `append()` possui custo amortizado \(O(1)\).

### 3.2. Tabela Hash com Encadeamento Separado

Nessa implementação, a tabela é organizada em uma lista principal de posições, chamadas de *buckets*. Cada posição contém uma lista que pode armazenar um ou mais produtos.

Quando dois produtos diferentes geram o mesmo índice pela função hash, ambos são armazenados na lista correspondente àquela posição.

As operações funcionam da seguinte maneira:

- **Inserção:** calcula o índice e adiciona o produto ao bucket correspondente.
- **Busca:** calcula o índice e percorre apenas os elementos daquele bucket.
- **Remoção:** localiza o produto dentro do bucket e remove sua entrada.

Essa estratégia permite tratar colisões sem substituir os elementos já armazenados. Seu desempenho médio depende da distribuição dos elementos e da quantidade de colisões.

### 3.3. Tabela Hash com Endereçamento Aberto

Diferentemente do encadeamento separado, essa implementação armazena todos os produtos diretamente na própria tabela, sem utilizar listas individuais para cada posição.

Quando ocorre uma colisão, é utilizada a **sondagem linear**, que verifica as posições seguintes até encontrar uma posição adequada.

O avanço entre as posições é realizado por:

```python
indice = (indice + 1) % capacidade
```

As operações funcionam da seguinte maneira:

- **Inserção:** calcula o índice inicial e procura uma posição disponível caso ocorra uma colisão.
- **Busca:** percorre a sequência de posições até encontrar o produto ou determinar que ele não existe.
- **Remoção:** substitui o elemento por um marcador especial chamado `DELETED`.

O marcador `DELETED` é necessário porque uma posição removida não pode ser tratada como uma posição que nunca foi ocupada. Isso preserva a sequência de sondagem e permite que as buscas continuem funcionando corretamente.

## 4. Metodologia dos Experimentos

Para comparar as três estruturas, foram utilizados conjuntos de dados com diferentes quantidades de produtos.

### 4.1. Conjuntos de Dados

| Arquivo | Quantidade de produtos |
|---|---:|
| `products_10000.csv` | 10.000 |
| `products_100000.csv` | 100.000 |
| `products_300000.csv` | 300.000 |

Cada produto possui três atributos:

- ID: identificador único do produto.
- Nome: identificação textual do produto.
- Preço: valor associado ao produto.

Os mesmos conjuntos de dados são utilizados nas três estruturas, permitindo uma comparação sob as mesmas condições.

### 4.2. Operações Avaliadas

Foram realizadas cinco medições para cada estrutura e tamanho de conjunto:

1. **Tempo de inserção:** tempo total necessário para inserir todos os produtos.
2. **Busca de produto existente:** tempo médio por consulta, utilizando uma amostra de 50 IDs presentes no conjunto.
3. **Busca de produto inexistente:** tempo médio por consulta, utilizando 50 IDs que não estão armazenados.
4. **Tempo de remoção:** tempo total necessário para remover uma amostra de 50 produtos existentes.
5. **Tempo total do experimento:** tempo necessário para executar, em sequência, a inserção de todos os produtos, as buscas de produtos existentes e inexistentes e a remoção dos 50 produtos selecionados.

O tempo total é medido de maneira independente, não sendo calculado pela soma dos resultados das operações individuais.

### 4.3. Repetições e Medição

Cada medição é executada três vezes, e a mediana dos resultados é utilizada como valor final.

A medição dos intervalos utiliza a função `time.perf_counter()`, que permite obter tempos de alta precisão.

A leitura dos arquivos CSV, a preparação das consultas e a criação das estruturas ficam fora dos intervalos cronometrados correspondentes. Antes das medições, também são realizadas verificações para conferir o funcionamento das operações.

Os resultados de inserção e remoção representam o tempo total das respectivas operações. Já os resultados das buscas representam o tempo médio por consulta.

## 5. Resultados dos Experimentos

Os resultados são apresentados por meio de cinco gráficos de barras agrupadas. Cada gráfico compara as três estruturas nos conjuntos de 10.000, 100.000 e 300.000 produtos.

Os tempos são apresentados em milissegundos (ms). Para facilitar a interpretação de valores muito pequenos, as tabelas também apresentam a representação em notação científica.

### 5.1. Tempo de Inserção

Tempo necessário para inserir todos os produtos em cada estrutura.

![Gráfico de tempo de inserção](<img width="972" height="526" alt="Apresentação - 2° Unidade PA (1)" src="https://github.com/user-attachments/assets/16a1aba1-3e50-4f1c-a3dd-9da750dfadbb" />
)

| Quantidade | Lista Sequencial | Hash com Encadeamento | Hash com Endereçamento Aberto |
|---|---:|---:|---:|
| 10.000 | A preencher | A preencher | A preencher |
| 100.000 | A preencher | A preencher | A preencher |
| 300.000 | A preencher | A preencher | A preencher |

*Formato dos valores: tempo em ms (notação científica em ms).*

### 5.2. Busca de Produto Existente

Tempo médio por consulta para localizar produtos presentes no conjunto de dados.

![Gráfico de busca existente](<img width="977" height="528" alt="Apresentação - 2° Unidade PA (2)" src="https://github.com/user-attachments/assets/69099ee4-d1ef-4d04-88da-a93d2502de61" />
)

| Quantidade | Lista Sequencial | Hash com Encadeamento | Hash com Endereçamento Aberto |
|---|---:|---:|---:|
| 10.000 | A preencher | A preencher | A preencher |
| 100.000 | A preencher | A preencher | A preencher |
| 300.000 | A preencher | A preencher | A preencher |

*Formato dos valores: tempo em ms (notação científica em ms).*

### 5.3. Busca de Produto Inexistente

Tempo médio por consulta para verificar que um produto não está presente no conjunto de dados.

![Gráfico de busca inexistente](<img width="954" height="516" alt="Apresentação - 2° Unidade PA (5)" src="https://github.com/user-attachments/assets/077b4833-5871-4a29-9d22-84a841a8176b" />
)

| Quantidade | Lista Sequencial | Hash com Encadeamento | Hash com Endereçamento Aberto |
|---|---:|---:|---:|
| 10.000 | A preencher | A preencher | A preencher |
| 100.000 | A preencher | A preencher | A preencher |
| 300.000 | A preencher | A preencher | A preencher |

*Formato dos valores: tempo em ms (notação científica em ms).*

### 5.4. Tempo de Remoção

Tempo total necessário para remover os 50 produtos selecionados em cada estrutura.

![Gráfico de tempo de remoção](<img width="979" height="529" alt="Apresentação - 2° Unidade PA (3)" src="https://github.com/user-attachments/assets/c3d8d596-8f8d-4785-83f4-6f421d72b94e" />
)

| Quantidade | Lista Sequencial | Hash com Encadeamento | Hash com Endereçamento Aberto |
|---|---:|---:|---:|
| 10.000 | A preencher | A preencher | A preencher |
| 100.000 | A preencher | A preencher | A preencher |
| 300.000 | A preencher | A preencher | A preencher |

*Formato dos valores: tempo em ms (notação científica em ms).*

### 5.5. Tempo Total do Experimento

Tempo necessário para executar todas as etapas do experimento, desde a inserção dos produtos até a conclusão das remoções.

![Gráfico de tempo total](<img width="970" height="522" alt="Apresentação - 2° Unidade PA (4)" src="https://github.com/user-attachments/assets/55b34c46-16db-4ee0-9d3a-cc3eaf4eda4e" />
)

| Quantidade | Lista Sequencial | Hash com Encadeamento | Hash com Endereçamento Aberto |
|---|---:|---:|---:|
| 10.000 | A preencher | A preencher | A preencher |
| 100.000 | A preencher | A preencher | A preencher |
| 300.000 | A preencher | A preencher | A preencher |

*Formato dos valores: tempo em ms (notação científica em ms).*

### 5.6. Observações sobre os Gráficos

Alguns gráficos utilizam escala logarítmica no eixo vertical para facilitar a visualização de resultados com diferenças muito grandes entre si.

Nessa escala, a distância entre os valores representa diferenças de proporção, e não diferenças lineares. Isso permite visualizar resultados muito pequenos que poderiam ficar praticamente imperceptíveis em uma escala convencional.

Os resultados experimentais representam o comportamento das implementações nas condições específicas dos testes. Portanto, não devem ser interpretados como uma garantia de desempenho para qualquer conjunto de dados ou ambiente de execução.

## 6. Como Executar o Projeto

### 6.1. Pré-requisitos

Para executar o projeto, é necessário possuir:

- Python instalado.
- Pip para instalação de bibliotecas.
- Matplotlib e NumPy para geração dos gráficos.

### 6.2. Clonando o Repositório

```bash
git clone URL_DO_REPOSITORIO
cd NOME_DO_REPOSITORIO
```

### 6.3. Criando um Ambiente Virtual

Recomenda-se utilizar um ambiente virtual para instalar as dependências do projeto sem interferir em outras instalações do Python.

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 6.4. Instalando as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install matplotlib numpy
```

### 6.5. Gerando os Arquivos CSV

Os conjuntos de dados não estão incluídos no repositório. Portanto, antes de executar os testes, é necessário gerá-los:

```bash
python data_generator.py
```

### 6.6. Executando os Experimentos

Com os arquivos CSV disponíveis no diretório `data/`, execute o benchmark:

```bash
python main.py
```

O programa realizará os testes nas três estruturas e gerará os arquivos de resultados:

- `results/benchmark_results.csv`: resultados organizados em formato CSV.
- `results/benchmark_readable.txt`: resultados organizados em formato textual.

### 6.7. Gerando os Gráficos

Após executar o benchmark, execute:

```bash
python plot_benchmark.py
```

Os gráficos serão gerados no diretório:

```text
results/graficos/
```

Dessa forma, é possível reproduzir os experimentos e gerar novamente os resultados e gráficos na própria máquina.
