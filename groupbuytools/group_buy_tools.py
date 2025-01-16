import os
import pandas as pd


class GroupBuyTools:
    """
    提供所有拼团工具的接口
    """
    def __init__(self, root_dir):
        self.files = {
            'average_price': 'average_price.txt',
            'adjusted_price': 'adjusted_price.txt',
            'final_price': 'final_price.txt',
            'matching_table': 'matching_table.txt',
            'mix': 'mix.txt',
        }
        self.root_dir = root_dir
        self.product_name = os.path.basename(root_dir)
        self.average_price = self.get_average_price()
        self.character = self.get_character()
        self.adjusted_price = self.get_adjusted_price()
        self.final_price = self.get_final_price()
        self.matching_table = self.get_matching_table()
        self.mix = self.get_mix()

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

    # =====================
    # 以下是提供给外部调用的接口
    # =====================

    def gen_final_price(self):
        file = os.path.join(self.root_dir, self.files['final_price'])
        with open(file, 'w', encoding='utf-8') as f:
            for character, final_price in self.final_price.items():
                f.write(f"{character} {final_price}\n")
        print(f"最终定价已保存至 {file}")

    def verify(self):
        self.__verify_adjusted_price()

    def visualize_matching_table(self):
        data = {"Name": ["Alice", "Bob", "Charlie"], "Age": [24, 27, 22]}
        df = pd.DataFrame(data)
        print(df)
        df.to_excel('output.xlsx', sheet_name='People', index=False)

        # 构建排表的二维数组
        tdarray = []
        for character, matching_table in self.matching_table.items():
            pass

    def cal_remaining(self):
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
        # 输出余量
        print("余量：")
        for character, num in remaining.items():
            print(f"{character}: {num}")

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
