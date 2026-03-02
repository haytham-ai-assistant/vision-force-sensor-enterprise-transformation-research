#!/usr/bin/env python3
"""
RTF文件头部修复脚本
修复V12版本RTF文件缺少标准头部的问题
"""

import os
import sys
import re

def create_rtf_header():
    """创建标准的RTF头部"""
    header = """{\\rtf1\\ansi\\deff0
{\\fonttbl
{\\f0 \\froman Times New Roman;}
{\\f1 \\fswiss Arial;}
{\\f2 \\fmodern Courier New;}
{\\f3 \\fnil \\fcharset134 \\'cb\\'ce\\'cc\\'e5;}  /* 宋体 */
{\\f4 \\fnil \\fcharset134 \\'ba\\'da\\'cc\\'e5;}  /* 黑体 */
}
{\\colortbl;\\red0\\green0\\blue0;\\red255\\green0\\blue0;}
\\viewkind4\\uc1\\pard\\lang2052\\f0\\fs24
"""
    return header

def fix_rtf_file(input_file, output_file):
    """修复RTF文件，添加标准头部"""
    print(f"正在修复RTF文件: {input_file}")
    
    # 读取原始文件内容
    with open(input_file, 'rb') as f:
        content = f.read()
    
    # 尝试检测编码
    try:
        text = content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = content.decode('gbk')
        except UnicodeDecodeError:
            text = content.decode('latin-1')
    
    # 创建标准头部
    header = create_rtf_header()
    
    # 组合修复后的内容
    # 如果已经有RTF头部，则替换
    if text.startswith('{\\rtf1'):
        # 已经是正确的RTF格式，只检查字体表
        if '{\\fonttbl' not in text[:1000]:
            # 插入字体表
            rtf_end = text.find('\\', 10)  # 找到第一个\后的位置
            fixed_text = text[:rtf_end] + header[rtf_end:] + text[rtf_end:]
        else:
            fixed_text = text
    else:
        # 没有RTF头部，直接添加
        fixed_text = header + text
    
    # 写入修复后的文件
    with open(output_file, 'wb') as f:
        f.write(fixed_text.encode('utf-8'))
    
    print(f"修复完成，输出文件: {output_file}")
    print(f"原始文件大小: {len(content)} 字节")
    print(f"修复后大小: {len(fixed_text.encode('utf-8'))} 字节")
    
    return True

def main():
    if len(sys.argv) != 3:
        print("用法: python3 fix_rtf_header.py <输入文件> <输出文件>")
        print("示例: python3 fix_rtf_header.py 原始.rtf 修复后.rtf")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"错误: 输入文件不存在: {input_file}")
        sys.exit(1)
    
    try:
        fix_rtf_file(input_file, output_file)
        print("\n✅ RTF文件修复成功！")
        print("请使用Microsoft Office或WordPad打开修复后的文件测试兼容性。")
    except Exception as e:
        print(f"❌ 修复过程中出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()