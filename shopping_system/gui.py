import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re


class ShoppingGUI:
    def __init__(self, shopping_system):
        self.system = shopping_system
        self.current_user = None
        self.user_type = None

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("商品购物推荐系统")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # 设置样式
        self.setup_styles()
        self.create_login_frame()

    def setup_styles(self):
        """设置界面样式"""
        style = ttk.Style()
        style.configure("Header.TFrame", background="#2c3e50")
        style.configure("Header.TLabel", background="#2c3e50", foreground="white", font=("Arial", 16, "bold"))
        style.configure("Nav.TFrame", background="#34495e")
        style.configure("Nav.TButton", font=("Arial", 10))
        style.configure("Card.TFrame", relief="raised", borderwidth=1)
        style.configure("Title.TLabel", font=("Arial", 14, "bold"))
        style.configure("Price.TLabel", font=("Arial", 12, "bold"), foreground="#e74c3c")

    def create_login_frame(self):
        """创建登录界面"""
        self.clear_frame()

        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # 标题区域
        header_frame = ttk.Frame(main_frame, style="Header.TFrame", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        ttk.Label(header_frame, text="商品购物推荐系统", style="Header.TLabel").pack(pady=25)

        # 登录表单区域
        login_frame = ttk.Frame(main_frame)
        login_frame.pack(expand=True)

        # 登录卡片
        card_frame = ttk.Frame(login_frame, style="Card.TFrame", padding="30")
        card_frame.pack()

        ttk.Label(card_frame, text="用户登录", font=("Arial", 18, "bold"), anchor="center").pack(pady=(0, 20))

        # 用户名输入
        ttk.Label(card_frame, text="用户名:", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        self.username_entry = ttk.Entry(card_frame, width=30, font=("Arial", 11))
        self.username_entry.pack(pady=(0, 10))

        # 密码输入
        ttk.Label(card_frame, text="密码:", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        self.password_entry = ttk.Entry(card_frame, width=30, show="*", font=("Arial", 11))
        self.password_entry.pack(pady=(0, 15))

        # 用户类型选择
        ttk.Label(card_frame, text="用户类型:", font=("Arial", 10)).pack(anchor="w", pady=(5, 0))
        self.user_type_var = tk.StringVar(value="user")
        user_frame = ttk.Frame(card_frame)
        user_frame.pack(pady=(0, 20))

        ttk.Radiobutton(user_frame, text="用户", variable=self.user_type_var, value="user").pack(side="left",
                                                                                                 padx=(0, 15))
        ttk.Radiobutton(user_frame, text="商家", variable=self.user_type_var, value="merchant").pack(side="left",
                                                                                                     padx=(0, 15))
        ttk.Radiobutton(user_frame, text="管理员", variable=self.user_type_var, value="admin").pack(side="left")

        # 按钮区域
        button_frame = ttk.Frame(card_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(button_frame, text="登录", command=self.login).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="注册", command=self.show_register).pack(side="left")

        # 绑定回车键
        self.root.bind('<Return>', lambda event: self.login())

    def show_register(self):
        """显示注册界面"""
        self.clear_frame()

        # 主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # 标题区域
        header_frame = ttk.Frame(main_frame, style="Header.TFrame", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)

        ttk.Label(header_frame, text="商品购物推荐系统", style="Header.TLabel").pack(pady=25)

        # 注册表单区域
        register_frame = ttk.Frame(main_frame)
        register_frame.pack(expand=True)

        # 注册卡片
        card_frame = ttk.Frame(register_frame, style="Card.TFrame", padding="30")
        card_frame.pack()

        ttk.Label(card_frame, text="用户注册", font=("Arial", 18, "bold"), anchor="center").pack(pady=(0, 20))

        # 表单字段
        fields_frame = ttk.Frame(card_frame)
        fields_frame.pack()

        # 用户名
        ttk.Label(fields_frame, text="用户名:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        reg_username = ttk.Entry(fields_frame, width=25, font=("Arial", 11))
        reg_username.grid(row=0, column=1, padx=(10, 0), pady=5)

        # 密码
        ttk.Label(fields_frame, text="密码:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        reg_password = ttk.Entry(fields_frame, width=25, show="*", font=("Arial", 11))
        reg_password.grid(row=1, column=1, padx=(10, 0), pady=5)

        # 邮箱
        ttk.Label(fields_frame, text="邮箱:", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        reg_email = ttk.Entry(fields_frame, width=25, font=("Arial", 11))
        reg_email.grid(row=2, column=1, padx=(10, 0), pady=5)

        # 商家信息（默认隐藏）
        shop_frame = ttk.Frame(card_frame)
        shop_frame.pack(pady=10)
        shop_frame.pack_forget()  # 默认隐藏

        ttk.Label(shop_frame, text="店铺名:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        reg_shop_name = ttk.Entry(shop_frame, width=25, font=("Arial", 11))
        reg_shop_name.grid(row=0, column=1, padx=(10, 0), pady=5)

        ttk.Label(shop_frame, text="联系方式:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        reg_contact = ttk.Entry(shop_frame, width=25, font=("Arial", 11))
        reg_contact.grid(row=1, column=1, padx=(10, 0), pady=5)

        # 用户类型选择
        ttk.Label(card_frame, text="用户类型:", font=("Arial", 10)).pack(anchor="w", pady=(15, 5))
        reg_user_type = tk.StringVar(value="user")
        type_frame = ttk.Frame(card_frame)
        type_frame.pack(pady=(0, 15))

        def on_user_type_change(*args):
            if reg_user_type.get() == "merchant":
                shop_frame.pack(pady=10)
            else:
                shop_frame.pack_forget()

        reg_user_type.trace("w", on_user_type_change)

        ttk.Radiobutton(type_frame, text="用户", variable=reg_user_type, value="user").pack(side="left", padx=(0, 15))
        ttk.Radiobutton(type_frame, text="商家", variable=reg_user_type, value="merchant").pack(side="left")

        def register():
            username = reg_username.get()
            password = reg_password.get()
            email = reg_email.get()
            user_type = reg_user_type.get()
            shop_name = reg_shop_name.get()
            contact = reg_contact.get()

            if not username or not password or not email:
                messagebox.showerror("错误", "请填写完整信息！")
                return

            if user_type == "merchant" and (not shop_name or not contact):
                messagebox.showerror("错误", "商家请填写店铺名和联系方式！")
                return

            if self.system.register(username, password, email, user_type, shop_name, contact):
                messagebox.showinfo("成功", "注册成功！")
                self.create_login_frame()
            else:
                messagebox.showerror("错误", "用户名已存在！")

        # 按钮区域
        button_frame = ttk.Frame(card_frame)
        button_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(button_frame, text="注册", command=register).pack(side="left", padx=(0, 10))
        ttk.Button(button_frame, text="返回登录", command=self.create_login_frame).pack(side="left")

    def create_user_dashboard(self):
        """创建用户主界面"""
        self.clear_frame()

        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # 创建顶部导航栏
        self.create_user_navbar(main_frame)

        # 创建内容区域
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 显示推荐商品
        self.show_recommendations()

    def create_user_navbar(self, parent):
        """创建用户导航栏"""
        nav_frame = ttk.Frame(parent, style="Nav.TFrame", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        # 左侧导航按钮
        left_frame = ttk.Frame(nav_frame, style="Nav.TFrame")
        left_frame.pack(side="left", fill="y")

        ttk.Button(left_frame, text="首页", style="Nav.TButton",
                   command=self.show_recommendations).pack(side="left", padx=5, pady=10)
        ttk.Button(left_frame, text="商品浏览", style="Nav.TButton",
                   command=self.browse_products).pack(side="left", padx=5, pady=10)
        ttk.Button(left_frame, text="搜索", style="Nav.TButton",
                   command=self.search_products).pack(side="left", padx=5, pady=10)

        # 右侧用户信息
        right_frame = ttk.Frame(nav_frame, style="Nav.TFrame")
        right_frame.pack(side="right", fill="y")

        ttk.Label(right_frame, text=f"欢迎, {self.current_user}!",
                  foreground="white", background="#34495e",
                  font=("Arial", 10)).pack(side="left", padx=10, pady=15)
        ttk.Button(right_frame, text="购物车", style="Nav.TButton",
                   command=self.view_cart).pack(side="left", padx=5, pady=10)
        ttk.Button(right_frame, text="我的订单", style="Nav.TButton",
                   command=self.view_orders).pack(side="left", padx=5, pady=10)
        ttk.Button(right_frame, text="退出", style="Nav.TButton",
                   command=self.logout).pack(side="left", padx=5, pady=10)

    def browse_products(self):
        """浏览商品"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="所有商品", style="Title.TLabel").pack(side="left")

        # 商品展示区域
        canvas_frame = ttk.Frame(self.content_frame)
        canvas_frame.pack(fill="both", expand=True)

        # 创建Canvas和滚动条
        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 获取商品数据
        products = self.system.get_all_products()

        # 创建商品网格
        self.create_product_grid(scrollable_frame, products)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_product_grid(self, parent, products):
        """创建商品网格布局"""
        # 计算行数和列数
        cols = 4
        rows = (len(products) + cols - 1) // cols

        for i, product in enumerate(products):
            row = i // cols
            col = i % cols

            # 商品卡片
            card_frame = ttk.Frame(parent, style="Card.TFrame", padding="10")
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # 商品名称
            name_label = ttk.Label(card_frame, text=product["name"],
                                   font=("Arial", 11, "bold"), wraplength=150)
            name_label.pack(anchor="w", pady=(0, 5))

            # 商品价格
            price_label = ttk.Label(card_frame, text=f"¥{product['price']}",
                                    style="Price.TLabel")
            price_label.pack(anchor="w", pady=(0, 5))

            # 商品类别
            category_label = ttk.Label(card_frame, text=f"类别: {product['category']}",
                                       font=("Arial", 9))
            category_label.pack(anchor="w", pady=(0, 5))

            # 商家信息
            merchant_label = ttk.Label(card_frame, text=f"商家: {product['merchant']}",
                                       font=("Arial", 9))
            merchant_label.pack(anchor="w", pady=(0, 10))

            # 操作按钮
            button_frame = ttk.Frame(card_frame)
            button_frame.pack(fill="x")

            ttk.Button(button_frame, text="查看详情", width=10,
                       command=lambda p=product: self.show_product_detail(p)).pack(side="left", padx=(0, 5))
            ttk.Button(button_frame, text="加入购物车", width=10,
                       command=lambda p=product: self.add_to_cart(p["product_id"])).pack(side="left")

        # 配置网格权重
        for i in range(cols):
            parent.columnconfigure(i, weight=1)

    def show_product_detail(self, product):
        """显示商品详情"""
        # 创建详情窗口
        detail_window = tk.Toplevel(self.root)
        detail_window.title("商品详情")
        detail_window.geometry("500x400")
        detail_window.resizable(False, False)

        # 主框架
        main_frame = ttk.Frame(detail_window, padding="20")
        main_frame.pack(fill="both", expand=True)

        # 商品名称
        ttk.Label(main_frame, text=product["name"],
                  font=("Arial", 16, "bold")).pack(pady=(0, 15))

        # 价格信息
        price_frame = ttk.Frame(main_frame)
        price_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(price_frame, text="价格:", font=("Arial", 12)).pack(side="left")
        ttk.Label(price_frame, text=f"¥{product['price']}",
                  style="Price.TLabel").pack(side="left", padx=(10, 0))

        # 其他信息
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(info_frame, text=f"类别: {product['category']}",
                  font=("Arial", 11)).pack(anchor="w", pady=2)
        ttk.Label(info_frame, text=f"商家: {product['merchant']}",
                  font=("Arial", 11)).pack(anchor="w", pady=2)
        ttk.Label(info_frame, text=f"库存: {product.get('stock', 0)}",
                  font=("Arial", 11)).pack(anchor="w", pady=2)

        # 商品描述
        ttk.Label(main_frame, text="商品描述:", font=("Arial", 12, "bold")).pack(anchor="w", pady=(10, 5))

        desc_frame = ttk.Frame(main_frame)
        desc_frame.pack(fill="both", expand=True, pady=(0, 15))

        desc_text = scrolledtext.ScrolledText(desc_frame, height=8, wrap=tk.WORD)
        desc_text.insert("1.0", product.get("description", "暂无描述"))
        desc_text.config(state="disabled")
        desc_text.pack(fill="both", expand=True)

        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x")

        ttk.Button(button_frame, text="加入购物车",
                   command=lambda: [self.add_to_cart(product["product_id"]), detail_window.destroy()]).pack(side="left",
                                                                                                            padx=(0,
                                                                                                                  10))
        ttk.Button(button_frame, text="关闭",
                   command=detail_window.destroy).pack(side="left")

    def add_to_cart(self, product_id, quantity=1):
        """添加到购物车"""
        if self.system.add_to_cart(self.current_user, product_id, quantity):
            messagebox.showinfo("成功", "已添加到购物车！")
        else:
            messagebox.showerror("错误", "添加失败！")

    def view_cart(self):
        """查看购物车"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="我的购物车", style="Title.TLabel").pack(side="left")

        # 购物车内容
        cart_items = self.system.get_cart_items(self.current_user)
        if not cart_items:
            ttk.Label(self.content_frame, text="购物车为空", font=("Arial", 12)).pack(pady=50)
            return

        # 创建表格
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, columns=("name", "price", "quantity", "total"), show="headings", height=15)
        tree.heading("name", text="商品名")
        tree.heading("price", text="单价")
        tree.heading("quantity", text="数量")
        tree.heading("total", text="小计")

        tree.column("name", width=200)
        tree.column("price", width=100, anchor="center")
        tree.column("quantity", width=100, anchor="center")
        tree.column("total", width=100, anchor="center")

        total_amount = 0
        for item in cart_items:
            subtotal = item["price"] * item["quantity"]
            total_amount += subtotal
            tree.insert("", "end", values=(
                item["name"],
                f"¥{item['price']}",
                item["quantity"],
                f"¥{subtotal}"
            ), tags=(item["product_id"],))

        tree.pack(side="left", fill="both", expand=True)

        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # 总计和操作按钮
        bottom_frame = ttk.Frame(self.content_frame)
        bottom_frame.pack(fill="x", pady=15)

        ttk.Label(bottom_frame, text=f"总计: ¥{total_amount}",
                  font=("Arial", 14, "bold")).pack(side="left")

        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(side="right")

        ttk.Button(button_frame, text="删除选中",
                   command=lambda: self.remove_from_cart(tree)).pack(side="left", padx=5)
        ttk.Button(button_frame, text="清空购物车",
                   command=self.clear_cart).pack(side="left", padx=5)
        ttk.Button(button_frame, text="立即购买",
                   command=lambda: self.purchase_cart(total_amount)).pack(side="left", padx=5)

    def remove_from_cart(self, tree):
        """从购物车删除"""
        selection = tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请选择商品！")
            return

        product_id = tree.item(selection[0])["tags"][0]
        if self.system.remove_from_cart(self.current_user, product_id):
            messagebox.showinfo("成功", "已从购物车删除！")
            self.view_cart()
        else:
            messagebox.showerror("错误", "删除失败！")

    def clear_cart(self):
        """清空购物车"""
        if messagebox.askyesno("确认", "确定要清空购物车吗？"):
            if self.system.clear_cart(self.current_user):
                messagebox.showinfo("成功", "购物车已清空！")
                self.view_cart()

    def purchase_cart(self, total_amount):
        """购买购物车商品"""
        if messagebox.askyesno("确认", f"确定要购买吗？总金额: ¥{total_amount}"):
            if self.system.purchase_cart(self.current_user):
                messagebox.showinfo("成功", "购买成功！")
                self.view_cart()
            else:
                messagebox.showerror("错误", "购买失败！")

    def search_products(self):
        """搜索商品"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="搜索商品", style="Title.TLabel").pack(side="left")

        # 搜索区域
        search_frame = ttk.Frame(self.content_frame)
        search_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(search_frame, text="关键词:").pack(side="left")
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side="left", padx=5)

        ttk.Label(search_frame, text="类别:").pack(side="left", padx=(20, 5))
        category_var = tk.StringVar()
        categories = self.system.get_categories()
        category_combo = ttk.Combobox(search_frame, textvariable=category_var,
                                      values=["所有"] + categories, width=15)
        category_combo.set("所有")
        category_combo.pack(side="left", padx=5)

        def perform_search():
            query = search_entry.get()
            category = category_var.get() if category_var.get() != "所有" else None
            results = self.system.search_products(query, category)
            display_results(results)

        ttk.Button(search_frame, text="搜索", command=perform_search).pack(side="left", padx=5)

        # 结果显示区域
        self.results_container = ttk.Frame(self.content_frame)
        self.results_container.pack(fill="both", expand=True)

        def display_results(products):
            # 清空之前的结果
            for widget in self.results_container.winfo_children():
                widget.destroy()

            if not products:
                ttk.Label(self.results_container, text="未找到相关商品",
                          font=("Arial", 12)).pack(pady=50)
                return

            # 创建商品网格
            canvas_frame = ttk.Frame(self.results_container)
            canvas_frame.pack(fill="both", expand=True)

            canvas = tk.Canvas(canvas_frame)
            scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            self.create_product_grid(scrollable_frame, products)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

        # 绑定回车键
        search_entry.bind('<Return>', lambda event: perform_search())

    def show_recommendations(self):
        """显示推荐商品"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="为您推荐", style="Title.TLabel").pack(side="left")

        # 获取推荐商品
        recommendations = self.system.get_recommendations(self.current_user)
        if not recommendations:
            ttk.Label(self.content_frame, text="暂无推荐", font=("Arial", 12)).pack(pady=50)
            return

        # 创建推荐商品网格
        canvas_frame = ttk.Frame(self.content_frame)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        self.create_product_grid(scrollable_frame, recommendations)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def view_orders(self):
        """查看订单"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="我的订单", style="Title.TLabel").pack(side="left")

        # 获取订单数据
        orders = self.system.get_user_orders(self.current_user)
        if not orders:
            ttk.Label(self.content_frame, text="暂无订单", font=("Arial", 12)).pack(pady=50)
            return

        # 创建订单列表
        canvas_frame = ttk.Frame(self.content_frame)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 显示订单
        for order in orders:
            order_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding="15")
            order_frame.pack(fill="x", pady=5)

            # 订单头部信息
            header_frame = ttk.Frame(order_frame)
            header_frame.pack(fill="x", pady=(0, 10))

            ttk.Label(header_frame, text=f"订单号: {order['order_id']}",
                      font=("Arial", 11, "bold")).pack(side="left")
            ttk.Label(header_frame, text=f"{order['order_time']}",
                      font=("Arial", 10)).pack(side="right")

            # 订单商品
            items_frame = ttk.Frame(order_frame)
            items_frame.pack(fill="x", pady=(0, 10))

            for item in order["items"]:
                item_frame = ttk.Frame(items_frame)
                item_frame.pack(fill="x", pady=2)
                ttk.Label(item_frame, text=f"{item['name']} x{item['quantity']}").pack(side="left")
                ttk.Label(item_frame, text=f"¥{item['price'] * item['quantity']}").pack(side="right")

            # 订单总额
            total_frame = ttk.Frame(order_frame)
            total_frame.pack(fill="x", pady=(0, 10))
            ttk.Label(total_frame, text=f"总计: ¥{order['total_amount']}",
                      font=("Arial", 12, "bold")).pack(side="right")

            # 评价按钮
            if not order.get("reviewed", False):
                ttk.Button(order_frame, text="评价商品",
                           command=lambda o=order: self.review_order(o)).pack(anchor="e")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def review_order(self, order):
        """评价订单"""
        review_window = tk.Toplevel(self.root)
        review_window.title("商品评价")
        review_window.geometry("500x400")

        # 主框架
        main_frame = ttk.Frame(review_window, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="商品评价", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # 创建Canvas和滚动条用于评价表单
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 评价控件列表
        review_controls = []

        # 为每个商品创建评价表单
        for item in order["items"]:
            item_frame = ttk.LabelFrame(scrollable_frame, text=item["name"], padding="15")
            item_frame.pack(fill="x", pady=10)

            # 评分
            rating_frame = ttk.Frame(item_frame)
            rating_frame.pack(fill="x", pady=5)
            ttk.Label(rating_frame, text="评分:").pack(side="left")
            rating_var = tk.StringVar(value="5")
            rating_combo = ttk.Combobox(rating_frame, textvariable=rating_var,
                                        values=["1", "2", "3", "4", "5"],
                                        state="readonly", width=5)
            rating_combo.pack(side="left", padx=10)

            # 评论
            ttk.Label(item_frame, text="评论:").pack(anchor="w", pady=(10, 5))
            review_text = scrolledtext.ScrolledText(item_frame, height=4, width=40)
            review_text.pack(fill="x", expand=True)

            review_controls.append({
                "product_id": item["product_id"],
                "rating_var": rating_var,
                "review_text": review_text
            })

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def submit_review():
            reviews = []
            for control in review_controls:
                rating = int(control["rating_var"].get())
                comment = control["review_text"].get("1.0", "end-1c").strip()
                if comment:
                    reviews.append({
                        "product_id": control["product_id"],
                        "rating": rating,
                        "comment": comment
                    })

            if reviews:
                if self.system.submit_review(self.current_user, order["order_id"], reviews):
                    messagebox.showinfo("成功", "评价提交成功！")
                    review_window.destroy()
                    self.view_orders()
                else:
                    messagebox.showerror("错误", "评价提交失败！")
            else:
                messagebox.showwarning("警告", "请至少填写一条评论！")

        # 提交按钮
        ttk.Button(main_frame, text="提交评价", command=submit_review).pack(pady=20)

    def create_merchant_dashboard(self):
        """创建商家主界面"""
        self.clear_frame()

        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # 创建顶部导航栏
        self.create_merchant_navbar(main_frame)

        # 创建内容区域
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 显示商家商品
        self.view_merchant_products()

    def create_merchant_navbar(self, parent):
        """创建商家导航栏"""
        nav_frame = ttk.Frame(parent, style="Nav.TFrame", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        # 左侧导航按钮
        left_frame = ttk.Frame(nav_frame, style="Nav.TFrame")
        left_frame.pack(side="left", fill="y")

        ttk.Button(left_frame, text="我的商品", style="Nav.TButton",
                   command=self.view_merchant_products).pack(side="left", padx=5, pady=10)
        ttk.Button(left_frame, text="申请上架", style="Nav.TButton",
                   command=self.apply_product).pack(side="left", padx=5, pady=10)
        ttk.Button(left_frame, text="商品评价", style="Nav.TButton",
                   command=self.view_product_reviews).pack(side="left", padx=5, pady=10)

        # 右侧用户信息
        right_frame = ttk.Frame(nav_frame, style="Nav.TFrame")
        right_frame.pack(side="right", fill="y")

        merchant_info = self.system.get_merchant_info(self.current_user)
        ttk.Label(right_frame, text=f"欢迎, {merchant_info['shop_name']}!",
                  foreground="white", background="#34495e",
                  font=("Arial", 10)).pack(side="left", padx=10, pady=15)
        ttk.Button(right_frame, text="退出", style="Nav.TButton",
                   command=self.logout).pack(side="left", padx=5, pady=10)

    def apply_product(self):
        """申请上架商品"""
        apply_window = tk.Toplevel(self.root)
        apply_window.title("申请上架商品")
        apply_window.geometry("600x500")

        # 主框架
        main_frame = ttk.Frame(apply_window, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="商品上架申请", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # 表单区域
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill="both", expand=True)

        # 商品名称
        ttk.Label(form_frame, text="商品名称:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(form_frame, width=40)
        name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)

        # 价格
        ttk.Label(form_frame, text="价格:").grid(row=1, column=0, sticky="w", pady=5)
        price_entry = ttk.Entry(form_frame, width=40)
        price_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # 类别
        ttk.Label(form_frame, text="类别:").grid(row=2, column=0, sticky="w", pady=5)
        category_entry = ttk.Entry(form_frame, width=40)
        category_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)

        # 库存
        ttk.Label(form_frame, text="库存:").grid(row=3, column=0, sticky="w", pady=5)
        stock_entry = ttk.Entry(form_frame, width=40)
        stock_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)

        # 商品描述
        ttk.Label(form_frame, text="商品描述:").grid(row=4, column=0, sticky="nw", pady=5)
        desc_text = scrolledtext.ScrolledText(form_frame, height=8)
        desc_text.grid(row=4, column=1, sticky="nsew", padx=10, pady=5)

        # 配置网格权重
        form_frame.columnconfigure(1, weight=1)
        form_frame.rowconfigure(4, weight=1)

        def submit_application():
            name = name_entry.get()
            price = price_entry.get()
            category = category_entry.get()
            stock = stock_entry.get()
            description = desc_text.get("1.0", "end-1c")

            if not all([name, price, category, stock]):
                messagebox.showerror("错误", "请填写完整信息！")
                return

            try:
                float(price)
                int(stock)
            except ValueError:
                messagebox.showerror("错误", "价格和库存必须是数字！")
                return

            if self.system.apply_product(self.current_user, name, price, category, stock, description):
                messagebox.showinfo("成功", "申请已提交，等待管理员审核！")
                apply_window.destroy()
            else:
                messagebox.showerror("错误", "申请提交失败！")

        # 提交按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20)
        ttk.Button(button_frame, text="提交申请", command=submit_application).pack(side="right")

    def view_merchant_products(self):
        """查看商家商品"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="我的商品", style="Title.TLabel").pack(side="left")

        # 获取商品数据
        products = self.system.get_merchant_products(self.current_user)
        if not products:
            ttk.Label(self.content_frame, text="暂无商品", font=("Arial", 12)).pack(pady=50)
            return

        # 创建表格
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, columns=("name", "price", "category", "stock", "status"), show="headings",
                            height=15)
        tree.heading("name", text="商品名")
        tree.heading("price", text="价格")
        tree.heading("category", text="类别")
        tree.heading("stock", text="库存")
        tree.heading("status", text="状态")

        tree.column("name", width=200)
        tree.column("price", width=100, anchor="center")
        tree.column("category", width=100, anchor="center")
        tree.column("stock", width=80, anchor="center")
        tree.column("status", width=100, anchor="center")

        for product in products:
            status = "已上架" if product.get("approved", False) else "待审核"
            tree.insert("", "end", values=(
                product["name"],
                f"¥{product['price']}",
                product["category"],
                product["stock"],
                status
            ), tags=(product["product_id"],))

        tree.pack(side="left", fill="both", expand=True)

        # 滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def view_product_reviews(self):
        """查看商品评价"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="商品评价", style="Title.TLabel").pack(side="left")

        # 获取评价数据
        reviews = self.system.get_merchant_reviews(self.current_user)
        if not reviews:
            ttk.Label(self.content_frame, text="暂无评价", font=("Arial", 12)).pack(pady=50)
            return

        # 创建评价列表
        canvas_frame = ttk.Frame(self.content_frame)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 显示评价
        for review in reviews:
            review_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding="15")
            review_frame.pack(fill="x", pady=5)

            # 商品名称
            ttk.Label(review_frame, text=f"商品: {review['product_name']}",
                      font=("Arial", 11, "bold")).pack(anchor="w")

            # 评分
            rating_text = "★" * review['rating'] + "☆" * (5 - review['rating'])
            ttk.Label(review_frame, text=f"评分: {rating_text}").pack(anchor="w", pady=2)

            # 评论内容
            ttk.Label(review_frame, text=f"评论: {review['comment']}",
                      wraplength=500).pack(anchor="w", pady=2)

            # 用户信息和时间
            ttk.Label(review_frame, text=f"用户: {review['user']} - {review['review_time']}",
                      font=("Arial", 9)).pack(anchor="w", pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_admin_dashboard(self):
        """创建管理员主界面"""
        self.clear_frame()

        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)

        # 创建顶部导航栏
        self.create_admin_navbar(main_frame)

        # 创建内容区域
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # 显示待审核申请
        self.review_applications()

    def create_admin_navbar(self, parent):
        """创建管理员导航栏"""
        nav_frame = ttk.Frame(parent, style="Nav.TFrame", height=50)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        # 左侧导航按钮
        left_frame = ttk.Frame(nav_frame, style="Nav.TFrame")
        left_frame.pack(side="left", fill="y")

        ttk.Button(left_frame, text="审核申请", style="Nav.TButton",
                   command=self.review_applications).pack(side="left", padx=5, pady=10)
        ttk.Button(left_frame, text="商品管理", style="Nav.TButton",
                   command=self.admin_search_products).pack(side="left", padx=5, pady=10)
        ttk.Button(left_frame, text="评价管理", style="Nav.TButton",
                   command=self.view_all_reviews).pack(side="left", padx=5, pady=10)

        # 右侧用户信息
        right_frame = ttk.Frame(nav_frame, style="Nav.TFrame")
        right_frame.pack(side="right", fill="y")

        ttk.Label(right_frame, text="欢迎, 管理员!",
                  foreground="white", background="#34495e",
                  font=("Arial", 10)).pack(side="left", padx=10, pady=15)
        ttk.Button(right_frame, text="退出", style="Nav.TButton",
                   command=self.logout).pack(side="left", padx=5, pady=10)

    def review_applications(self):
        """审核上架申请"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="上架申请审核", style="Title.TLabel").pack(side="left")

        # 获取待审核申请
        applications = self.system.get_pending_applications()
        if not applications:
            ttk.Label(self.content_frame, text="暂无待审核申请", font=("Arial", 12)).pack(pady=50)
            return

        # 创建申请列表
        canvas_frame = ttk.Frame(self.content_frame)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 显示申请
        for application in applications:
            app_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding="15")
            app_frame.pack(fill="x", pady=5)

            # 申请ID和时间
            header_frame = ttk.Frame(app_frame)
            header_frame.pack(fill="x", pady=(0, 10))

            ttk.Label(header_frame, text=f"申请ID: {application['application_id']}",
                      font=("Arial", 11, "bold")).pack(side="left")
            ttk.Label(header_frame, text=f"{application['apply_time']}",
                      font=("Arial", 10)).pack(side="right")

            # 申请信息
            info_frame = ttk.Frame(app_frame)
            info_frame.pack(fill="x", pady=(0, 10))

            ttk.Label(info_frame, text=f"商家: {application['merchant']}").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"商品名称: {application['product_name']}").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"价格: ¥{application['price']}").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"类别: {application['category']}").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"库存: {application['stock']}").pack(anchor="w", pady=2)
            ttk.Label(info_frame, text=f"描述: {application['description']}",
                      wraplength=500).pack(anchor="w", pady=2)

            # 审核按钮
            button_frame = ttk.Frame(app_frame)
            button_frame.pack(anchor="e")

            ttk.Button(button_frame, text="通过",
                       command=lambda app=application: self.approve_application(app)).pack(side="left", padx=5)
            ttk.Button(button_frame, text="拒绝",
                       command=lambda app=application: self.reject_application(app)).pack(side="left")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def approve_application(self, application):
        """通过申请"""
        if self.system.approve_application(application["application_id"]):
            messagebox.showinfo("成功", "申请已通过！")
            self.review_applications()
        else:
            messagebox.showerror("错误", "操作失败！")

    def reject_application(self, application):
        """拒绝申请"""
        if self.system.reject_application(application["application_id"]):
            messagebox.showinfo("成功", "申请已拒绝！")
            self.review_applications()
        else:
            messagebox.showerror("错误", "操作失败！")

    def admin_search_products(self):
        """管理员搜索商品"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="商品管理", style="Title.TLabel").pack(side="left")

        # 搜索区域
        search_frame = ttk.Frame(self.content_frame)
        search_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(search_frame, text="关键词:").pack(side="left")
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.pack(side="left", padx=5)

        def perform_search():
            query = search_entry.get()
            results = self.system.search_products(query)
            display_results(results)

        ttk.Button(search_frame, text="搜索", command=perform_search).pack(side="left", padx=5)

        # 结果显示区域
        self.results_container = ttk.Frame(self.content_frame)
        self.results_container.pack(fill="both", expand=True)

        def display_results(products):
            # 清空之前的结果
            for widget in self.results_container.winfo_children():
                widget.destroy()

            if not products:
                ttk.Label(self.results_container, text="未找到相关商品",
                          font=("Arial", 12)).pack(pady=50)
                return

            # 创建表格
            tree_frame = ttk.Frame(self.results_container)
            tree_frame.pack(fill="both", expand=True)

            tree = ttk.Treeview(tree_frame, columns=("name", "price", "category", "merchant", "status"),
                                show="headings", height=15)
            tree.heading("name", text="商品名")
            tree.heading("price", text="价格")
            tree.heading("category", text="类别")
            tree.heading("merchant", text="商家")
            tree.heading("status", text="状态")

            tree.column("name", width=200)
            tree.column("price", width=100, anchor="center")
            tree.column("category", width=100, anchor="center")
            tree.column("merchant", width=120, anchor="center")
            tree.column("status", width=100, anchor="center")

            for product in products:
                status = "已上架" if product.get("approved", False) else "待审核"
                tree.insert("", "end", values=(
                    product["name"],
                    f"¥{product['price']}",
                    product["category"],
                    product["merchant"],
                    status
                ), tags=(product["product_id"],))

            tree.pack(side="left", fill="both", expand=True)

            # 滚动条
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

        # 绑定回车键
        search_entry.bind('<Return>', lambda event: perform_search())

    def view_all_reviews(self):
        """查看所有商品评价"""
        self.clear_content()

        # 标题
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill="x", pady=(0, 15))
        ttk.Label(header_frame, text="所有商品评价", style="Title.TLabel").pack(side="left")

        # 获取评价数据
        reviews = self.system.get_all_reviews()
        if not reviews:
            ttk.Label(self.content_frame, text="暂无评价", font=("Arial", 12)).pack(pady=50)
            return

        # 创建评价列表
        canvas_frame = ttk.Frame(self.content_frame)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 显示评价
        for review in reviews:
            review_frame = ttk.Frame(scrollable_frame, style="Card.TFrame", padding="15")
            review_frame.pack(fill="x", pady=5)

            # 商品名称和商家
            header_frame = ttk.Frame(review_frame)
            header_frame.pack(fill="x", pady=(0, 5))
            ttk.Label(header_frame, text=f"商品: {review['product_name']}",
                      font=("Arial", 11, "bold")).pack(side="left")
            ttk.Label(header_frame, text=f"商家: {review['merchant']}",
                      font=("Arial", 10)).pack(side="right")

            # 评分
            rating_text = "★" * review['rating'] + "☆" * (5 - review['rating'])
            ttk.Label(review_frame, text=f"评分: {rating_text}").pack(anchor="w", pady=2)

            # 评论内容
            ttk.Label(review_frame, text=f"评论: {review['comment']}",
                      wraplength=500).pack(anchor="w", pady=2)

            # 用户信息和时间
            ttk.Label(review_frame, text=f"用户: {review['user']} - {review['review_time']}",
                      font=("Arial", 9)).pack(anchor="w", pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def login(self):
        """登录"""
        # 检查控件是否存在
        try:
            username = self.username_entry.get()
            password = self.password_entry.get()
        except tk.TclError:
            # 控件已被销毁，重新创建登录界面
            self.create_login_frame()
            return

        user_type = self.user_type_var.get()

        if not username or not password:
            messagebox.showerror("错误", "请输入用户名和密码！")
            return

        if self.system.login(username, password, user_type):
            self.current_user = username
            self.user_type = user_type

            if user_type == "user":
                self.create_user_dashboard()
            elif user_type == "merchant":
                self.create_merchant_dashboard()
            elif user_type == "admin":
                self.create_admin_dashboard()
        else:
            messagebox.showerror("错误", "用户名或密码错误！")

    def logout(self):
        """退出登录"""
        self.current_user = None
        self.user_type = None
        self.create_login_frame()

    def clear_frame(self):
        """清空窗口"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def clear_content(self):
        """清空内容区域"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def run(self):
        """运行应用"""
        self.root.mainloop()
