import uuid
from datetime import datetime
from database import Database
from user import User
from merchant import Merchant
from admin import Admin
from product import Product
from recommendation import RecommendationSystem
from gui import ShoppingGUI

class ShoppingSystem:
    def __init__(self):
        self.db = Database()
        self.recommendation_system = RecommendationSystem(self.db)
        self.current_user = None
    
    def register(self, username, password, email, user_type, shop_name="", contact=""):
        """用户注册"""
        if username in self.db.data["users"] or username in self.db.data["merchants"] or username in self.db.data["admins"]:
            return False
        
        if user_type == "user":
            user = User(username, password, email)
            self.db.add_user(username, user.to_dict())
        elif user_type == "merchant":
            merchant = Merchant(username, password, shop_name, contact)
            self.db.add_merchant(username, merchant.to_dict())
        
        return True
    
    def login(self, username, password, user_type):
        """用户登录"""
        if user_type == "user":
            if username in self.db.data["users"]:
                user_data = self.db.data["users"][username]
                if user_data["password"] == password:
                    self.current_user = username
                    return True
        elif user_type == "merchant":
            if username in self.db.data["merchants"]:
                merchant_data = self.db.data["merchants"][username]
                if merchant_data["password"] == password:
                    self.current_user = username
                    return True
        elif user_type == "admin":
            if username in self.db.data["admins"]:
                admin_data = self.db.data["admins"][username]
                if admin_data["password"] == password:
                    self.current_user = username
                    return True
        
        return False
    
    def get_all_products(self):
        """获取所有已上架商品"""
        products = []
        for product_id, product_data in self.db.data["products"].items():
            if product_data.get("approved", False):
                products.append(product_data)
        return products
    
    def get_product(self, product_id):
        """获取商品信息"""
        return self.db.data["products"].get(product_id)
    
    def add_to_cart(self, username, product_id, quantity=1):
        """添加到购物车"""
        if username not in self.db.data["users"]:
            return False
        
        user_data = self.db.data["users"][username]
        user = User.from_dict(user_data)
        user.add_to_cart(product_id, quantity)
        self.db.data["users"][username] = user.to_dict()
        self.db.save_data()
        return True
    
    def remove_from_cart(self, username, product_id):
        """从购物车移除"""
        if username not in self.db.data["users"]:
            return False
        
        user_data = self.db.data["users"][username]
        user = User.from_dict(user_data)
        user.remove_from_cart(product_id)
        self.db.data["users"][username] = user.to_dict()
        self.db.save_data()
        return True
    
    def clear_cart(self, username):
        """清空购物车"""
        if username not in self.db.data["users"]:
            return False
        
        user_data = self.db.data["users"][username]
        user = User.from_dict(user_data)
        user.clear_cart()
        self.db.data["users"][username] = user.to_dict()
        self.db.save_data()
        return True
    
    def get_cart_items(self, username):
        """获取购物车商品"""
        if username not in self.db.data["users"]:
            return []
        
        user_data = self.db.data["users"][username]
        user = User.from_dict(user_data)
        
        cart_items = []
        for product_id, quantity in user.cart.items():
            product_data = self.db.data["products"].get(product_id)
            if product_data and product_data.get("approved", False):
                cart_items.append({
                    "product_id": product_id,
                    "name": product_data["name"],
                    "price": product_data["price"],
                    "quantity": quantity
                })
        
        return cart_items
    
    def purchase_cart(self, username):
        """购买购物车商品"""
        if username not in self.db.data["users"]:
            return False
        
        cart_items = self.get_cart_items(username)
        if not cart_items:
            return False
        
        # 创建订单
        order_id = str(uuid.uuid4())[:8]
        total_amount = sum(item["price"] * item["quantity"] for item in cart_items)
        
        order_data = {
            "order_id": order_id,
            "user": username,
            "items": cart_items,
            "total_amount": total_amount,
            "order_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "reviewed": False
        }
        
        self.db.add_order(order_data)
        
        # 更新用户订单历史
        user_data = self.db.data["users"][username]
        user = User.from_dict(user_data)
        user.order_history.append(order_id)
        
        # 添加用户偏好
        for item in cart_items:
            product_data = self.db.data["products"][item["product_id"]]
            user.add_preference(product_data["category"])
        
        # 清空购物车
        user.clear_cart()
        self.db.data["users"][username] = user.to_dict()
        self.db.save_data()
        
        return True
    
    def get_user_orders(self, username):
        """获取用户订单"""
        orders = []
        for order in self.db.data["orders"]:
            if order["user"] == username:
                orders.append(order)
        return orders
    
    def record_view_history(self, username, product_id):
        """记录浏览历史"""
        if username not in self.db.data["users"]:
            return
        
        user_data = self.db.data["users"][username]
        user = User.from_dict(user_data)
        user.add_view_history(product_id)
        self.db.data["users"][username] = user.to_dict()
        self.db.save_data()
    
    def get_recommendations(self, username):
        """获取推荐商品"""
        return self.recommendation_system.recommend_for_user(username)
    
    def search_products(self, query, category_filter=None):
        """搜索商品"""
        return self.recommendation_system.search_products(query, category_filter)
    
    def get_categories(self):
        """获取所有商品类别"""
        categories = set()
        for product_data in self.db.data["products"].values():
            if product_data.get("approved", False):
                categories.add(product_data["category"])
        return list(categories)
    
    def submit_review(self, username, order_id, reviews):
        """提交评价"""
        for review_data in reviews:
            review = {
                "review_id": str(uuid.uuid4())[:8],
                "user": username,
                "product_id": review_data["product_id"],
                "product_name": self.db.data["products"][review_data["product_id"]]["name"],
                "merchant": self.db.data["products"][review_data["product_id"]]["merchant"],
                "rating": review_data["rating"],
                "comment": review_data["comment"],
                "review_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.db.add_review(review)
            
            # 更新商品评分
            product_id = review_data["product_id"]
            product_reviews = [r for r in self.db.data["reviews"] if r["product_id"] == product_id]
            if product_reviews:
                total_rating = sum(r["rating"] for r in product_reviews)
                avg_rating = total_rating / len(product_reviews)
                self.db.data["products"][product_id]["rating"] = avg_rating
                self.db.data["products"][product_id]["review_count"] = len(product_reviews)
        
        # 标记订单已评价
        for order in self.db.data["orders"]:
            if order["order_id"] == order_id:
                order["reviewed"] = True
                break
        
        self.db.save_data()
        return True
    
    def apply_product(self, merchant_username, name, price, category, stock, description):
        """申请上架商品"""
        if merchant_username not in self.db.data["merchants"]:
            return False
        
        application_id = str(uuid.uuid4())[:8]
        application_data = {
            "application_id": application_id,
            "merchant": merchant_username,
            "product_name": name,
            "price": float(price),
            "category": category,
            "stock": int(stock),
            "description": description,
            "apply_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "pending"  # pending, approved, rejected
        }
        
        self.db.add_application(application_data)
        return True
    
    def get_merchant_info(self, merchant_username):
        """获取商家信息"""
        return self.db.data["merchants"].get(merchant_username, {})
    
    def get_merchant_products(self, merchant_username):
        """获取商家商品"""
        products = []
        for product_id, product_data in self.db.data["products"].items():
            if product_data["merchant"] == merchant_username:
                products.append(product_data)
        return products
    
    def get_merchant_reviews(self, merchant_username):
        """获取商家商品评价"""
        reviews = []
        for review in self.db.data["reviews"]:
            if review["merchant"] == merchant_username:
                reviews.append(review)
        return reviews
    
    def get_pending_applications(self):
        """获取待审核申请"""
        return [app for app in self.db.data["applications"] if app["status"] == "pending"]
    
    def approve_application(self, application_id):
        """通过申请"""
        for application in self.db.data["applications"]:
            if application["application_id"] == application_id:
                application["status"] = "approved"
                
                # 创建商品
                product_id = str(uuid.uuid4())[:8]
                product_data = {
                    "product_id": product_id,
                    "name": application["product_name"],
                    "price": application["price"],
                    "category": application["category"],
                    "merchant": application["merchant"],
                    "description": application["description"],
                    "stock": application["stock"],
                    "approved": True,
                    "rating": 0.0,
                    "review_count": 0
                }
                
                self.db.add_product(product_id, product_data)
                
                # 更新商家的商品列表
                merchant_data = self.db.data["merchants"][application["merchant"]]
                merchant = Merchant.from_dict(merchant_data)
                merchant.products.append(product_id)
                self.db.data["merchants"][application["merchant"]] = merchant.to_dict()
                
                self.db.save_data()
                return True
        
        return False
    
    def reject_application(self, application_id):
        """拒绝申请"""
        for application in self.db.data["applications"]:
            if application["application_id"] == application_id:
                application["status"] = "rejected"
                self.db.save_data()
                return True
        return False
    
    def get_all_reviews(self):
        """获取所有评价"""
        return self.db.data["reviews"]

def main():
    """主函数"""
    system = ShoppingSystem()
    gui = ShoppingGUI(system)
    gui.run()

if __name__ == "__main__":
    main()