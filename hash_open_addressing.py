
class HashOpenAddressing:
    DELETED = object()

    def __init__(self, capacity=101):
        self.capacity = capacity
        self.table = [None] * capacity
        self.size = 0

    def _hash(self, product_id): #Tratamento de uso interno
        return product_id % self.capacity

    def insert(self, product):
        product_id = product["id"]
        index = self._hash(product_id)
        first_deleted = None

        for _ in range(self.capacity):
            current = self.table[index]

            if current is None:
                target = (
                    first_deleted
                    if first_deleted is not None
                    else index
                )
                self.table[target] = product
                self.size += 1
                return

            if current is self.DELETED:
                if first_deleted is None:
                    first_deleted = index

            elif current["id"] == product_id:
                self.table[index] = product
                return

            index = (index + 1) % self.capacity

        if first_deleted is not None:
            self.table[first_deleted] = product
            self.size += 1
            return

        raise OverflowError("Tabela Hash cheia.")

    def search(self, product_id):
        index = self._hash(product_id)

        for _ in range(self.capacity):
            current = self.table[index]

            if current is None:
                return None

            if (
                current is not self.DELETED
                and current["id"] == product_id
            ):
                return current

            index = (index + 1) % self.capacity

        return None

    def remove(self, product_id):
        index = self._hash(product_id)

        for _ in range(self.capacity):
            current = self.table[index]

            if current is None:
                return None

            if (
                current is not self.DELETED
                and current["id"] == product_id
            ):
                self.table[index] = self.DELETED
                self.size -= 1
                return current

            index = (index + 1) % self.capacity

        return None

    def __len__(self):
        return self.size
