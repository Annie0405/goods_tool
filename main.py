from groupbuytools.group_buy_tools import GroupBuyTools

rijiubajifengzu = GroupBuyTools(r"datas/日九系列/日九吧唧风组")
rijiupld = GroupBuyTools(r"datas/日九系列/日九拍立得")
guancangka = GroupBuyTools(r"datas/馆藏卡")
tripxiaoka = GroupBuyTools(r"datas/trip系列/trip小卡")

rijiubajifengzu.verify()
rijiubajifengzu.gen_final_price()
rijiubajifengzu.cal_pay_table()
