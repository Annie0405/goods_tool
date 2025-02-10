import tkinter as tk
from tkinter import ttk


class Calculator:
    def __init__(self):
        self.root = tk.Tk()
        self.entries = {}
        self.output = {}
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
        window_width = 600
        window_height = 750
        axis_x = int((screen_width - window_width) / 2)
        axis_y = int((screen_height - window_height) / 2)
        self.root.geometry(f"{window_width}x{window_height}+{axis_x}+{axis_y}")

    def _create_frames(self):
        # 统计谷子种类的 frame
        self.frame_type = tk.Frame(self.root, width=600, height=290)
        self.frame_type.place(x=0, y=20)
        self.frame_type.pack_propagate(False)
        # 日元总价校验的 frame
        self.frame_price_check = tk.Frame(self.root, width=600, height=40)
        self.frame_price_check.place(x=0, y=300)
        self.frame_price_check.pack_propagate(False)
        # 填写最终费用的 frame
        self.frame_price = tk.Frame(self.root, width=600, height=30)
        self.frame_price.place(x=0, y=260)
        self.frame_price.pack_propagate(False)
        # 开始计算按钮的 frame
        self.frame_button = tk.Frame(self.root, width=600, height=30)
        self.frame_button.place(x=0, y=350)
        # 显示均价的 frame
        self.frame_average = tk.Frame(self.root, width=600, height=160)
        self.frame_average.place(x=0, y=390)
        # 分割线
        self.frame_divider = tk.Frame(self.root, width=580, height=1, bg="gray")
        self.frame_divider.place(x=10, y=560)
        # 计算器的 frame
        self.frame_calculator = tk.Frame(self.root, width=600, height=200)
        self.frame_calculator.place(x=0, y=570)
        self.frame_calculator.pack_propagate(False)

    def _create_widgets(self):
        # region 统计谷子种类的组件
        frame = tk.Frame(self.frame_type, width=600, height=200)
        frame.pack()
        label = tk.Label(frame, text="请填写谷子种类、价格、点数，如果没有这么多种类可以置空")
        label.pack(side=tk.LEFT)
        button = tk.Button(frame, text="清空", command=self._clear)
        button.pack(side=tk.LEFT, padx=(20, 0))

        for i in range(9):
            frame = tk.Frame(self.frame_type, width=600, height=30)
            frame.pack()

            label = tk.Label(frame, text=f"种类: ")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.entries[f"type{i}"] = entry

            options = ["单价", "总价"]
            combo = ttk.Combobox(frame, values=options, width=5)
            combo.pack(side=tk.LEFT, padx=(35, 0))
            combo.set("单价")
            self.entries[f"price_mode{i}"] = combo
            label = tk.Label(frame, text=f": ")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.entries[f"category_price{i}"] = entry
            label = tk.Label(frame, text=f"（日元）")
            label.pack(side=tk.LEFT)

            label = tk.Label(frame, text=f"点数: ")
            label.pack(side=tk.LEFT, padx=(20, 0))
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.entries[f"num{i}"] = entry
        # endregion

        # region 日元总价校验的组件
        label = tk.Label(self.frame_price_check, text="商品总价（包含岛内运费，不含手续费）: ")
        label.pack(side=tk.LEFT, padx=(10, 0))
        entry = tk.Entry(self.frame_price_check, width=10)
        entry.pack(side=tk.LEFT)
        self.entries["check_total_price"] = entry
        label = tk.Label(self.frame_price_check, text="（日元）")
        label.pack(side=tk.LEFT)
        button = tk.Button(self.frame_price_check, text="校验", command=self._check_price)
        button.pack(side=tk.LEFT, padx=(20, 0))
        # endregion

        # region 填写最终费用的组件
        label = tk.Label(self.frame_price, text="岛内运费: ")
        label.pack(side=tk.LEFT, padx=(10, 0))
        entry = tk.Entry(self.frame_price, width=10)
        entry.pack(side=tk.LEFT)
        self.entries["japan_shipping"] = entry
        label = tk.Label(self.frame_price, text="（日元）")
        label.pack(side=tk.LEFT)

        label = tk.Label(self.frame_price, text="手续费: ")
        label.pack(side=tk.LEFT, padx=(10, 0))
        entry = tk.Entry(self.frame_price, width=10)
        entry.pack(side=tk.LEFT)
        self.entries["service_charge"] = entry
        label = tk.Label(self.frame_price, text="（日元）")
        label.pack(side=tk.LEFT)

        label = tk.Label(self.frame_price, text="合计人民币: ")
        label.pack(side=tk.LEFT, padx=(10, 0))
        entry = tk.Entry(self.frame_price, width=10)
        entry.pack(side=tk.LEFT)
        self.entries["total_CNY"] = entry
        label = tk.Label(self.frame_price, text="（元）")
        label.pack(side=tk.LEFT)
        # endregion

        # region 开始计算按钮的组件
        button = tk.Button(self.frame_button, text="开始计算", command=self._calculate)
        button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        # endregion

        # region 显示均价的组件
        text = tk.Text(self.frame_average, height=10, width=75)
        text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.output["text1"] = text
        # endregion

        # region 计算器的组件
        label = tk.Label(self.frame_calculator, text="计算器，均价请输入人民币，如果没有这么多种类可置空" + '\n'
                         + "注：上半部分的计算结果无需校验，下半部分用于自己调整价格")
        label.pack(pady=(0, 10))

        _frame = tk.Frame(self.frame_calculator)
        _frame.pack()
        for i in range(3):
            for j in range(3):
                frame = tk.Frame(_frame)
                frame.grid(row=i, column=j)
                label = tk.Label(frame, text=f"均价: ")
                label.pack(side=tk.LEFT, padx=(20, 0))
                entry = tk.Entry(frame, width=6)
                entry.pack(side=tk.LEFT)
                self.entries[f"r_avg_price{i*3+j}"] = entry
                label = tk.Label(frame, text=f"点数: ")
                label.pack(side=tk.LEFT)
                entry = tk.Entry(frame, width=6)
                entry.pack(side=tk.LEFT)
                self.entries[f"r_num{i*3+j}"] = entry

        # region 计算按钮和显示结果
        frame = tk.Frame(self.frame_calculator)
        frame.pack(pady=(10, 0))
        button = tk.Button(frame, text="计算", command=self._calculator)
        button.pack(side=tk.LEFT, padx=(0, 30))
        label = tk.Label(frame, text="计算得合计人民币: ")
        label.pack(side=tk.LEFT)
        text = tk.Text(frame, height=1, width=10)
        text.pack(side=tk.LEFT)
        self.output["text2"] = text
        label = tk.Label(frame, text="元")
        label.pack(side=tk.LEFT)
        # endregion
        # endregion

    def _clear(self):
        for i in range(9):
            self.entries[f"type{i}"].delete(0, tk.END)
            self.entries[f"price_mode{i}"].set("单价")
            self.entries[f"category_price{i}"].delete(0, tk.END)
            self.entries[f"num{i}"].delete(0, tk.END)
        self.entries["japan_shipping"].delete(0, tk.END)
        self.entries["service_charge"].delete(0, tk.END)
        self.entries["total_CNY"].delete(0, tk.END)

    def _check_price(self):
        check_price = 0
        for i in range(9):
            if self.entries[f"type{i}"].get() == "":
                continue
            else:
                price_mode = self.entries[f"price_mode{i}"].get()
                if price_mode == "总价":
                    check_price += int(self.entries[f"category_price{i}"].get())
                else:
                    check_price += int(self.entries[f"category_price{i}"].get()) * int(self.entries[f"num{i}"].get())
        japan_shipping = int(self.entries["japan_shipping"].get())
        check_price += japan_shipping

        total_price = int(self.entries["check_total_price"].get())

        if check_price == total_price:
            self.output["text1"].delete("1.0", tk.END)
            self.output["text1"].insert(tk.END, "商品总价校验成功！\n")
        else:
            self.output["text1"].delete("1.0", tk.END)
            self.output["text1"].insert(tk.END, f"商品校验失败！计算结果为 {check_price}, 不等于 {total_price}\n")

    def _calculate(self):
        # 先确认有多少种类
        type_cnt = 0
        for i in range(9):
            if self.entries[f"type{i}"].get() == "":
                continue
            else:
                type_cnt += 1

        # 总点数
        total_num = 0
        for i in range(9):
            if self.entries[f"num{i}"].get() == "":
                continue
            else:
                total_num += int(self.entries[f"num{i}"].get())
        # 岛内均摊
        japan_shipping = float(self.entries["japan_shipping"].get())
        average_japan_shipping = japan_shipping / total_num

        # 各类单价
        single_price_dict = {}
        for i in range(9):
            if self.entries[f"type{i}"].get() == "":
                continue
            else:
                key = self.entries[f"type{i}"].get()
                price_mode = self.entries[f"price_mode{i}"].get()
                if self.entries[f"price_mode{i}"].get() == "单价":
                    value = float(self.entries[f"category_price{i}"].get())
                else:
                    num = int(self.entries[f"num{i}"].get())
                    value = float(self.entries[f"category_price{i}"].get()) / num
                value = value + average_japan_shipping
                single_price_dict[key] = value

        # 合计人民币
        total_CNY = float(self.entries["total_CNY"].get())

        # 总价
        total_price = 0
        for i in range(9):
            if self.entries[f"type{i}"].get() == "":
                continue
            else:
                if self.entries[f"price_mode{i}"].get() == "单价":
                    total_price += float(self.entries[f"category_price{i}"].get()) * int(self.entries[f"num{i}"].get())
                else:
                    total_price += float(self.entries[f"category_price{i}"].get())

        # 汇率
        exchange_rate = total_CNY / (total_price + japan_shipping)

        # 均价
        average_price = {}
        for key, value in single_price_dict.items():
            average_price[key] = round((value * exchange_rate), 2)

        # 进位校验
        while True:
            total_check = 0
            for i in range(9):
                if self.entries[f"type{i}"].get() == "":
                    continue
                else:
                    total_check += average_price[self.entries[f"type{i}"].get()] * int(self.entries[f"num{i}"].get())
            if total_check < total_CNY:
                for key, value in average_price.items():
                    average_price[key] += 0.01
                    average_price[key] = round(average_price[key], 2)
            else:
                break

        # 输出
        output_list = []
        for key, value in average_price.items():
            output_list.append(f"{key} 的均价是 {value} 人民币")
        output = "\n".join(output_list)
        self.output["text1"].delete("1.0", tk.END)
        self.output["text1"].insert(tk.END, output)

    def _calculator(self):
        total_price = 0
        for i in range(9):
            avg_price = self.entries[f"r_avg_price{i}"].get()
            if avg_price:
                total_price += float(avg_price) * int(self.entries[f"r_num{i}"].get())
        total_price = round(total_price, 2)
        self.output["text2"].delete("1.0", tk.END)
        self.output["text2"].insert(tk.END, total_price)


if __name__ == '__main__':
    try:
        Calculator()
    except Exception as e:
        # print(e)
        pass
