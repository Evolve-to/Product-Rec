import math
from collections import Counter

class RecommendationSystem:
    def __init__(self, database):
        self.db = database
    
    def recommend_for_user(self, username, max_recommendations=10):
        """为用户推荐商品"""
        if username not in self.db.data["users"]:
            return []
        
        user_data = self.db.data["users"][username]
        
        # 直接使用字典数据而不是User对象
        user_preferences = set(user_data.get("preferences", []))
        user_view_history = user_data.get("view_history", [])
        user_order_history = user_data.get("order_history", [])
        
        recommendations = []
        
        # 基于偏好的推荐
        if user_preferences:
            for product_id, product_data in self.db.data["products"].items():
                if (product_data.get("approved", False) and
                    product_data["category"] in user_preferences and 
                    product_id not in user_view_history):
                    recommendations.append((product_id, 2.0))  # 偏好权重
        
        # 基于浏览历史的推荐
        recent_views = user_view_history[-5:]  # 最近浏览的5个商品
        for viewed_id in recent_views:
            viewed_product = self.db.data["products"].get(viewed_id)
            if viewed_product and viewed_product.get("approved", False):
                category = viewed_product["category"]
                # 推荐同类别商品
                for product_id, product_data in self.db.data["products"].items():
                    if (product_data.get("approved", False) and
                        product_data["category"] == category and 
                        product_id != viewed_id and 
                        product_id not in user_view_history):
                        recommendations.append((product_id, 1.5))  # 同类权重
        
        # 基于热门商品的推荐
        product_scores = Counter()
        for order in self.db.data["orders"]:
            for item in order.get("items", []):
                product_scores[item["product_id"]] += 1
        
        for product_id, score in product_scores.most_common(10):
            product_data = self.db.data["products"].get(product_id)
            if (product_data and product_data.get("approved", False) and
                product_id not in user_view_history):
                recommendations.append((product_id, math.log(score + 1)))  # 热门权重
        
        # 去重并排序
        rec_dict = {}
        for product_id, score in recommendations:
            if product_id in rec_dict:
                rec_dict[product_id] += score
            else:
                rec_dict[product_id] = score
        
        # 按分数排序并返回商品信息
        sorted_recs = sorted(rec_dict.items(), key=lambda x: x[1], reverse=True)
        result = []
        for product_id, score in sorted_recs[:max_recommendations]:
            product_data = self.db.data["products"].get(product_id)
            if product_data:
                result.append(product_data)
        
        return result
    
    def search_products(self, query, category_filter=None):
        """搜索商品（模糊匹配）"""
        results = []
        query = query.lower().strip()
        
        if not query:  # 如果查询为空，返回空结果
            return results
            
        for product_id, product_data in self.db.data["products"].items():
            # 检查商品是否上架
            if not product_data.get("approved", False):
                continue
            
            # 类别过滤
            if category_filter and product_data["category"] != category_filter:
                continue
            
            # 模糊匹配商品名和描述
            name_match = query in product_data["name"].lower()
            desc_match = query in product_data.get("description", "").lower()
            category_match = query in product_data["category"].lower()
            
            if name_match or desc_match or category_match:
                # 计算匹配度分数
                score = 0
                if name_match:
                    score += 3
                if desc_match:
                    score += 1
                if category_match:
                    score += 2
                
                results.append((product_data, score))
        
        # 按匹配度排序
        results.sort(key=lambda x: x[1], reverse=True)
        return [result[0] for result in results]
    
    def get_similar_products(self, product_id, max_results=5):
        """获取相似商品（基于类别）"""
        if product_id not in self.db.data["products"]:
            return []
        
        target_product = self.db.data["products"][product_id]
        target_category = target_product["category"]
        
        similar_products = []
        for pid, product in self.db.data["products"].items():
            if (pid != product_id and 
                product.get("approved", False) and 
                product["category"] == target_category):
                similar_products.append(product)
        
        return similar_products[:max_results]
    
    def update_product_ratings(self):
        """更新所有商品的评分"""
        # 收集所有商品的评价
        product_reviews = {}
        for review in self.db.data["reviews"]:
            product_id = review["product_id"]
            if product_id not in product_reviews:
                product_reviews[product_id] = []
            product_reviews[product_id].append(review["rating"])
        
        # 更新商品评分
        for product_id, ratings in product_reviews.items():
            if product_id in self.db.data["products"]:
                avg_rating = sum(ratings) / len(ratings)
                self.db.data["products"][product_id]["rating"] = round(avg_rating, 1)
                self.db.data["products"][product_id]["review_count"] = len(ratings)
        
        self.db.save_data()