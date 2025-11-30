# 设置库别名
import sys
import os
import tkinter as tk

# 窗口创建
w1 = tk.Tk()

# 获取用户分辨率(宽,高)
w2 = w1.maxsize()
w, h = w2

# 窗口大小(宽x高+x轴偏移+y轴偏移)
# w1.geometry('300x300+600+600')
# 窗口居中
w1.geometry(f'{int(w * 0.5)}x{int(h * 0.5)}+{int(w*0.25)}+{int(h * 0.25)}')

# 窗口缩放是否允许(宽,高),默认`true`允许
w1.resizable(False, False)

# 窗口图标设置


def resource_path(relative_path):
    """
    获取资源的绝对路径，打包后使用临时目录，开发时使用原始路径
    """
    # hasattr函数：检查sys模块是否有_MEIPASS
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        # "__file__" 是一个特殊变量,指向当前脚本文件所在的目录
        # dirname返回路径中目录部分；abspath返回当前绝对路径
        base_path = os.path.dirname(os.path.abspath(__file__))

        # 将脚本目录和图标文件名组合成一个完整的路径
    return os.path.join(base_path, relative_path)


icon_path = resource_path('test.ico')

# 使用转义字符----'r'解析绝对路径
# w1.iconbitmap(r'C:\Users\xxxx\test.ico')

w1.iconbitmap(icon_path)

# 窗口背景色(也可设置为bg='blue')
w1.configure(bg='#000')

# 窗口透明度(0~1)
w1.attributes('-alpha', 0.5)

# 窗口置顶
w1.attributes('-topmost', True)

# 窗口关闭


def close():
    w1.destroy()


w1.protocol('WM_DELETE_WINDOW', close)  # (`close`加括号会默认执行一次)


# 标签组件
l1 = tk.Label(w1, text='ai', font=('黑体', 26), fg='white', bg='black')

# 填充布局 pack() 默认布局:默认字体水平居中
l1.pack()

# 自定义布局 place(),注意不要超过窗口范围
# l1.place(x=100, y=100)

# 网格布局 grid()
# l1.grid(row=1, column=1)
# l1 = tk.Label(w1, text='ai', font=('黑体', 26), fg='white', bg='black')
# l1.grid(row=2, column=2)

# 窗口开启
w1.mainloop()
