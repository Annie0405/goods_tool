import os
import pandas as pd
from openpyxl.styles import Alignment
import groupbuytools.utils as utils

NULL = ' '

class GroupBuyTools:
    """
    提供所有拼团工具的接口
    """
    def __init__(self, root_dir):
        self.files = {
            'average_price': 'average_price.txt',   # 均价
            'adjusted_price': 'adjusted_price.txt',     # 调价
            'final_price': 'final_price.txt',   # 定价
            'matching_table': 'matching_table.txt',     # 排表
            'mix': 'mix.txt',   # 配比
            'already_pay': 'already_pay.txt',   # 已肾
        }
        self.root_dir = root_dir    # 根目录
        self.product_name = self.get_product_name()     # 谷名
        self.average_price = self.get_average_price()   # 均价
        self.character = self.get_character()   # 角色列表
        self.adjusted_price = self.get_adjusted_price()     # 调价
        self.final_price = self.get_final_price()   # 定价
        self.matching_table = self.get_matching_table()     # 排表
        self.mix = self.get_mix()   # 配比
        self.remaining = self.get_remaining()   # 余量
        self.pay_table = self.get_pay_table()     # 肾表（应肾）
        self.already_pay = self.get_already_pay()   # 肾表（已肾）

    def get_product_name(self):
        dir_name = self.root_dir.split('datas/')[1]
        return dir_name

    def get_average_price(self):
        """
        均价文件里只有一个元素，即均价
        """
        file = os.path.join(self.root_dir, self.files['average_price'])
        with open(file, 'r', encoding='utf-8') as f:
            average_price = round(float(f.readline().strip()), 2)
        return average_price

    def get_character(self):
        character = []
        file = os.path.join(self.root_dir, self.files['adjusted_price'])
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    character.append(line.split(' ')[0])
        return character

    def get_adjusted_price(self):
        """
        调价文件每行两个元素，空格隔开
        第一个元素是角色名，第二个元素是调价
        返回一个字典，键是角色名，值是调价
        """
        map_adjusted_price = {}
        file = os.path.join(self.root_dir, self.files['adjusted_price'])
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    character, adjusted_price = line.split(' ')
                    adjusted_price = round(float(adjusted_price), 2)
                    map_adjusted_price[character] = adjusted_price
        return map_adjusted_price

    def get_final_price(self):
        """
        返回一个列表，键是角色名，值是最终定价
        :return:
        """
        map_final_price = {}
        for character, adjusted_price in self.adjusted_price.items():
            final_price = round(self.average_price + adjusted_price, 2)
            map_final_price[character] = final_price
        return map_final_price

    def get_matching_table(self):
        """
        排表文件每行若干个元素
        第一个元素是cn。第二个元素开始，每两个元素依次是角色名和排量
        返回一个嵌套字典，外层字典的键是角色名
        内层字典的键是cn，值是排量
        """
        # 初始化排表
        matching_table = {}
        for character in self.character:
            matching_table[character] = {}
        # 从文件中读取
        file = os.path.join(self.root_dir, self.files['matching_table'])
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    cn = line.split(' ')[0]
                    character_nums = line.split(' ')[1:]
                    for i in range(0, len(character_nums), 2):
                        pair = character_nums[i:i+2]
                        character = pair[0]
                        if character not in self.character:
                            print(f"{self.product_name} 的排表有误，角色 {character} 不在调价文件中")
                            return
                        num = int(pair[1])
                        matching_table[character][cn] = num
        return matching_table

    def get_mix(self):
        """
        配比文件里只有一个元素，即配比
        """
        file = os.path.join(self.root_dir, self.files['mix'])
        with open(file, 'r', encoding='utf-8') as f:
            mix = int(f.readline().strip())
        return mix

    def get_remaining(self):
        # 初始化余量表
        remaining = {}
        for character in self.character:
            remaining[character] = self.mix
        # 计算余量
        for character, matching_table in self.matching_table.items():
            for cn, num in matching_table.items():
                remaining[character] -= num
        # 删除0余量角色
        zero = []
        for character, num in remaining.items():
            if num == 0:
                zero.append(character)
        for character in zero:
            remaining.pop(character)
        return remaining

    def get_pay_table(self):
        pay_table = {}
        for character, matching_table in self.matching_table.items():
            price = self.final_price[character]
            for cn, num in matching_table.items():
                if cn not in pay_table:
                    pay_table[cn] = 0
                pay_table[cn] += price * num
                pay_table[cn] = round(pay_table[cn], 2)
        return pay_table

    def get_already_pay(self):
        """
        肾表（已肾）文件每行2个元素
        第一个元素是cn。第二个元素是已肾金额
        返回一个字典，键是cn，值是已肾金额
        """
        already_pay = {}
        file = os.path.join(self.root_dir, self.files['already_pay'])
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    cn, money = line.split(' ')
                    money = round(float(money), 2)
                    already_pay[cn] = money
        return already_pay

    # =====================
    # 以下是提供给外部调用的接口
    # =====================

    def gen_final_price(self):
        print("==========")
        file = os.path.join(self.root_dir, self.files['final_price'])
        with open(file, 'w', encoding='utf-8') as f:
            for character, final_price in self.final_price.items():
                f.write(f"{character} {final_price}\n")
        print(f"最终定价已保存至 {file}")

    def verify(self):
        print("==========")
        self.__verify_adjusted_price()
        self.__verify_matching_table()

    def visualize_matching_table(self, width=10):
        print("==========")
        # 初始化一个空的 pandas 格式字典
        pd_dict = {"character": []}
        for count in range(1, self.mix + 1):
            pd_dict[str(count)] = []
        # 遍历排表，将排表转成 pandas 格式
        for character, matching_table in self.matching_table.items():
            pd_dict["character"].append(character)    # 添加角色名
            cn_list = []    # 初始化 cn 列表
            for cn, num in matching_table.items():
                cn_list.extend([cn] * num)
            for i in range(self.mix):
                if i < len(cn_list):
                    pd_dict[str(i + 1)].append(cn_list[i])
                else:
                    pd_dict[str(i + 1)].append(NULL)
        # 输出 pandas 列表
        df = pd.DataFrame(pd_dict)
        if '/' in self.product_name:
            excel_name = self.product_name.split('/')[1]
        else:
            excel_name = self.product_name
        out_path = f"datas/{self.product_name}/{excel_name}排表.xlsx"
        with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="排表")
            worksheet = writer.sheets["排表"]
            for col in worksheet.columns:
                column = col[0].column_letter  # 获取列字母
                worksheet.column_dimensions[column].width = width
                for cell in col:
                    cell.alignment = Alignment(horizontal='center', vertical='center')  # 单元格居中
        print(f"排表已保存至 {out_path}")

    def cal_remaining(self):
        print("==========")
        # 输出余量（如果有）
        if self.remaining:
            # 计算总余量
            total_remaining = sum(self.remaining.values())
            # 输出余量
            out_path = os.path.join(self.root_dir, "余量.txt")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(f"总余量：{total_remaining}\n")
                for character, num in self.remaining.items():
                    f.write(f"{character}: {num}\n")
            print(f"余量已保存至 {out_path}")
        else:
            print("无余量")

    def cal_pay_table(self):
        print("==========")
        if self.remaining:
            print("警告！存在余量！")
        # 输出肾表
        pay_table = utils.reorder_dict(self.pay_table)  # 按联系方式排序
        out_path = os.path.join(self.root_dir, "肾表（应肾).txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            for cn, price in pay_table.items():
                f.write(f"{cn}: {price}\n")
            print(f"肾表已保存至 {out_path}")
        # 校验肾表
        total_price = self.mix * self.average_price * len(self.character)
        total_price = round(total_price, 2)
        total_pay_price = 0
        for price in self.pay_table.values():
            total_pay_price += price
        total_pay_price = round(total_pay_price, 2)
        if total_pay_price != total_price:
            print(f"{self.product_name}的肾表有误，当前肾表总和为{total_pay_price}，应等于{total_price}")
        else:
            print(f"{self.product_name}的肾表无误，当前肾表总和等于{total_price}")

    def refund_and_makeup(self):
        print("==========")
        # 计算退补
        rm_table = {}
        for cn, price in self.pay_table.items():
            if cn in self.already_pay:
                rm_price = price - self.already_pay[cn]
                if rm_price != 0:
                    rm_table[cn] = round(rm_price, 2)
            else:
                rm_table[cn] = price
        for cn, price in self.already_pay.items():
            if cn not in self.pay_table:
                rm_table[cn] = -price
        # 输出退补
        rm_table = utils.reorder_dict(rm_table)     # 按联系方式排序
        out_path = os.path.join(self.root_dir, "退补.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            for cn, price in rm_table.items():
                already = self.already_pay[cn] if cn in self.already_pay else 0
                if price > 0:
                    f.write(f"{cn}已付{already}元，需补{price}元\n")
                else:
                    f.write(f"{cn}已付{already}元，需退{-price}元\n")
        print(f"退补已保存至 {out_path}")

    # =====================
    # 以下是私有方法
    # =====================

    def __verify_adjusted_price(self):
        total_price = 0
        for adjusted_price in self.adjusted_price.values():
            total_price += adjusted_price
        if total_price == 0:
            print(f"{self.product_name}的调价已配平")
        else:
            print(f"{self.product_name}的调价未配平，当前调价总和为 {total_price}")

    def __verify_matching_table(self):
        for character, matching_table in self.matching_table.items():
            total_num = 0
            for num in matching_table.values():
                total_num += num
            if total_num > self.mix:
                print(f"{self.product_name}的排表有误，角色 {character} 的排量总和为 {total_num}，应小于等于 {self.mix}")
                return
        print(f"{self.product_name}的排表无误，所有角色的排量总和都小于等于{self.mix}")
