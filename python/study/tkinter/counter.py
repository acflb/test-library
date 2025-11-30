import tkinter as tk


class Counter(tk.Frame):  # 继承 tk.Frame
    # '__init__'是 Python 类的构造函数（初始化方法），用于创建对象时自动执行初始化操作
    def __init__(self, master):  # 添加 master 参数
        super().__init__(master)  # 调用父类初始化
        self.pack()  # 将 Frame 添加到父窗口

        # 显示区域
        self.display = tk.Entry(self)

        self.master.geometry('340x500')
        self.a = 0
        self.b = 0

        # sticky="nsew" = 拉伸填充;columnspan=4 = 这个元素横跨4列（显示屏要铺满）
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")

        def divide(a, b):
            return a/b

        def subtract(a, b):
            return a - b

        def ride(a, b):
            return a * b

        def add(a, b):
            return a + b

        # 按钮
        # 第二行：7 8 9 ÷
        tk.Button(self, text="7").grid(row=1, column=0)
        tk.Button(self, text="8").grid(row=1, column=1)
        tk.Button(self, text="9").grid(row=1, column=2)
        tk.Button(self, command=add(self.a, self.b),
                  text="+").grid(row=1, column=3)

        # 第三行：7 8 9 ÷
        tk.Button(self, text="4").grid(row=2, column=0)
        tk.Button(self, text="5").grid(row=2, column=1)
        tk.Button(self, text="6").grid(row=2, column=2)
        tk.Button(self, text="-").grid(row=2, column=3)

        # 第四行：7 8 9 ÷
        tk.Button(self, text="1").grid(row=3, column=0)
        tk.Button(self, text="2").grid(row=3, column=1)
        tk.Button(self, text="3").grid(row=3, column=2)
        tk.Button(self, text="x").grid(row=3, column=3)

        # 第五行：7 8 9 ÷
        tk.Button(self, text="0").grid(row=4, column=0)
        tk.Button(self, text=".").grid(row=4, column=1)
        tk.Button(self, text="/").grid(row=4, column=2)
        tk.Button(self, text="=").grid(row=4, column=3)


# 1. 创建主窗口
root = tk.Tk()

# 2. 创建 Counter 对象（自动执行 __init__）
myapp = Counter(root)
# 相当于：
# - Counter.__init__(myapp, root)
# - super().__init__(root)  → myapp 是 Frame，属于 root
# - self.pack()  → 将 myapp 显示在 root 中
# - 创建所有按钮

# 3. 启动事件循环
root.mainloop()
