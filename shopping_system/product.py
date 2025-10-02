class Product:
    def __init__(self, product_id, name, price, category, merchant, description="", stock=0):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.category = category
        self.merchant = merchant
        self.description = description
        self.stock = int(stock)
        self.rating = 0.0
        self.review_count = 0
    
    def to_dict(self):
        """转换为字典"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "merchant": self.merchant,
            "description": self.description,
            "stock": self.stock,
            "rating": self.rating,
            "review_count": self.review_count
        }
    
    @staticmethod
    def from_dict(data):
        """从字典创建对象"""
        product = Product(
            data["product_id"],
            data["name"],
            data["price"],
            data["category"],
            data["merchant"],
            data.get("description", ""),
            data.get("stock", 0)
        )
        product.rating = data.get("rating", 0.0)
        product.review_count = data.get("review_count", 0)
        return product