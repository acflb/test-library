import pymupdf
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import io
import os


class PDFCropTool:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF裁剪工具")
        self.root.geometry("1200x800")

        self.pdf_doc = None
        self.current_page = 0
        self.total_pages = 0
        self.page_image = None
        self.photo = None

        # 裁剪线的位置 (比例: 0-1)asdf
        self.v_lines = []  # 垂直线位置 - 初始为空
        self.h_lines = [0.5]  # 水平线位置 - 初始只有一条水平线

        # 拖动状态
        self.dragging = None  # ('v', index) or ('h', index)
        self.drag_threshold = 10  # 拖动检测阈值(像素)

        self.setup_ui()
        self.setup_drag_drop()

    def setup_ui(self):
        # 顶部控制栏
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        tk.Button(control_frame, text="📁 打开PDF", command=self.open_pdf).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(control_frame, text="◀ 上一页", command=self.prev_page).pack(
            side=tk.LEFT, padx=5
        )

        self.page_label = tk.Label(control_frame, text="0/0页")
        self.page_label.pack(side=tk.LEFT, padx=10)

        tk.Button(control_frame, text="下一页 ▶", command=self.next_page).pack(
            side=tk.LEFT, padx=5
        )

        tk.Button(
            control_frame, text="➕ 添加垂直线", command=self.add_vertical_line
        ).pack(side=tk.LEFT, padx=15)
        tk.Button(
            control_frame, text="➕ 添加水平线", command=self.add_horizontal_line
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="🗑️ 清除所有线", command=self.clear_lines).pack(
            side=tk.LEFT, padx=15
        )

        tk.Button(
            control_frame,
            text="✂️ 执行裁剪",
            command=self.crop_pdf,
            bg="#4CAF50",
            fg="white",
        ).pack(side=tk.RIGHT, padx=5)

        # 画布区域(支持拖拽提示)
        canvas_frame = tk.Frame(self.root, bg="gray")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(canvas_frame, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 拖拽提示标签
        self.drop_hint = tk.Label(
            self.canvas,
            text="📄 拖动PDF文件到这里\n或点击'打开PDF'按钮",
            font=("Arial", 16),
            bg="white",
            fg="gray",
        )
        self.drop_hint.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # 提示标签
        self.hint_label = tk.Label(
            self.root,
            text="💡 支持从微信/文件夹直接拖拽PDF | 拖动红色虚线调整裁剪位置",
            bg="#E8F5E9",
            anchor=tk.W,
            padx=10,
        )
        self.hint_label.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_drag_drop(self):
        """设置拖拽功能"""
        # 注册拖拽目标
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.on_drop)

        # 拖拽悬停效果
        self.root.dnd_bind("<<DragEnter>>", self.on_drag_enter)
        self.root.dnd_bind("<<DragLeave>>", self.on_drag_leave)

    def on_drag_enter(self, event):
        """鼠标拖拽进入窗口"""
        self.canvas.config(bg="#E8F5E9")  # 浅绿色提示
        if self.drop_hint.winfo_exists():
            self.drop_hint.config(
                text="📥 松开鼠标即可打开", fg="#4CAF50", font=("Arial", 18, "bold")
            )

    def on_drag_leave(self, event):
        """鼠标拖拽离开窗口"""
        self.canvas.config(bg="white")
        if self.drop_hint.winfo_exists():
            self.drop_hint.config(
                text="📄 拖动PDF文件到这里\n或点击'打开PDF'按钮",
                fg="gray",
                font=("Arial", 16),
            )

    def on_drop(self, event):
        """处理拖拽放下事件"""
        self.canvas.config(bg="white")

        # 获取拖拽的文件路径
        files = self.root.tk.splitlist(event.data)

        if not files:
            return

        file_path = files[0].strip("{}")  # 去掉可能的大括号

        # 检查是否是 PDF 文件
        if not file_path.lower().endswith(".pdf"):
            messagebox.showwarning("警告", "请拖入 PDF 文件喵!")
            return

        # 检查文件是否存在
        if not os.path.exists(file_path):
            messagebox.showerror("错误", "文件不存在喵!")
            return

        # 打开 PDF
        self.load_pdf(file_path)

    def open_pdf(self):
        """通过对话框打开PDF"""
        filename = filedialog.askopenfilename(
            title="选择PDF文件", filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filename:
            self.load_pdf(filename)

    def load_pdf(self, filename):
        """加载PDF文件"""
        try:
            # 关闭之前打开的PDF
            if self.pdf_doc:
                self.pdf_doc.close()

            self.pdf_doc = pymupdf.open(filename)
            self.total_pages = len(self.pdf_doc)
            self.current_page = 0
            self.pdf_filename = filename

            # 隐藏拖拽提示
            if self.drop_hint.winfo_exists():
                self.drop_hint.place_forget()

            self.render_page()

            # 显示成功消息
            file_name = os.path.basename(filename)
            self.hint_label.config(
                text=f"✅ 已打开: {file_name} | 共 {self.total_pages} 页"
            )

        except Exception as e:
            messagebox.showerror("错误", f"无法打开PDF文件:\n{str(e)}")

    def render_page(self):
        if not self.pdf_doc:
            return

        page = self.pdf_doc[self.current_page]

        # 渲染PDF页面为图像
        zoom = 2  # 提高清晰度
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)

        # 转换为PIL Image
        img_data = pix.tobytes("png")
        self.page_image = Image.open(io.BytesIO(img_data))

        # 调整图像大小以适应画布
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width > 1 and canvas_height > 1:
            img_ratio = self.page_image.width / self.page_image.height
            canvas_ratio = canvas_width / canvas_height

            if img_ratio > canvas_ratio:
                new_width = canvas_width - 40
                new_height = int(new_width / img_ratio)
            else:
                new_height = canvas_height - 40
                new_width = int(new_height * img_ratio)

            self.page_image = self.page_image.resize(
                (new_width, new_height), Image.Resampling.LANCZOS
            )

        self.photo = ImageTk.PhotoImage(self.page_image)

        # 更新画布
        self.canvas.delete("all")
        self.img_x = (self.canvas.winfo_width() - self.page_image.width) // 2
        self.img_y = (self.canvas.winfo_height() - self.page_image.height) // 2
        self.canvas.create_image(self.img_x, self.img_y, anchor=tk.NW, image=self.photo)

        # 绘制裁剪线
        self.draw_crop_lines()

        # 更新页码
        self.page_label.config(text=f"{self.current_page + 1}/{self.total_pages}页")

    def draw_crop_lines(self):
        if not self.page_image:
            return

        img_w = self.page_image.width
        img_h = self.page_image.height

        # 绘制垂直线
        for i, pos in enumerate(self.v_lines):
            x = self.img_x + int(pos * img_w)
            self.canvas.create_line(
                x,
                self.img_y,
                x,
                self.img_y + img_h,
                fill="red",
                width=2,
                dash=(5, 5),
                tags=f"vline_{i}",
            )

        # 绘制水平线
        for i, pos in enumerate(self.h_lines):
            y = self.img_y + int(pos * img_h)
            self.canvas.create_line(
                self.img_x,
                y,
                self.img_x + img_w,
                y,
                fill="red",
                width=2,
                dash=(5, 5),
                tags=f"hline_{i}",
            )

    def get_line_at_pos(self, x, y):
        """检测鼠标是否在某条线附近"""
        if not self.page_image:
            return None

        img_w = self.page_image.width
        img_h = self.page_image.height

        # 检测垂直线
        for i, pos in enumerate(self.v_lines):
            line_x = self.img_x + int(pos * img_w)
            if abs(x - line_x) < self.drag_threshold:
                return ("v", i)

        # 检测水平线
        for i, pos in enumerate(self.h_lines):
            line_y = self.img_y + int(pos * img_h)
            if abs(y - line_y) < self.drag_threshold:
                return ("h", i)

        return None

    def on_mouse_down(self, event):
        self.dragging = self.get_line_at_pos(event.x, event.y)

    def on_mouse_drag(self, event):
        if not self.dragging or not self.page_image:
            return

        line_type, line_idx = self.dragging
        img_w = self.page_image.width
        img_h = self.page_image.height

        if line_type == "v":
            # 垂直线：检查是否拖拽到图像外
            if event.x < self.img_x or event.x > self.img_x + img_w:
                # 拖拽到图像外，删除这条垂直线
                if 0 <= line_idx < len(self.v_lines):
                    self.v_lines.pop(line_idx)
                    self.dragging = None  # 停止拖拽
                    self.render_page()
                    self.canvas.config(cursor="crosshair")
                    return

            # 更新垂直线位置
            new_pos = (event.x - self.img_x) / img_w
            new_pos = max(0.01, min(0.99, new_pos))  # 限制在图像范围内
            self.v_lines[line_idx] = new_pos
        else:
            # 水平线：检查是否拖拽到图像外
            if event.y < self.img_y or event.y > self.img_y + img_h:
                # 拖拽到图像外，删除这条水平线
                if 0 <= line_idx < len(self.h_lines):
                    self.h_lines.pop(line_idx)
                    self.dragging = None  # 停止拖拽
                    self.render_page()
                    self.canvas.config(cursor="crosshair")
                    return

            # 更新水平线位置
            new_pos = (event.y - self.img_y) / img_h
            new_pos = max(0.01, min(0.99, new_pos))
            self.h_lines[line_idx] = new_pos

        self.render_page()

    def on_mouse_up(self, event):
        self.dragging = None

    def on_mouse_move(self, event):
        """改变鼠标样式"""
        line = self.get_line_at_pos(event.x, event.y)
        if line:
            line_type = line[0]
            if line_type == "v":
                self.canvas.config(cursor="sb_h_double_arrow")
            else:
                self.canvas.config(cursor="sb_v_double_arrow")
        else:
            self.canvas.config(cursor="crosshair")

    def add_vertical_line(self):
        self.v_lines.append(0.5)
        self.v_lines.sort()
        self.render_page()

    def add_horizontal_line(self):
        self.h_lines.append(0.5)
        self.h_lines.sort()
        self.render_page()

    def clear_lines(self):
        self.v_lines = []
        self.h_lines = []
        self.render_page()

    def prev_page(self):
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def next_page(self):
        if self.pdf_doc and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.render_page()

    def crop_pdf(self):
        if not self.pdf_doc:
            messagebox.showwarning("警告", "请先打开PDF文件!")
            return

        if not self.v_lines and not self.h_lines:
            messagebox.showwarning("警告", "请至少添加一条裁剪线!")
            return

        # 询问保存位置
        default_name = os.path.splitext(os.path.basename(self.pdf_filename))[0]
        output_file = filedialog.asksaveasfilename(
            title="保存裁剪后的PDF",
            defaultextension=".pdf",
            initialfile=f"{default_name}_裁剪.pdf",
            filetypes=[("PDF文件", "*.pdf")],
        )

        if not output_file:
            return

        try:
            doc = pymupdf.open()

            for spage in self.pdf_doc:
                r = spage.rect
                d = pymupdf.Rect(spage.cropbox_position, spage.cropbox_position)

                # 生成裁剪矩形列表
                v_positions = [0] + sorted(self.v_lines) + [1]
                h_positions = [0] + sorted(self.h_lines) + [1]

                for i in range(len(h_positions) - 1):
                    for j in range(len(v_positions) - 1):
                        # 计算矩形区域
                        x0 = r.x0 + v_positions[j] * r.width
                        y0 = r.y0 + h_positions[i] * r.height
                        x1 = r.x0 + v_positions[j + 1] * r.width
                        y1 = r.y0 + h_positions[i + 1] * r.height

                        rx = pymupdf.Rect(x0, y0, x1, y1) + d

                        page = doc.new_page(-1, width=rx.width, height=rx.height)
                        page.show_pdf_page(
                            page.rect, self.pdf_doc, spage.number, clip=rx
                        )

            doc.save(output_file, garbage=3, deflate=True)
            messagebox.showinfo("成功", f"PDF已成功裁剪并保存!\n共生成 {len(doc)} 页")

        except Exception as e:
            messagebox.showerror("错误", f"裁剪失败:\n{str(e)}")


if __name__ == "__main__":
    root = TkinterDnD.Tk()  # 使用支持拖拽的Tk
    app = PDFCropTool(root)
    root.mainloop()
