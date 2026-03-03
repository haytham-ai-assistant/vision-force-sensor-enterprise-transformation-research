#!/usr/bin/env python3
"""
AI痕迹检查脚本
检查论文中剩余的AI痕迹特征
"""

import re
import sys
from collections import Counter

def load_content(file_path):
    """加载论文内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def check_long_sentences(content):
    """检查长句（超过60字）"""
    # 简单的中文句子分割
    sentences = re.split(r'[。！？；]', content)
    long_sentences = []
    
    for s in sentences:
        s = s.strip()
        if len(s) > 60 and not s.startswith('#') and not s.startswith('['):
            # 排除标题行和链接
            long_sentences.append(s)
    
    return long_sentences

def check_ai_transition_words(content):
    """检查AI常用的标准化过渡词"""
    patterns = [
        r'综上所述', r'由此可见', r'鉴于上述分析',
        r'研究表明', r'研究结果显示', r'具体来说',
        r'具体来看', r'总的来说', r'总体而言',
        r'一方面', r'另一方面', r'首先', r'其次', r'再次', r'最后',
        r'第一，', r'第二，', r'第三，', r'第四，', r'第五，',
        r'其一，', r'其二，', r'其三，',
        r'从.*角度来看', r'在.*背景下', r'随着.*发展',
        r'需要指出的是', r'值得注意的是', r'可以预见的是'
    ]
    
    matches = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, content))
    
    return matches

def check_pseudo_precise_scores(content):
    """检查伪精确数字评分"""
    # 匹配如85.4分、4.8分、2.0分等模式
    pattern = r'\b\d+\.\d+分\b'
    return re.findall(pattern, content)

def check_keyword_density(content):
    """检查关键词密度"""
    keywords = ['战略转型', '数字化转型', 'DIC', '硬科技', '视觉力学传感器']
    counts = {}
    
    for keyword in keywords:
        counts[keyword] = len(re.findall(keyword, content))
    
    return counts

def check_list_patterns(content):
    """检查列表式结构"""
    patterns = [
        r'第一，.*?第二，.*?第三，',
        r'首先，.*?其次，.*?再次，.*?最后，',
        r'一是.*?二是.*?三是',
        r'一方面.*?另一方面',
    ]
    
    matches = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, content, re.DOTALL))
    
    return matches

def check_textbook_definitions(content):
    """检查教科书式定义"""
    # 匹配以"XX是指"、"XX是"开头的定义式句子
    pattern = r'[^。！？；]{2,20}是指[^。！？；]{10,100}。'
    return re.findall(pattern, content)

def main():
    if len(sys.argv) < 2:
        print("用法: python3 ai_trace_check.py <论文文件>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    content = load_content(file_path)
    
    print("=" * 60)
    print("AI痕迹检查报告")
    print("=" * 60)
    
    # 1. 长句检查
    long_sentences = check_long_sentences(content)
    print(f"\n1. 长句检查（超过60字）:")
    print(f"   发现 {len(long_sentences)} 个长句")
    if long_sentences:
        print(f"   示例（前3个）:")
        for i, s in enumerate(long_sentences[:3]):
            print(f"   {i+1}. {s[:80]}...")
    
    # 2. 标准化过渡词
    transition_words = check_ai_transition_words(content)
    print(f"\n2. 标准化过渡词检查:")
    print(f"   发现 {len(transition_words)} 个标准化过渡词")
    if transition_words:
        word_counts = Counter(transition_words)
        print(f"   最常见的5个:")
        for word, count in word_counts.most_common(5):
            print(f"     {word}: {count}次")
    
    # 3. 伪精确数字评分
    pseudo_scores = check_pseudo_precise_scores(content)
    print(f"\n3. 伪精确数字评分检查:")
    print(f"   发现 {len(pseudo_scores)} 个伪精确评分")
    if pseudo_scores:
        print(f"   具体数值: {', '.join(set(pseudo_scores))}")
    
    # 4. 关键词密度
    keyword_counts = check_keyword_density(content)
    print(f"\n4. 关键词密度检查:")
    total_words = len(content)
    for keyword, count in keyword_counts.items():
        density = (count / total_words) * 10000  # 每万字出现次数
        print(f"   {keyword}: {count}次 (密度: {density:.2f}/万字)")
    
    # 5. 列表式结构
    list_patterns = check_list_patterns(content)
    print(f"\n5. 列表式结构检查:")
    print(f"   发现 {len(list_patterns)} 个列表式结构")
    if list_patterns:
        print(f"   示例（前2个）:")
        for i, pattern in enumerate(list_patterns[:2]):
            print(f"   {i+1}. {pattern[:100]}...")
    
    # 6. 教科书式定义
    textbook_defs = check_textbook_definitions(content)
    print(f"\n6. 教科书式定义检查:")
    print(f"   发现 {len(textbook_defs)} 个教科书式定义")
    if textbook_defs:
        print(f"   示例（前2个）:")
        for i, definition in enumerate(textbook_defs[:2]):
            print(f"   {i+1}. {definition}")
    
    # 总体评估
    print(f"\n" + "=" * 60)
    print("总体评估:")
    
    issue_count = (
        len(long_sentences) // 10 +  # 每10个长句算一个问题
        len(transition_words) // 5 +  # 每5个标准化词算一个问题
        len(pseudo_scores) +  # 每个伪精确评分都是问题
        len(list_patterns) +  # 每个列表式结构都是问题
        len(textbook_defs)    # 每个教科书定义都是问题
    )
    
    if issue_count == 0:
        print("✅ 论文AI痕迹极低，通过反AI查重检测的概率很高")
    elif issue_count <= 5:
        print("⚠️  论文有少量AI痕迹，建议进一步优化")
    elif issue_count <= 15:
        print("⚠️  论文有较多AI痕迹，需要优化")
    else:
        print("❌ 论文AI痕迹明显，需要大幅优化")
    
    print(f"   问题指标总数: {issue_count}")
    
    # 建议
    print(f"\n优化建议:")
    if long_sentences:
        print(f"  - 拆分{len(long_sentences)}个长句，使句子更简洁")
    if transition_words:
        print(f"  - 替换{len(transition_words)}个标准化过渡词，使用更自然的表达")
    if pseudo_scores:
        print(f"  - 移除{len(pseudo_scores)}个伪精确评分，改用定性描述")
    if list_patterns:
        print(f"  - 重构{len(list_patterns)}个列表式结构，转换为自然段落")
    if textbook_defs:
        print(f"  - 重写{len(textbook_defs)}个教科书式定义，加入个性化理解")
    
    print(f"\n" + "=" * 60)

if __name__ == "__main__":
    main()