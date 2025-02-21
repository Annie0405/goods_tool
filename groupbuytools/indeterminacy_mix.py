import os
import pandas as pd
from openpyxl.styles import Alignment, PatternFill
import groupbuytools.utils as utils
from groupbuytools.group_buy_tools import GroupBuyTools

NULL = '><'


class IMTools(GroupBuyTools):
    def __init__(self, root_dir):
        super().__init__(root_dir)
        self.files = {
            'average_price': '预设1_均价.txt',   # 均价
            'adjusted_price': '预设2_调价.txt',     # 调价
            'final_price': '生成1_定价.txt',   # 定价
            'matching_table': '预设3_排表.txt',     # 排表
            'mix': '预设4_配比.txt',   # 配比
            'already_pay': '预设5_已肾.txt',   # 已肾
            'international_fee': '预设6_国际.txt',   # 国际
            'personal_international_fee': '生成2_国际.txt',
        }
        self.international_fee = self.get_international_fee()

    def get_mix(self):
        """
        配比文件有若干行，每行第一个元素是角色名，第二个元素是配比，两个元素之间用空格隔开
        """
        mix = {}
        total = 0
        file = os.path.join(self.root_dir, self.files['mix'])
        with open(file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    character, mix_ratio = line.split(' ')
                    mix_ratio = int(mix_ratio)
                    total += mix_ratio
                    mix[character] = mix_ratio
        print(f'{self.product_name}的总配比数为: ', total)
        return mix

    def get_remaining(self):
        # 初始化余量表
        remaining = {}
        for character in self.character:
            remaining[character] = self.mix[character]
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

    def get_international_fee(self):
        file_path = os.path.join(self.root_dir, self.files['international_fee'])
        with open(file_path, 'r') as f:
            fee = f.read()
        fee = fee.strip()
        fee = round(float(fee), 2)
        return fee

    def visualize_matching_table(self, width=8):
        print("==========")
        # 初始化一个空的 pandas 格式字典
        length = max(self.mix.values())
        pd_dict = {"character": []}
        for count in range(1, length+1):
            pd_dict[str(count)] = []
        # 遍历排表，将排表转成 pandas 格式
        for character, matching_table in self.matching_table.items():
            pd_dict["character"].append(character)    # 添加角色名
            cn_list = []    # 初始化 cn 列表
            for cn, num in matching_table.items():
                cn_list.extend([cn] * num)
            for i in range(length):
                if i < len(cn_list):
                    pd_dict[str(i + 1)].append(cn_list[i])
                elif i < self.mix[character]:
                    pd_dict[str(i + 1)].append(NULL)
                else:
                    pd_dict[str(i + 1)].append('')
        # 输出 pandas 列表
        df = pd.DataFrame(pd_dict)
        if '/' in self.product_name:
            excel_name = self.product_name.split('/')[-1]
        else:
            excel_name = self.product_name
        out_path = f"datas/{self.product_name}/{excel_name}排表.xlsx"
        fill = PatternFill(start_color="F0F8FF", end_color="F0F8FF", fill_type="solid")
        with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="排表")
            worksheet = writer.sheets["排表"]
            for col in worksheet.columns:
                column = col[0].column_letter  # 获取列字母
                worksheet.column_dimensions[column].width = width
                for cell in col:
                    cell.alignment = Alignment(horizontal='center', vertical='center')  # 单元格居中
                    if cell.value:  # 设置底色
                        cell.fill = fill
        print(f"排表已保存至 {out_path}")

    def cal_pay_table(self):
        print("==========")
        if self.remaining:
            print("警告！存在余量！")
        # 输出肾表
        pay_table = utils.reorder_dict(self.pay_table)  # 按联系方式排序
        out_path = os.path.join(self.root_dir, "肾表（应肾）.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            for cn, price in pay_table.items():
                f.write(f"{cn}: {price}\n")
            print(f"肾表已保存至 {out_path}")
        # 校验肾表
        total_mix = 0
        for character, mix_radio in self.mix.items():
            total_mix += mix_radio
        total_price = total_mix * self.average_price
        total_price = round(total_price, 2)
        total_pay_price = 0
        for price in self.pay_table.values():
            total_pay_price += price
        total_pay_price = round(total_pay_price, 2)
        if total_pay_price != total_price:
            print(f"{self.product_name}的肾表有误，当前肾表总和为{total_pay_price}，应等于{total_price}")
        else:
            print(f"{self.product_name}的肾表无误，当前肾表总和等于{total_price}")

    def cal_international_fee(self):
        fee_dict = {}
        file_path = os.path.join(self.root_dir, self.files['matching_table'])
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line:
                    elements = line.split(' ')
                    cn = elements[0]
                    cnt = 0
                    for e in elements[1:]:
                        if e.isdigit():
                            cnt += int(e)
                    fee_dict[cn] = round(cnt * self.international_fee, 2)
        file_path = os.path.join(self.root_dir, self.files['personal_international_fee'])
        with open (file_path, 'w', encoding='utf-8') as f:
            for cn, fee in fee_dict.items():
                f.write(f"{cn}\t{fee}\n")
            print(f"国际运费已保存至 {file_path}")

    def _verify_adjusted_price(self):
        total_price = 0
        for character, adjusted_price in self.adjusted_price.items():
            total_price += adjusted_price * self.mix[character]
        total_price = round(total_price, 2)
        if total_price == 0:
            print(f"{self.product_name}的调价已配平")
        else:
            print(f"{self.product_name}的调价未配平，当前调价总和为 {total_price}")

    def _verify_matching_table(self):
        for character, matching_table in self.matching_table.items():
            total_num = 0
            for num in matching_table.values():
                total_num += num
            if total_num > self.mix[character]:
                print(f"{self.product_name}的排表有误，角色 {character} 的排量总和为 {total_num}，应小于等于 {self.mix[character]}")
                return
        print(f"{self.product_name}的排表无误，所有角色的排量总和都小于等于其配比")
