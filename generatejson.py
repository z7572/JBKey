import json

def generate_all_code_combinations():
    """生成A-Z（1位）、AA-ZZ（2位）、AAA-ZZZ（3位）的所有大写字母组合"""
    # 生成1位字母（A-Z）
    one_char = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
    # 生成2位字母（AA-ZZ）
    two_char = [f"{a}{b}" for a in one_char for b in one_char]
    # 生成3位字母（AAA-ZZZ）
    three_char = [f"{a}{b}{c}" for a in one_char for b in one_char for c in one_char]
    # 合并所有组合（1位+2位+3位）
    all_codes = one_char + two_char + three_char
    return all_codes

def generate_license_json(license_id="114514", licensee_name="z7572", assignee_name="", metadata="0120250101PSAN000005"):
    """生成包含所有字母组合的license.json"""
    # 获取所有1-3位大写字母组合
    all_codes = generate_all_code_combinations()
    # 构造products数组（每个code对应一个对象，有效期2099-12-31）
    products = [{"code": code, "paidUpTo": "2099-12-31"} for code in all_codes]
    
    # 构造最终JSON结构
    license_data = {
        "licenseId": license_id,
        "licenseeName": licensee_name,
        "assigneeName": assignee_name,
        "products": products,
        "metadata": metadata
    }
    
    # 写入JSON文件（格式化输出，编码UTF-8，确保中文正常）
    with open("license_full_codes.json", "w", encoding="utf-8") as f:
        json.dump(license_data, f, ensure_ascii=False, indent=2)
    
    print(f"生成完成！共包含 {len(all_codes)} 个产品编码组合")
    print(f"文件已保存为：license_full_codes.json")

# 执行生成（可修改licenseId、licenseeName等参数）
if __name__ == "__main__":
    generate_license_json(
        license_id="114514",
        licensee_name="z7572",
        metadata="0120250101PSAN000005"
    )