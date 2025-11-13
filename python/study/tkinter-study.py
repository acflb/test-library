# 1. 看到的程序界面就是GUI；tkinter优点：简单、易上手、跨平台
# 注：文件名不要和库名一致，python的导入系统会首先查找当前目录的‘tkinter’，并将其作为模块导入，而不是去加载python安装时自带的那个真正的tkinter库文件


import os
import tkinter as tk  # 添加别名tk


# 1. 创建窗口
a1 = tk.Tk()

# 2. 设置窗口标题
a1.title('启动')

# 3. 获取用户分辨率
a2 = a1.maxsize()
k, g = a2

# 4. 设置窗口大小(宽x高+x轴偏移+y轴偏移)
# a1.geometry('300x300+600+600')
a1.geometry(f'{int(k * 0.5)}x{int(g * 0.5)}+{int(k*0.25)}+{int(g*0.25)}')

# 5. 设置窗口锁定缩放; 宽 和 高的拉伸是否开启，true可以拉伸，false不可以
a1.resizable(True, False)


# 6.1.0 获取当前脚本文件所在的目录
# __file__ 是一个指向当前脚本的特殊变量
script_dir = os.path.dirname(os.path.abspath(__file__))

# 6.1.1将脚本目录和图标文件名组合成一个完整的路径
icon_path = os.path.join(script_dir, 'test.ico')

# 6.1.2也可以使用转义字符---`r`解析绝对路径
# a1.iconbitmap(r'C:\Users\xxxxx\test.ico')

# 6.2 设置窗口图标
a1.iconbitmap(icon_path)


# 7. 设置窗口背景颜色(颜色英文 或者 颜色编码)
# a1.configure(bg='yellow')
a1.configure(bg='#000')

# 8. 设置窗口透明度(0~1)
a1.attributes('-alpha', 0.5)

# 9. 窗口置顶
a1.attributes('-topmost', True)

# 10. 窗口关闭时执行函数


def close():
    print('closed')
    # 销毁窗口
    a1.destroy()


# 传递函数引用，不加括号；当用户点击关闭按钮时才执行;加括号执行一次
a1.protocol('WM_DELETE_WINDOW', close)

# 开启窗口/主循环；所有窗口信息在窗口开启前执行
a1.mainloop()
