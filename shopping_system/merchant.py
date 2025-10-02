class Merchant:
    def __init__(self, username, password, shop_name, contact):
        self.username = username
        self.password = password
        self.shop_name = shop_name
        self.contact = contact
        self.products = []  # 商品ID列表
    
    def to_dict(self):
        """转换为字典"""
        return {
            "username": self.username,
            "password": self.password,
            "shop_name": self.shop_name,
            "contact": self.contact,
            "products": self.products
        }
    
    @staticmethod
    def from_dict(data):
        """从字典创建对象"""
        merchant = Merchant(data["username"], data["password"], 
                          data["shop_name"], data["contact"])
        merchant.products = data.get("products", [])
        return merchant