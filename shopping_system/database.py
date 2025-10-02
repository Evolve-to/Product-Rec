import json
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.data_file = "shopping_data.json"
        self.load_data()
    
    def load_data(self):
        """加载数据库"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            # 初始化数据结构
            self.data = {
                "users": {},
                "merchants": {},
                "admins": {"admin": {"password": "admin123", "role": "admin"}},
                "products": {},
                "applications": [],
                "orders": [],
                "reviews": []
            }
            self.save_data()
    
    def save_data(self):
        """保存数据到文件"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_user(self, username, user_data):
        """添加用户"""
        self.data["users"][username] = user_data
        self.save_data()
    
    def add_merchant(self, username, merchant_data):
        """添加商家"""
        self.data["merchants"][username] = merchant_data
        self.save_data()
    
    def add_product(self, product_id, product_data):
        """添加商品"""
        self.data["products"][product_id] = product_data
        self.save_data()
    
    def add_application(self, application_data):
        """添加申请"""
        self.data["applications"].append(application_data)
        self.save_data()
    
    def add_order(self, order_data):
        """添加订单"""
        self.data["orders"].append(order_data)
        self.save_data()
    
    def add_review(self, review_data):
        """添加评价"""
        self.data["reviews"].append(review_data)
        self.save_data()