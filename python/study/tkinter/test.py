import tkinter as tk


class Counter(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='#2b2b2b')  # 深色背景
        self.pack(fill='both', expand=True, padx=10, pady=10)

        self.c = tk.StringVar(value='0')

        # 配置网格权重，使按钮能自适应大小
        for i in range(5):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # 显示区域 - 优化样式
        self.display = tk.Entry(
            self,
            textvariable=self.c,
            font=('Arial', 28, 'bold'),  # 大字体
            bg='#1a1a1a',  # 深灰背景
            fg='#ffffff',  # 白色文字
            bd=0,  # 无边框
            justify='right',  # 右对齐
            relief='flat',  # 平面样式
            insertbackground='#ffffff'  # 光标颜色
        )

        self.master.title('计算器')
        self.master.geometry('400x550')
        self.master.resizable(False, False)  # 禁止调整大小
        self.master.configure(bg='#2b2b2b')

        self.a = 0
        self.b = 0
        self.symbol = None
        self.cache = 1

        # 显示区域占据第一行，增加高度
        self.display.grid(row=0, column=0, columnspan=4,
                          sticky="nsew", padx=5, pady=5, ipady=20)

        def result():
            self.b = self.display.get()
            if self.symbol == '+':
                self.c.set(str(float(self.a) + float(self.b)))
                self.symbol = None
            elif self.symbol == '-':
                self.c.set(str(float(self.a) - float(self.b)))
                self.symbol = None
            elif self.symbol == 'x':
                self.c.set(str(float(self.a) * float(self.b)))
                self.symbol = None
            elif self.symbol == '/':
                self.c.set(str(float(self.a) / float(self.b)))
                self.symbol = None
            self.cache = 1

        def change_symbol(a):
            self.symbol = a
            self.cache = 1
            self.a = self.display.get()

        def click(a):
            if self.cache:
                self.display.delete(0, tk.END)
                self.cache = 0
            self.display.insert(tk.END, a)

        def clear():
            self.c.set('0')
            self.a = 0
            self.b = 0
            self.symbol = None
            self.cache = 1

        # 定义按钮样式
        num_style = {
            'font': ('Arial', 20, 'bold'),
            'bg': '#404040',
            'fg': '#ffffff',
            'bd': 0,
            'activebackground': '#505050',
            'activeforeground': '#ffffff',
            'relief': 'flat'
        }

        operator_style = {
            'font': ('Arial', 20, 'bold'),
            'bg': '#ff9500',
            'fg': '#ffffff',
            'bd': 0,
            'activebackground': '#ffb143',
            'activeforeground': '#ffffff',
            'relief': 'flat'
        }

        equal_style = {
            'font': ('Arial', 20, 'bold'),
            'bg': '#34c759',
            'fg': '#ffffff',
            'bd': 0,
            'activebackground': '#5dd879',
            'activeforeground': '#ffffff',
            'relief': 'flat'
        }

        clear_style = {
            'font': ('Arial', 20, 'bold'),
            'bg': '#d1d1d6',
            'fg': '#000000',
            'bd': 0,
            'activebackground': '#e5e5ea',
            'activeforeground': '#000000',
            'relief': 'flat'
        }

        # 第一行：C 按钮
        tk.Button(self, command=clear, text="C", **clear_style).grid(
            row=1, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: change_symbol('/'),
                  text="÷", **operator_style).grid(
            row=1, column=3, sticky="nsew", padx=2, pady=2)

        # 第二行：7 8 9 +
        tk.Button(self, command=lambda: click(7),
                  text="7", **num_style).grid(
            row=2, column=0, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: click(8),
                  text="8", **num_style).grid(
            row=2, column=1, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: click(9),
                  text="9", **num_style).grid(
            row=2, column=2, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: change_symbol('x'),
                  text="×", **operator_style).grid(
            row=2, column=3, sticky="nsew", padx=2, pady=2)

        # 第三行：4 5 6 -
        tk.Button(self, command=lambda: click(4),
                  text="4", **num_style).grid(
            row=3, column=0, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: click(5),
                  text="5", **num_style).grid(
            row=3, column=1, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: click(6),
                  text="6", **num_style).grid(
            row=3, column=2, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: change_symbol('-'),
                  text="−", **operator_style).grid(
            row=3, column=3, sticky="nsew", padx=2, pady=2)

        # 第四行：1 2 3 +
        tk.Button(self, command=lambda: click(1),
                  text="1", **num_style).grid(
            row=4, column=0, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: click(2),
                  text="2", **num_style).grid(
            row=4, column=1, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: click(3),
                  text="3", **num_style).grid(
            row=4, column=2, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: change_symbol('+'),
                  text="+", **operator_style).grid(
            row=4, column=3, sticky="nsew", padx=2, pady=2)

        # 第五行：0 . =
        tk.Button(self, command=lambda: click(0),
                  text="0", **num_style).grid(
            row=5, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=lambda: click('.'),
                  text=".", **num_style).grid(
            row=5, column=2, sticky="nsew", padx=2, pady=2)
        tk.Button(self, command=result,
                  text="=", **equal_style).grid(
            row=5, column=3, sticky="nsew", padx=2, pady=2)


root = tk.Tk()
myapp = Counter(root)
root.mainloop()
