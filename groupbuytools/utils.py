def reorder_dict(d):
    # 提取包含“闲鱼”的键，包含“微信”的键和其他键
    first = {k: v for k, v in d.items() if "微信" not in k and "闲鱼" not in k}  # 排在前面的键值对
    second = {k: v for k, v in d.items() if "微信" in k}  # 包含“微信”的键值对
    third = {k: v for k, v in d.items() if "闲鱼" in k}  # 包含“闲鱼”的键值对
    # 按顺序合并字典
    return {**first, **second, **third}
