from groupbuytools.group_buy_tools import GroupBuyTools

# rijiubajishuizu = GroupBuyTools(r"datas/日九系列/日九吧唧水组")
# rijiubajishuizu.verify()
# rijiubajishuizu.gen_final_price()
#
# rijiubajifengzu = GroupBuyTools(r"datas/日九系列/日九吧唧风组")
# rijiubajifengzu.verify()
# rijiubajifengzu.gen_final_price()

rijiupld = GroupBuyTools(r"datas/日九系列/日九拍立得")
rijiupld.verify()
rijiupld.cal_pay_table()
# rijiupld.gen_final_price()
# rijiupld.visualize_matching_table(8)

# guancangka = GroupBuyTools(r"datas/馆藏卡")
# guancangka.verify()
# guancangka.cal_remaining()
