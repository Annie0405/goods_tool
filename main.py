from groupbuytools.group_buy_tools import GroupBuyTools

rijiubajifengzu = GroupBuyTools(r"datas/日九系列/日九吧唧风组")
rijiupld = GroupBuyTools(r"datas/日九系列/日九拍立得")
tripxiaoka = GroupBuyTools(r"datas/trip系列/trip小卡")
qi_miao = GroupBuyTools(r"datas/奇妙拍立得")
zhen_cang = GroupBuyTools(r"datas/珍藏小卡第五弹")
v5_hua_qian = GroupBuyTools(r"datas/v5系列/v5花前")
v5_hua_hou = GroupBuyTools(r"datas/v5系列/v5花后")

v5_hua_qian.verify()
v5_hua_qian.visualize_matching_table()
v5_hua_hou.verify()
v5_hua_hou.visualize_matching_table()
