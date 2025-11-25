import os
import tkinter as tk
from tkinter import messagebox

a = tk.Tk()

a.title('启动')
a1 = a.maxsize()
k, g = a1

# 注：图片引入时，当前工作路径和图标路径需一致
if os.path.exists('test.ico'):
    a.iconbitmap('test.ico')
else:
    print(f"当前工作路径：{os.getcwd()}")
    print("图标文件不存在")

a.geometry(f'{int(k*0.25)}x{int(g*0.5)}+{int(k*0.375)}+{int(g*0.25)}')
a.resizable(False, False)
tk.Label(a, text='账号:', font=('黑体', 26)).place(x=100, y=100)
tk.Label(a, text='密码:', font=('黑体', 26)).place(x=100, y=200)

# 创建字符串变量
# set----python的集合类型（无序、不重复、可遍历）
s1 = tk.StringVar()
s1.set('请输入账号')  # 提示文本
s2 = tk.StringVar()
s2.set('请输入密码')


# 1. 输入框组件 Entry
tk.Entry(a, textvariable=s1, width=15, font=('黑体', 26)).place(x=200, y=102)
tk.Entry(a, textvariable=s2, width=15, font=('黑体', 26)).place(x=200, y=202)

# 2. 按钮组件 Button


def register():
    print(f'点击啦 {s1.get()}', s2.get())
    # 注：‘in’判断键值是否有一样的
    if s1.get() in dict and s2.get() == dict[s1.get()]:
        print('登录成功')
        messagebox.showinfo('成功', '登录成功')
    else:
        # messagebox.showerror('错误', '账号或者密码错误')
        # messagebox.showwarning('警告', '账号或者密码错误')
        # 选择弹窗
        d1 = messagebox.askokcancel('错误', '账号或者密码错误')
        if d1:
            print('True')
        else:
            print('False')
        print('登录失败')


tk.Button(a, text='登录', command=register, font=('黑体', 26)).place(x=150, y=302)

# 3. 二次拦截


def close():
    d1 = messagebox.askokcancel('确认', '是否关闭窗口')
    if d1:
        a.destroy()
    else:
        pass


a.protocol('WM_DELETE_WINDOW', close)

# 4. 顶层窗口
dict = {}
a2 = None

s3 = tk.StringVar()
s3.set('')  # 提示文本
s4 = tk.StringVar()
s4.set('')


def login_affirm(a2):
    # 注：这里使用‘global’关键字声明使用全局变量‘dict’，若不声明会创建新局部变量‘dict’
    global dict
    if s3.get() in dict:
        messagebox.showerror('错误', '账号已存在')
    else:
        dict[s3.get()] = s4.get()
        messagebox.showinfo('成功', '注册成功')
        a2.destroy()
    print(dict)


def login():
    a2 = tk.Toplevel()
    a2.title('注册')
    a3 = a2.maxsize()
    k, g = a3
    a2.geometry(f'{int(k*0.2)}x{int(g*0.4)}+{int(k*0.4)}+{int(g*0.3)}')
    a2.resizable(False, False)
    tk.Label(a2, text='账号:', font=('楷体', 20)).grid(row=1, column=1)
    tk.Label(a2, text='密码:', font=('楷体', 20)).grid(row=2, column=1)
    # state为'disabled'或者'readonly'时为只读
    # tk.Entry(a2, state='disabled', width=10,font=('楷体', 20)).grid(row=1, column=2)
    # tk.Entry(a2, state='readonly', width=10,font=('楷体', 20)).grid(row=2, column=2)
    tk.Entry(a2, textvariable=s3, width=10,
             font=('楷体', 20)).grid(row=1, column=2)
    tk.Entry(a2, textvariable=s4, width=10,
             font=('楷体', 20)).grid(row=2, column=2)
    # 注：不使用lambda时，会立即执行函数，而不是等待按钮点击时调用
    # 解析：command函数执行时，将对应函数执行一次后的返回值赋给command
    # 注：函数名指向函数体本身，函数指向函数执行的结果
    tk.Button(a2, command=lambda: login_affirm(a2), text='确认注册', font=(
        '楷体', 20)).place(x=150, y=100)


tk.Button(a, text='注册', command=login, font=('黑体', 26)).place(x=350, y=302)


a.mainloop()
