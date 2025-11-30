import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import END

win = tk.Tk()
win.title('菜单')
win_size = win.maxsize()
w, h = win_size
win.geometry(f'{int(w*0.3)}x{int(h*0.4)}+{int(w*0.35)}+{int(h*0.3)}')
win.resizable(True, False)

# 创建列表框
tk.Label(win, font=('楷体', 16), text='员工列表: ', fg='green').place(x=10, y=10)
list = tk.Listbox(win, font=('楷体', 16), width=40, height=20)
# 注:链式调用时,place返回的是'none',而不是'listbox'对象
list.place(x=10, y=36)


# 创建主菜单
master_menu = tk.Menu(win)

# 设置菜单名
master_menu.add_cascade(label='name1')
master_menu.add_cascade(label='name2')

# 添加函数


def add(master_menu):
    child_menu = tk.Toplevel()
    child_menu.title('子菜单')
    child_menu.geometry('300x300+400+400')
    child_menu.resizable(False, False)

    # 设置顶层窗口的焦点
    child_menu.focus_set()

    tk.Label(child_menu, text='城市: ', font=('楷体', 16)).place(x=10, y=10)
    tk.Label(child_menu, text='性别: ', font=('楷体', 16)).place(x=10, y=50)
    tk.Label(child_menu, text='爱好: ', font=('楷体', 16)).place(x=10, y=80)

    child_choose = tk.StringVar()
    child_radio = tk.StringVar(value='男')
    child_nums = ['北京', '上海', '深圳']

    # 创建下拉列表(组合框)
    child_lower = Combobox(child_menu, width=10, textvariable=child_choose,
                           values=child_nums, font=('楷体', 16))
    child_lower.place(x=80, y=10)

    # 设置默认值
    # 注:设置默认值属性和'readonly'属性冲突,可以在设置后再改为'readonly'
    # child_lower.set(child_nums[0])
    # child_lower.current(0)
    # 给GUI一点时间渲染
    child_lower.after(10, lambda: child_lower.current(0))
    child_lower.config(state='readonly')

    def click():
        print(child_radio.get(), child_lower.get())
        print(checkbox.get(), checkbox1.get())
        love = f'爱好: {"足球" if checkbox.get() else ""}{""if checkbox.get() or checkbox1.get() else "未选择"}{"、"if checkbox.get() and checkbox1.get() else ""}{"跑步" if checkbox1.get() else ""}'
        list.insert(
            END, f'城市: {child_lower.get()};性别: {child_radio.get()};{love}')

    # 创建单选框
        # 注：这里的value值为英文时（male,female），会出现两个都选中的情况
    tk.Radiobutton(child_menu,  font=('楷体', 16),variable=child_radio, text='男', value='男').place(x=80, y=50)
    tk.Radiobutton(child_menu,  font=('楷体', 16),variable=child_radio, text='女', value='女').place(x=150, y=50)

    # 创建多选框
    # 整数变量
    checkbox = tk.IntVar()
    checkbox1 = tk.IntVar()
    tk.Checkbutton(child_menu,  font=('楷体', 16),
                   variable=checkbox, text='足球', onvalue=1, offvalue=0).place(x=80, y=80)
    tk.Checkbutton(child_menu,  font=('楷体', 16),
                   variable=checkbox1, text='跑步', onvalue=1, offvalue=0).place(x=150, y=80)

    tk.Button(child_menu, command=click, font=('楷体', 16),
              width=5, height=1, text='添加').place(x=10, y=120)

    # master_menu.add_cascade(label='name')


# 创建下级菜单
# 注: tearoff默认参数为'1',开启分割符
subordinate = tk.Menu(master_menu, tearoff=0)
subordinate.add_command(label='add', command=lambda: add(master_menu))
subordinate.add_command(label='lower2', command='')
# 绑定到主菜单
master_menu.add_cascade(label='name3', menu=subordinate)


# 开启菜单栏
win.config(menu=master_menu)

win.mainloop()
