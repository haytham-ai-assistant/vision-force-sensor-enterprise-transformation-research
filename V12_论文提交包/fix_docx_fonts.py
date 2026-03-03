#!/usr/bin/env python3
"""
DOCX字体兼容性优化脚本
优化V12版本DOCX文件的字体兼容性，确保在所有Office版本中正常显示
"""

import os
import sys
import zipfile
import tempfile
import shutil
import xml.etree.ElementTree as ET

def optimize_font_table(font_table_xml):
    """优化字体表，只保留最通用的字体"""
    # 最通用的字体列表（在所有Office版本中都可用）
    generic_fonts = [
        ("Times New Roman", "roman", "00"),  # 英文衬线字体
        ("Arial", "swiss", "00"),  # 英文无衬线字体
        ("Courier New", "modern", "00"),  # 等宽字体
        ("Symbol", "roman", "02"),  # 符号字体
        ("Wingdings", "roman", "02"),  # 符号字体
    ]
    
    # 解析现有的字体表
    try:
        root = ET.fromstring(font_table_xml)
    except ET.ParseError:
        # 如果XML解析失败，创建新的字体表
        return create_generic_font_table()
    
    namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    # 移除所有现有字体定义
    for font_elem in root.findall('.//w:font', namespace):
        root.remove(font_elem)
    
    # 添加通用字体
    for i, (font_name, font_family, charset) in enumerate(generic_fonts):
        font_elem = ET.SubElement(root, f'{{{namespace["w"]}}}font')
        font_elem.set(f'{{{namespace["w"]}}}name', font_name)
        
        # 添加字体属性
        panose1 = ET.SubElement(font_elem, f'{{{namespace["w"]}}}panose1')
        panose1.set(f'{{{namespace["w"]}}}val', "02020603050405020304" if font_name == "Times New Roman" else 
                   "020B0604020202020204" if font_name == "Arial" else
                   "02070309020205020404" if font_name == "Courier New" else
                   "02000500000000000000" if font_name == "Symbol" else
                   "05000000000000000000")
        
        charset_elem = ET.SubElement(font_elem, f'{{{namespace["w"]}}}charset')
        charset_elem.set(f'{{{namespace["w"]}}}val', charset)
        
        family_elem = ET.SubElement(font_elem, f'{{{namespace["w"]}}}family')
        family_elem.set(f'{{{namespace["w"]}}}val', font_family)
        
        pitch_elem = ET.SubElement(font_elem, f'{{{namespace["w"]}}}pitch')
        pitch_elem.set(f'{{{namespace["w"]}}}val', "variable")
    
    return ET.tostring(root, encoding='unicode', method='xml')

def create_generic_font_table():
    """创建通用的字体表"""
    font_table = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:fonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:font w:name="Times New Roman">
    <w:panose1 w:val="02020603050405020304"/>
    <w:charset w:val="00"/>
    <w:family w:val="roman"/>
    <w:pitch w:val="variable"/>
  </w:font>
  <w:font w:name="Arial">
    <w:panose1 w:val="020B0604020202020204"/>
    <w:charset w:val="00"/>
    <w:family w:val="swiss"/>
    <w:pitch w:val="variable"/>
  </w:font>
  <w:font w:name="Courier New">
    <w:panose1 w:val="02070309020205020404"/>
    <w:charset w:val="00"/>
    <w:family w:val="modern"/>
    <w:pitch w:val="variable"/>
  </w:font>
  <w:font w:name="Symbol">
    <w:panose1 w:val="02000500000000000000"/>
    <w:charset w:val="02"/>
    <w:family w:val="roman"/>
    <w:pitch w:val="variable"/>
  </w:font>
  <w:font w:name="Wingdings">
    <w:panose1 w:val="05000000000000000000"/>
    <w:charset w:val="02"/>
    <w:family w:val="roman"/>
    <w:pitch w:val="variable"/>
  </w:font>
</w:fonts>'''
    return font_table

def optimize_docx_fonts(input_docx, output_docx):
    """优化DOCX文件的字体兼容性"""
    print(f"正在优化DOCX文件字体兼容性: {input_docx}")
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 解压DOCX文件
        with zipfile.ZipFile(input_docx, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # 优化字体表
        font_table_path = os.path.join(temp_dir, 'word/fontTable.xml')
        if os.path.exists(font_table_path):
            with open(font_table_path, 'r', encoding='utf-8') as f:
                font_table_xml = f.read()
            
            optimized_font_table = optimize_font_table(font_table_xml)
            
            with open(font_table_path, 'w', encoding='utf-8') as f:
                f.write(optimized_font_table)
            
            print("✅ 字体表优化完成")
        else:
            print("⚠️ 未找到字体表文件，将创建通用字体表")
            os.makedirs(os.path.dirname(font_table_path), exist_ok=True)
            with open(font_table_path, 'w', encoding='utf-8') as f:
                f.write(create_generic_font_table())
        
        # 压缩为新的DOCX文件
        with zipfile.ZipFile(output_docx, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        print(f"✅ DOCX文件优化完成: {output_docx}")
        
        # 检查文件大小
        orig_size = os.path.getsize(input_docx)
        new_size = os.path.getsize(output_docx)
        print(f"原始文件大小: {orig_size} 字节")
        print(f"优化后大小: {new_size} 字节")
        
        return True
        
    except Exception as e:
        print(f"❌ 优化过程中出错: {e}")
        return False
    finally:
        # 清理临时目录
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def main():
    if len(sys.argv) != 3:
        print("用法: python3 fix_docx_fonts.py <输入DOCX文件> <输出DOCX文件>")
        print("示例: python3 fix_docx_fonts.py 原始.docx 优化后.docx")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"错误: 输入文件不存在: {input_file}")
        sys.exit(1)
    
    if optimize_docx_fonts(input_file, output_file):
        print("\n✅ DOCX字体优化成功！")
        print("优化后的文件使用最通用的字体，确保在所有Office版本中正常显示。")
        print("建议在不同版本的Office中测试文件显示效果。")
    else:
        print("\n❌ DOCX字体优化失败")
        sys.exit(1)

if __name__ == "__main__":
    main()