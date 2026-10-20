
class HashChaining:
    def __init__(self, capacity=101):
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _hash(self, product_id): #Tratamento de uso interno
        return product_id % self.capacity

    def insert(self, product):
        index = self._hash(product["id"])
        bucket = self.buckets[index]

        for i, existing in enumerate(bucket):
            if existing["id"] == product["id"]:
                bucket[i] = product
                return

        bucket.append(product)
        self.size += 1

    def search(self, product_id):
        index = self._hash(product_id)
        bucket = self.buckets[index]

        for product in bucket:
            if product["id"] == product_id:
                return product

        return None

    def remove(self, product_id):
        index = self._hash(product_id)
        bucket = self.buckets[index]

        for i, product in enumerate(bucket):
            if product["id"] == product_id:
                removed = bucket.pop(i)
                self.size -= 1
                return removed

        return None

    def __len__(self):
        return self.size
