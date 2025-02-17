from groupbuytools.group_buy_tools import GroupBuyTools
from groupbuytools.indeterminacy_mix import IMTools

rijiubajifengzu = GroupBuyTools(r"datas/日九系列/日九吧唧风组")
rijiupld = GroupBuyTools(r"datas/日九系列/日九拍立得")
tripxiaoka = GroupBuyTools(r"datas/trip系列/trip小卡")
qi_miao = GroupBuyTools(r"datas/奇妙拍立得")
zhen_cang = GroupBuyTools(r"datas/珍藏小卡第五弹")
v5_hua_qian = GroupBuyTools(r"datas/v5系列/v5花前")
v5_hua_hou = GroupBuyTools(r"datas/v5系列/v5花后")

ceshi = IMTools(r"datas/测试")
ceshi.verify()
ceshi.visualize_matching_table()
ceshi.cal_remaining()
ceshi.cal_pay_table()
