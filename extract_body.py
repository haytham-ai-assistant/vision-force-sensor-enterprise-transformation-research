#!/usr/bin/env python3
import re

def extract_body(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到正文开始位置（第一章绪论）
    # 使用正则找到"# 第一章 绪论"或类似模式
    # 论文中正文开始是"# 第一章 绪论"
    
    # 首先找到"<!-- 正文开始 -->"注释后的内容
    body_start_marker = "<!-- 正文开始 -->"
    body_start = content.find(body_start_marker)
    
    if body_start == -1:
        # 如果没有标记，找"# 第一章 绪论"
        chapter1_pattern = r'^# 第一章 绪论'
        match = re.search(chapter1_pattern, content, re.MULTILINE)
        if match:
            body_start = match.start()
        else:
            # 如果还是找不到，从开头开始
            body_start = 0
    else:
        body_start += len(body_start_marker)
    
    # 找到正文结束位置（参考文献部分之前）
    # 首先查找"# 参考文献"
    references_pattern = r'^# 参考文献'
    match = re.search(references_pattern, content[body_start:], re.MULTILINE)
    if match:
        body_end = body_start + match.start()
    else:
        # 如果没有参考文献部分，查找"# 致谢"
        acknowledgments_pattern = r'^# 致谢'
        match = re.search(acknowledgments_pattern, content[body_start:], re.MULTILINE)
        if match:
            body_end = body_start + match.start()
        else:
            # 如果都没有，使用全文
            body_end = len(content)
    
    # 提取正文
    body_content = content[body_start:body_end]
    
    # 移除可能残留的目录标记
    body_content = re.sub(r'<!-- 目录将由pandoc自动生成 -->', '', body_content)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# 论文正文（查重版）\n\n")
        f.write(body_content)
    
    print(f"已提取正文，长度: {len(body_content)} 字符")
    
    # 统计字数
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', body_content))
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', body_content))
    total_words_estimate = chinese_chars + english_words
    
    print(f"中文字符数: {chinese_chars:,}")
    print(f"英文单词数: {english_words:,}")
    print(f"估算总字数: {total_words_estimate:,}")

if __name__ == "__main__":
    input_file = "complete_paper.md"
    output_file = "查重版_正文.md"
    extract_body(input_file, output_file)