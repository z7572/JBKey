import json

def generate_all_code_combinations():
    """生成1-3位所有大写字母组合（A-Z、AA-ZZ、AAA-ZZZ），按长度+字母排序"""
    one_char = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    two_char = [f"{a}{b}" for a in one_char for b in one_char]
    three_char = [f"{a}{b}{c}" for a in one_char for b in one_char for c in one_char]
    all_codes = one_char + two_char + three_char
    # 排序规则：先按长度（1位→2位→3位），再按字母顺序
    return sorted(all_codes, key=lambda x: (len(x), x))

def get_target_group_codes(all_codes, split_choices, group_count_per_split=2):
    """
    根据二分选择列表，定位目标分组的编码
    :param all_codes: 全量1-3位编码列表
    :param split_choices: 二分选择列表（如[6,1]表示：第1次拆8组选第6组，第2次拆2组选第1组）
    :param group_count_per_split: 每次拆分的组数（默认2组，纯二分；也可设8组快速缩小范围）
    :return: 目标分组的编码列表 + 分组范围描述
    """
    current_codes = all_codes.copy()
    choice_desc = []  # 记录每一步的选择范围
    
    for idx, choice in enumerate(split_choices):
        # 拆分当前编码为指定组数
        total = len(current_codes)
        group_size = total // group_count_per_split
        groups = []
        for i in range(group_count_per_split):
            start = i * group_size
            end = (i + 1) * group_size if i < group_count_per_split - 1 else total
            group_codes = current_codes[start:end]
            groups.append({
                "group_id": i + 1,  # 分组编号从1开始
                "codes": group_codes,
                "range": f"{group_codes[0]} ~ {group_codes[-1]}" if group_codes else "Empty"
            })
        
        # 验证选择的分组是否有效
        if choice < 1 or choice > len(groups):
            raise ValueError(f"第{idx+1}次选择的分组{choice}无效！当前仅拆分出{len(groups)}组")
        
        # 定位到选择的分组
        target_group = groups[choice - 1]
        current_codes = target_group["codes"]
        choice_desc.append(f"第{idx+1}次选择：第{choice}组（范围：{target_group['range']}，数量：{len(target_group['codes'])}）")
    
    # 输出选择路径
    print("📌 二分选择路径：")
    for desc in choice_desc:
        print(f"   {desc}")
    
    # 返回最终目标分组的编码和范围
    range_desc = f"{current_codes[0]} ~ {current_codes[-1]}" if current_codes else "Empty"
    return current_codes, range_desc

def generate_target_license_file(target_codes, range_desc, base_config):
    """生成目标分组的license.json文件"""
    # 构造JSON数据
    license_data = {
        "licenseId": base_config["licenseId"],
        "licenseeName": base_config["licenseeName"],
        "assigneeName": base_config["assigneeName"],
        "products": [{"code": code, "paidUpTo": "2099-12-31"} for code in target_codes],
        "metadata": base_config["metadata"]
    }
    
    # 生成文件名（包含范围，便于识别）
    safe_range = range_desc.replace(" ~ ", "_").replace("/", "_")
    filename = f"license_find_sql.json"
    
    # 写入文件
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(license_data, f, ensure_ascii=False, indent=2)
    
    # 输出结果
    print(f"\n✅ 生成目标分组JSON文件：{filename}")
    print(f"🔢 编码数量：{len(target_codes)} | 范围：{range_desc}")
    print(f"💡 下一步：将该文件重命名为license.json，生成激活码验证")

# 主执行逻辑
if __name__ == "__main__":
    # ====================== 核心配置（只需修改这部分）======================
    # 1. 二分选择列表：按顺序记录每次选择的分组编号（从1开始）
    #    示例1：[6] → 首次拆8组，选第6组
    #    示例2：[6,1] → 首次拆8组选第6组，再拆2组选第1组
    #    示例3：[6,1,2] → 在上一步基础上，再拆2组选第2组
    split_choices = [1,1,2,1,1,2,2,1,2,2,1,2,2]  # 【你只需修改这个列表】
    
    # 2. 每次拆分的组数（默认2组=纯二分；首次可设8组快速缩小范围）
    group_count_per_split = 2  # 首次拆分建议设8，后续设2
    
    # 3. 基础授权配置（和你的一致，无需改）
    base_config = {
        "licenseId": "114514",
        "licenseeName": "z7572",
        "assigneeName": "",
        "metadata": "0120250101PSAN000005"
    }
    # =====================================================================
    
    # 生成全量编码 → 定位目标分组 → 生成JSON文件
    all_codes = generate_all_code_combinations()
    target_codes, range_desc = get_target_group_codes(all_codes, split_choices, group_count_per_split)
    generate_target_license_file(target_codes, range_desc, base_config)