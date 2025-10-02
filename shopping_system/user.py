class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.cart = {}  # {product_id: quantity}
        self.order_history = []
        self.preferences = set()  # 用户偏好类别
        self.view_history = []    # 浏览历史
    
    def to_dict(self):
        """转换为字典"""
        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "cart": self.cart,
            "order_history": self.order_history,
            "preferences": list(self.preferences),
            "view_history": self.view_history
        }
    
    @staticmethod
    def from_dict(data):
        """从字典创建对象"""
        user = User(data["username"], data["password"], data["email"])
        user.cart = data.get("cart", {})
        user.order_history = data.get("order_history", [])
        user.preferences = set(data.get("preferences", []))
        user.view_history = data.get("view_history", [])
        return user
    
    def add_to_cart(self, product_id, quantity=1):
        """添加到购物车"""
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
    
    def remove_from_cart(self, product_id):
        """从购物车移除"""
        if product_id in self.cart:
            del self.cart[product_id]
    
    def clear_cart(self):
        """清空购物车"""
        self.cart.clear()
    
    def add_preference(self, category):
        """添加偏好"""
        self.preferences.add(category)
    
    def add_view_history(self, product_id):
        """添加浏览历史"""
        if product_id in self.view_history:
            self.view_history.remove(product_id)
        self.view_history.append(product_id)
        # 只保留最近20条记录
        if len(self.view_history) > 20:
            self.view_history = self.view_history[-20:]