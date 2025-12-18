import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QSlider,
                             QFileDialog, QGroupBox, QSpinBox, QComboBox,
                             QMessageBox, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QFont
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PIL import Image

import os


class ImageProcessor:
    """图像处理核心类 - 就像猫咪的利爪喵~"""

    @staticmethod
    def preprocess_image(image, threshold_value=127, blur_size=3,
                         sharpen_strength=1.0, denoise_strength=5):
        """
        预处理图像 - 让试题变得黑白分明喵!

        参数说明(就像猫咪调整狩猎姿势):
        - threshold_value: 二值化阈值 (越小保留越多细节)
        - blur_size: 降噪强度 (奇数, 越大越模糊)
        - sharpen_strength: 锐化强度 (0-2之间)
        - denoise_strength: 去噪强度 (5-20之间)
        """

        # 1. 转换为灰度图 - 简化信息喵
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # 2. 降噪处理 - 去除毛躁喵
        if blur_size > 1:
            gray = cv2.GaussianBlur(gray, (blur_size, blur_size), 0)

        # 3. 自适应阈值二值化 - 核心魔法喵!
        # 就像猫眼适应不同光线,自动调整每个区域的阈值
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=11,  # 局部区域大小
            C=2  # 常数调整值
        )

        # 4. 形态学操作 - 清理杂点喵
        kernel = np.ones((2, 2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

        # 5. 锐化处理 - 让文字更清晰喵
        if sharpen_strength > 0:
            kernel_sharpen = np.array([
                [-1, -1, -1],
                [-1, 9 + sharpen_strength * 2, -1],
                [-1, -1, -1]
            ]) / (1 + sharpen_strength * 2)
            binary = cv2.filter2D(binary, -1, kernel_sharpen)

        # 6. 去除孤立噪点 - 最后清洁喵
        binary = cv2.fastNlMeansDenoising(
            binary, None, denoise_strength, 7, 21)

        return binary

    @staticmethod
    def adjust_contrast_brightness(image, contrast=1.0, brightness=0):
        """调整对比度和亮度 - 微调效果喵"""
        return cv2.convertScaleAbs(image, alpha=contrast, beta=brightness)


class ImagePrintApp(QMainWindow):
    """主窗口 - 猫咪的指挥中心喵~"""

    def __init__(self):
        super().__init__()
        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.init_ui()

    def init_ui(self):
        """初始化界面 - 布置猫窝喵"""
        self.setWindowTitle('🐾 试题图片处理打印助手 - 猫娘版 喵~')
        self.setGeometry(100, 100, 1200, 800)

        # 主窗口部件
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # 左侧: 控制面板
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel, 1)

        # 右侧: 图像显示区域
        image_panel = self.create_image_panel()
        main_layout.addWidget(image_panel, 3)

    def create_control_panel(self):
        """创建控制面板 - 猫咪的控制台喵"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # 标题
        title = QLabel('🐱 图像处理参数调整区 喵~')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 文件操作组
        file_group = QGroupBox('📁 文件操作')
        file_layout = QVBoxLayout()

        self.btn_load = QPushButton('🖼️ 选择图片')
        self.btn_load.clicked.connect(self.load_image)
        file_layout.addWidget(self.btn_load)

        self.btn_save = QPushButton('💾 保存处理后的图片')
        self.btn_save.clicked.connect(self.save_image)
        self.btn_save.setEnabled(False)
        file_layout.addWidget(self.btn_save)

        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # 图像处理参数组
        process_group = QGroupBox('🎨 图像处理参数')
        process_layout = QVBoxLayout()

        # 阈值调整
        process_layout.addWidget(QLabel('二值化阈值 (黑白分界线):'))
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setMinimum(50)
        self.threshold_slider.setMaximum(200)
        self.threshold_slider.setValue(127)
        self.threshold_slider.valueChanged.connect(self.process_image)
        self.threshold_label = QLabel('127')
        process_layout.addWidget(self.threshold_slider)
        process_layout.addWidget(self.threshold_label)

        # 降噪强度
        process_layout.addWidget(QLabel('降噪强度 (去除杂点):'))
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setMinimum(1)
        self.blur_slider.setMaximum(15)
        self.blur_slider.setValue(3)
        self.blur_slider.setSingleStep(2)
        self.blur_slider.valueChanged.connect(self.on_blur_changed)
        self.blur_label = QLabel('3')
        process_layout.addWidget(self.blur_slider)
        process_layout.addWidget(self.blur_label)

        # 锐化强度
        process_layout.addWidget(QLabel('锐化强度 (文字清晰度):'))
        self.sharpen_slider = QSlider(Qt.Horizontal)
        self.sharpen_slider.setMinimum(0)
        self.sharpen_slider.setMaximum(20)
        self.sharpen_slider.setValue(10)
        self.sharpen_slider.valueChanged.connect(self.process_image)
        self.sharpen_label = QLabel('1.0')
        process_layout.addWidget(self.sharpen_slider)
        process_layout.addWidget(self.sharpen_label)

        # 去噪强度
        process_layout.addWidget(QLabel('去噪强度 (平滑处理):'))
        self.denoise_slider = QSlider(Qt.Horizontal)
        self.denoise_slider.setMinimum(1)
        self.denoise_slider.setMaximum(20)
        self.denoise_slider.setValue(5)
        self.denoise_slider.valueChanged.connect(self.process_image)
        self.denoise_label = QLabel('5')
        process_layout.addWidget(self.denoise_slider)
        process_layout.addWidget(self.denoise_label)

        # 处理按钮
        self.btn_process = QPushButton('✨ 应用处理')
        self.btn_process.clicked.connect(self.process_image)
        self.btn_process.setEnabled(False)
        process_layout.addWidget(self.btn_process)

        # 重置按钮
        self.btn_reset = QPushButton('🔄 重置参数')
        self.btn_reset.clicked.connect(self.reset_parameters)
        process_layout.addWidget(self.btn_reset)

        process_group.setLayout(process_layout)
        layout.addWidget(process_group)

        # 打印设置组
        print_group = QGroupBox('🖨️ 打印设置')
        print_layout = QVBoxLayout()

        print_layout.addWidget(QLabel('打印DPI:'))
        self.dpi_spinbox = QSpinBox()
        self.dpi_spinbox.setMinimum(150)
        self.dpi_spinbox.setMaximum(600)
        self.dpi_spinbox.setValue(300)
        self.dpi_spinbox.setSingleStep(50)
        print_layout.addWidget(self.dpi_spinbox)

        self.btn_print = QPushButton('🖨️ 打印图片')
        self.btn_print.clicked.connect(self.print_image)
        self.btn_print.setEnabled(False)
        print_layout.addWidget(self.btn_print)

        print_group.setLayout(print_layout)
        layout.addWidget(print_group)

        # 底部说明
        info_label = QLabel('💡 提示: 调整参数后会自动预览效果喵~')
        info_label.setWordWrap(True)
        info_label.setStyleSheet('color: #666; font-size: 11px;')
        layout.addWidget(info_label)

        layout.addStretch()
        return panel

    def create_image_panel(self):
        """创建图像显示面板 - 猫咪的观察窗喵"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        # 标题
        title = QLabel('🖼️ 图像预览区域')
        title.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(title)

        # 图像对比显示
        images_layout = QHBoxLayout()

        # 原图
        original_widget = QWidget()
        original_layout = QVBoxLayout()
        original_layout.addWidget(QLabel('原始图像:'))
        self.original_label = QLabel()
        self.original_label.setAlignment(Qt.AlignCenter)
        self.original_label.setMinimumSize(400, 400)
        self.original_label.setStyleSheet(
            'border: 2px solid #ccc; background: #f5f5f5;')
        original_layout.addWidget(self.original_label)
        original_widget.setLayout(original_layout)
        images_layout.addWidget(original_widget)

        # 处理后图像
        processed_widget = QWidget()
        processed_layout = QVBoxLayout()
        processed_layout.addWidget(QLabel('处理后图像:'))
        self.processed_label = QLabel()
        self.processed_label.setAlignment(Qt.AlignCenter)
        self.processed_label.setMinimumSize(400, 400)
        self.processed_label.setStyleSheet(
            'border: 2px solid #ccc; background: #f5f5f5;')
        processed_layout.addWidget(self.processed_label)
        processed_widget.setLayout(processed_layout)
        images_layout.addWidget(processed_widget)

        layout.addLayout(images_layout)

        # 状态栏
        self.status_label = QLabel('等待加载图片... 喵~')
        self.status_label.setStyleSheet('color: #888; padding: 10px;')
        layout.addWidget(self.status_label)

        return panel

    def on_blur_changed(self):
        """确保模糊值为奇数"""
        value = self.blur_slider.value()
        if value % 2 == 0:
            value += 1
            self.blur_slider.setValue(value)
        self.blur_label.setText(str(value))
        self.process_image()

    def load_image(self):
        """加载图片 - 猫咪叼回猎物喵"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, '选择图片', '',
            'Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)'
        )

        if file_path:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path)

            if self.original_image is None:
                QMessageBox.warning(self, '错误', '无法加载图片喵!')
                return

            # 显示原图
            self.display_image(self.original_image, self.original_label)

            # 启用按钮
            self.btn_process.setEnabled(True)
            self.btn_save.setEnabled(True)
            self.btn_print.setEnabled(True)

            # 自动处理
            self.process_image()

            self.status_label.setText(f'已加载: {os.path.basename(file_path)} 喵~')

    def process_image(self):
        """处理图片 - 猫咪施展魔法喵"""
        if self.original_image is None:
            return

        # 获取参数
        threshold = self.threshold_slider.value()
        blur = self.blur_slider.value()
        sharpen = self.sharpen_slider.value() / 10.0
        denoise = self.denoise_slider.value()

        # 更新标签
        self.threshold_label.setText(str(threshold))
        self.sharpen_label.setText(f'{sharpen:.1f}')
        self.denoise_label.setText(str(denoise))

        # 处理图像
        try:
            self.processed_image = ImageProcessor.preprocess_image(
                self.original_image.copy(),
                threshold_value=threshold,
                blur_size=blur,
                sharpen_strength=sharpen,
                denoise_strength=denoise
            )

            # 显示处理后的图像
            self.display_image(self.processed_image, self.processed_label)
            self.status_label.setText('处理完成喵~ 可以打印或保存啦!')

        except Exception as e:
            QMessageBox.warning(self, '错误', f'处理失败喵: {str(e)}')

    def display_image(self, cv_image, label):
        """显示图像到标签 - 展示给主人看喵"""
        if len(cv_image.shape) == 2:  # 灰度图
            height, width = cv_image.shape
            bytes_per_line = width
            q_image = QImage(cv_image.data, width, height,
                             bytes_per_line, QImage.Format_Grayscale8)
        else:  # 彩色图
            height, width, channel = cv_image.shape
            bytes_per_line = 3 * width
            rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
            q_image = QImage(rgb_image.data, width, height,
                             bytes_per_line, QImage.Format_RGB888)

        # 缩放以适应标签大小
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(
            label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        label.setPixmap(scaled_pixmap)

    def save_image(self):
        """保存处理后的图像 - 存粮食喵"""
        if self.processed_image is None:
            QMessageBox.warning(self, '提示', '请先处理图片喵!')
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, '保存图片', '',
            'PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)'
        )

        if file_path:
            cv2.imwrite(file_path, self.processed_image)
            QMessageBox.information(self, '成功', '图片已保存喵~')
            self.status_label.setText(
                f'已保存到: {os.path.basename(file_path)} 喵~')

    def print_image(self):
        """打印图像 - 送到打印机喵"""
        if self.processed_image is None:
            QMessageBox.warning(self, '提示', '请先处理图片喵!')
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setResolution(self.dpi_spinbox.value())

        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            painter = QPainter(printer)

            # 转换为QImage
            if len(self.processed_image.shape) == 2:
                height, width = self.processed_image.shape
                q_image = QImage(self.processed_image.data, width, height,
                                 width, QImage.Format_Grayscale8)
            else:
                height, width, channel = self.processed_image.shape
                rgb_image = cv2.cvtColor(
                    self.processed_image, cv2.COLOR_BGR2RGB)
                q_image = QImage(rgb_image.data, width, height,
                                 3 * width, QImage.Format_RGB888)

            # 缩放以适应纸张
            rect = painter.viewport()
            size = q_image.size()
            size.scale(rect.size(), Qt.KeepAspectRatio)

            painter.setViewport(rect.x(), rect.y(),
                                size.width(), size.height())
            painter.setWindow(q_image.rect())
            painter.drawImage(0, 0, q_image)
            painter.end()

            QMessageBox.information(self, '成功', '打印任务已发送喵~')
            self.status_label.setText('打印完成喵~')

    def reset_parameters(self):
        """重置所有参数 - 恢复初始状态喵"""
        self.threshold_slider.setValue(127)
        self.blur_slider.setValue(3)
        self.sharpen_slider.setValue(10)
        self.denoise_slider.setValue(5)
        self.dpi_spinbox.setValue(300)

        if self.original_image is not None:
            self.process_image()

        self.status_label.setText('参数已重置喵~')


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用现代风格
    window = ImagePrintApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
