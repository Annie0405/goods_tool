from groupbuytools.group_buy_tools import GroupBuyTools
from groupbuytools.indeterminacy_mix import IMTools

v5_A = IMTools(r"datas/v5系列/v5花前")
# v5_A.cal_pay_table()

v5_B = IMTools(r"datas/v5系列/v5花后")
v5_B.cal_pay_table()
