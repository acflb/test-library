import tkinter as tk

a = tk.Tk()

a.title('启动')
a1 = a.maxsize()
k, g = a1

a.geometry(f'{int(k*0.5)}x{int(g*0.5)}+{int(k*0.25)}+{int(g*0.25)}')
a.resizable(False, False)
tk.Label(a, text='账号:', font=('黑体', 26)).place(x=50, y=100)
tk.Label(a, text='密码:', font=('黑体', 26)).place(x=50, y=200)

a.mainloop()
