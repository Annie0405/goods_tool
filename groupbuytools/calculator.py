import tkinter as tk


class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self._setup_window()
        self._create_frames()
        self._create_widgets()
        self.root.mainloop()

    def _setup_window(self):
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 添加窗口标题
        self.root.title("均价计算器")
        # 窗口大小和位置
        window_width = 700
        window_height = 600
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 统计谷子种类的 frame
        self.frame_type = tk.Frame(self.root, width=600, height=290)
        self.frame_type.place(x=50, y=20)
        # 填写最终费用的 frame
        self.frame_price = tk.Frame(self.root, width=600, height=30)
        # 开始计算按钮的 frame
        self.frame_button = tk.Frame(self.root, width=600, height=30)
        # 显示均价的 frame
        self.frame_average = tk.Frame(self.root, width=600, height=60)

    def _create_widgets(self):
        # 统计谷子种类的组件
        frame = tk.Frame(self.frame_type, width=600, height=20)
        frame.pack()
        label = tk.Label(frame, text="请填写谷子种类、价格、点数，如果没有这么多种类可以置空")
        label.pack()
        for i in range(9):
            frame = tk.Frame(self.frame_type, width=600, height=30)
            frame.pack()
            label = tk.Label(frame, text=f"种类: ")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.entries[f"type{i}"] = entry


if __name__ == '__main__':
    Calculator()
