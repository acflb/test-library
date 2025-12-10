import tkinter as tk

# 继承tk的Frame类的所有特性和方法；tk.Frame本质是一个容器，用于组织和布局其它小组件（例如：按钮、标签）


class Counter(tk.Frame):
    # 'def __init__' 构造函数.当创建一个类的新(实例/对象)时,这个方法自动调用,用于初始化该对象
    # '(self,master)'self
    def __init__(self, master):  # 添加 master 参数

        super().__init__(master, bg='#251f1a')  # 调用父类初始化

        # 调用tkinter上的pack布局方法，fill:填充布局；expand:当有可用空间时，也随之扩大；padx:x方向两侧填充10px；pady：y方向两侧填充10px
        self.pack(fill='both', expand=True, padx=4, pady=4)

        # 配置网格权重，使按钮能自适应大小
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        self.c = tk.StringVar(value='0')

        # 显示区域
        self.display = tk.Entry(
            self,
            textvariable=self.c,
            font=('Arial', 28, 'bold'),  # 大字体
            bg='#251f1a',
            fg='#ffffff',  # 白色文字
            bd=0,  # 无边框
            justify='right',  # 右对齐
            # 平面样式；‘relief’设置边框样式和三维外观：‘flat’：平坦的；‘sunken’：凹陷的；‘raised’：凸起的；‘groove’：凹槽；‘ridge’：凸槽
            relief='flat',
            insertwidth=0
        )

        self.master.title('计算器')
        self.master.geometry('328x500')
        self.master.configure(bg='#251f1a')

        self.a = 0
        self.b = 0
        self.symbol = None
        self.cache = 1

        # sticky="nsew" = 拉伸填充;columnspan=4 = 这个元素横跨4列（显示屏要铺满）
        self.display.grid(row=0, column=0, columnspan=4,
                          sticky="nsew", padx=8, pady=5)

        def result():
            self.b = self.display.get()
            if self.symbol == '+':
                self.c.set(str(int(self.a) + int(self.b)))
                self.symbol = None
            elif self.symbol == '-':
                self.c.set(str(int(self.a) - int(self.b)))
                self.symbol = None
            elif self.symbol == 'x':
                self.c.set(str(int(self.a) * int(self.b)))
                self.symbol = None
            elif self.symbol == '/':
                self.c.set(str(int(self.a) / int(self.b)))
                self.symbol = None
            self.cache = 1

        def change_symbol(a):
            self.symbol = a
            self.cache = 1
            self.a = self.display.get()

        def click(a):
            if self.cache:
                # 清空显示，然后插入数字
                self.display.delete(0, tk.END)
                self.cache = 0
            # self.c.set(str(a))
            if self.display.get() == '0':
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, a)
            else:
                self.display.insert(tk.END, a)

        def clear():
            self.a = 0
            self.b = 0
            self.c.set('0')
            self.symbol = None
            self.cache = 1

        def deleteMy():
            if len(self.display.get()) > 0:
                self.display.delete(len(self.display.get()) - 1)
                if len(self.display.get()) == 0:
                    self.display.insert(tk.END, '0')
                    self.cache = 1

        # 按钮
        tk.Button(self, command=deleteMy, text="delete").grid(
            row=1, column=3, sticky="nsew")
        tk.Button(self, command=clear, text="clear").grid(
            row=1, column=0, columnspan=3, sticky="nsew")

        # 第二行：7 8 9 ÷
        tk.Button(self, command=lambda: click(7),
                  text="7").grid(row=2, column=0, sticky="nsew")
        tk.Button(self, command=lambda: click(8),
                  text="8").grid(row=2, column=1, sticky="nsew")
        tk.Button(self, command=lambda: click(9),
                  text="9").grid(row=2, column=2, sticky="nsew")
        tk.Button(self, command=lambda: change_symbol('+'),
                  text="+").grid(row=2, column=3, sticky="nsew")

        # 第三行
        tk.Button(self, command=lambda: click(4),
                  text="4").grid(row=3, column=0, sticky="nsew")
        tk.Button(self, command=lambda: click(5),
                  text="5").grid(row=3, column=1, sticky="nsew")
        tk.Button(self, command=lambda: click(6),
                  text="6").grid(row=3, column=2, sticky="nsew")
        tk.Button(self, command=lambda: change_symbol(
            '-'), text="-").grid(row=3, column=3, sticky="nsew")

        # 第四行
        tk.Button(self, command=lambda: click(1),
                  text="1").grid(row=4, column=0, sticky="nsew")
        tk.Button(self, command=lambda: click(2),
                  text="2").grid(row=4, column=1, sticky="nsew")
        tk.Button(self, command=lambda: click(3),
                  text="3").grid(row=4, column=2, sticky="nsew")
        tk.Button(self, command=lambda: change_symbol(
            'x'), text="x").grid(row=4, column=3, sticky="nsew")

        # 第五行
        tk.Button(self, command=lambda: click(0),
                  text="0").grid(row=5, column=0, sticky="nsew")
        tk.Button(self, text=".").grid(row=5, column=1, sticky="nsew")
        tk.Button(self, command=lambda: change_symbol(
            '/'), text="/").grid(row=5, column=2, sticky="nsew")
        tk.Button(self, command=lambda: result(),
                  text="=").grid(row=5, column=3, sticky="nsew")


# 创建根窗口，所有其他组件都将放置在这个窗口内
root = tk.Tk()

# 实例化Counter类的构造函数(def __init__(self,master))；
# root作为作为参数传递给‘Counter’的构造函数，因此root成为了Counter实例的‘master’；
myapp = Counter(root)

# 启动事件循环
root.mainloop()
