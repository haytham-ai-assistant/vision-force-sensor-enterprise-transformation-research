#!/usr/bin/env python3
"""
验证Word文档结构
检查字体、样式、标题编号等关键格式元素
"""

import zipfile
import xml.etree.ElementTree as ET
import re
from pathlib import Path

def check_docx_structure(docx_path):
    """检查.docx文件的结构"""
    print(f"正在验证文档: {docx_path}")
    
    with zipfile.ZipFile(docx_path, 'r') as docx:
        # 检查必要文件是否存在
        required_files = [
            'word/document.xml',
            'word/styles.xml', 
            'word/fontTable.xml',
            'word/numbering.xml'
        ]
        
        for file in required_files:
            if file not in docx.namelist():
                print(f"  ⚠️  缺少必要文件: {file}")
            else:
                print(f"  ✓ {file} 存在")
        
        # 分析字体表
        print("\n=== 字体分析 ===")
        if 'word/fontTable.xml' in docx.namelist():
            font_content = docx.read('word/fontTable.xml').decode('utf-8')
            chinese_fonts = ['宋体', '黑体', '仿宋', '微软雅黑', 'SimSun', 'SimHei']
            found_fonts = []
            for font in chinese_fonts:
                if font in font_content:
                    found_fonts.append(font)
            if found_fonts:
                print(f"  ✓ 找到中文字体: {', '.join(found_fonts)}")
            else:
                print("  ⚠️  未找到常用中文字体")
        
        # 分析样式
        print("\n=== 样式分析 ===")
        if 'word/styles.xml' in docx.namelist():
            styles_content = docx.read('word/styles.xml').decode('utf-8')
            heading_styles = ['Heading 1', 'heading 1', '标题 1']
            found_headings = []
            for style in heading_styles:
                if style.lower() in styles_content.lower():
                    found_headings.append(style)
            if found_headings:
                print(f"  ✓ 找到标题样式: {', '.join(found_headings)}")
            
            # 检查标题样式定义
            tree = ET.fromstring(styles_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            heading_count = 0
            for style in tree.findall('.//w:style', ns):
                style_type = style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type')
                style_id = style.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}styleId')
                if style_type == 'paragraph' and style_id and ('Heading' in style_id or 'heading' in style_id):
                    heading_count += 1
            print(f"  ✓ 找到 {heading_count} 个标题段落样式")
        
        # 检查文档内容中的标题
        print("\n=== 标题结构分析 ===")
        if 'word/document.xml' in docx.namelist():
            doc_content = docx.read('word/document.xml').decode('utf-8')
            
            # 查找章节标题
            chapter_patterns = [
                r'第[一二三四五六七八九十]+章',
                r'第一章', r'第二章', r'第三章', r'第四章', r'第五章', r'第六章', r'第七章'
            ]
            
            found_chapters = []
            for pattern in chapter_patterns:
                matches = re.findall(pattern, doc_content)
                found_chapters.extend(matches)
            
            if found_chapters:
                unique_chapters = sorted(set(found_chapters))
                print(f"  ✓ 找到章节标题: {', '.join(unique_chapters)}")
                
                # 检查标题数量
                chapter_count = len([c for c in found_chapters if '章' in c])
                print(f"  ✓ 文档包含 {chapter_count} 个章节标题")
            else:
                print("  ⚠️  未找到章节标题")
            
            # 检查是否应用了标题样式
            if 'w:val="Heading' in doc_content or 'w:val="heading' in doc_content:
                print("  ✓ 检测到标题样式应用")
            else:
                print("  ⚠️  未检测到标题样式应用标记")
        
        # 检查编号系统
        print("\n=== 编号系统分析 ===")
        if 'word/numbering.xml' in docx.namelist():
            numbering_content = docx.read('word/numbering.xml').decode('utf-8')
            if 'w:numId' in numbering_content:
                print("  ✓ 文档包含编号定义")
            else:
                print("  ⚠️  文档可能缺少编号定义")
        
        print("\n=== 验证完成 ===")

if __name__ == '__main__':
    # 使用最新生成的Word文档
    docx_dir = Path('/workspace/论文/视觉力学传感器企业战略转型研究-HSM/final_submission')
    latest_docx = None
    latest_time = 0
    
    for file in docx_dir.glob('视觉力学传感器企业战略转型研究_格式调整版_*.docx'):
        if file.stat().st_mtime > latest_time:
            latest_time = file.stat().st_mtime
            latest_docx = file
    
    if latest_docx:
        check_docx_structure(str(latest_docx))
    else:
        print("未找到Word文档")