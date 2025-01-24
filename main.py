from groupbuytools.group_buy_tools import GroupBuyTools

rijiubajifengzu = GroupBuyTools(r"datas/日九系列/日九吧唧风组")
rijiupld = GroupBuyTools(r"datas/日九系列/日九拍立得")
tripxiaoka = GroupBuyTools(r"datas/trip系列/trip小卡")
qi_miao = GroupBuyTools(r"datas/奇妙拍立得")

rijiupld.verify()
rijiupld.cal_pay_table()

qi_miao.verify()
