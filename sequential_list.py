class SequentialList:
    def __init__(self):
        self.products = []

    def insert(self, product):
        self.products.append(product)

    def search(self, product_id):
        for product in self.products:
            if product["id"] == product_id:
                return product

        return None

    def remove(self, product_id):
        for index, product in enumerate(self.products):
            if product["id"] == product_id:
                return self.products.pop(index)

        return None

    def __len__(self):
        return len(self.products)
