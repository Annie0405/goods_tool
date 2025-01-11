import os


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
        }
        self.root_dir = root_dir
        self.product_name = os.path.basename(root_dir)
        self.average_price = self.get_average_price()
        self.adjusted_price = self.get_adjusted_price()
        self.final_price = self.get_final_price()
        self.matching_table = self.get_matching_table()

    def get_average_price(self):
        """
        均价文件里只有一个元素，即均价
        """
        file = os.path.join(self.root_dir, self.files['average_price'])
        with open(file, 'r', encoding='utf-8') as f:
            average_price = round(float(f.readline().strip()), 2)
        return average_price

    def get_adjusted_price(self):
        """
        调价文件每行两个元素，空格隔开
        第一个元素是角色名，第二个元素是调价
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
        map_final_price = {}
        for character, adjusted_price in self.adjusted_price.items():
            final_price = round(self.average_price + adjusted_price, 2)
            map_final_price[character] = final_price
        return map_final_price

    def get_matching_table(self):
        pass

    def verify_adjusted_price(self):
        total_price = 0
        for adjusted_price in self.adjusted_price.values():
            total_price += adjusted_price
        if total_price == 0:
            print(f"{self.product_name}的调价已配平")
        else:
            print(f"{self.product_name}的调价未配平，当前调价总和为 {total_price}")

    def gen_final_price(self):
        file = os.path.join(self.root_dir, self.files['final_price'])
        with open(file, 'w', encoding='utf-8') as f:
            for character, final_price in self.final_price.items():
                f.write(f"{character} {final_price}\n")
        print(f"最终定价已保存至 {file}")
