#!/usr/bin/env python3
"""
Office兼容性诊断脚本
诊断Word文档在Office中的兼容性问题并提供修复建议
"""

import os
import sys
import magic
import zipfile
import tempfile
import shutil

def check_file_type(file_path):
    """检查文件类型"""
    mime = magic.Magic(mime=True)
    file_type = mime.from_file(file_path)
    
    print(f"📄 文件类型检查: {file_path}")
    print(f"   MIME类型: {file_type}")
    
    if file_type == 'application/rtf':
        return 'rtf'
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        return 'docx'
    elif file_type == 'application/msword':
        return 'doc'
    else:
        return 'unknown'

def check_rtf_compatibility(rtf_path):
    """检查RTF文件兼容性"""
    print(f"\n🔍 RTF文件兼容性检查: {rtf_path}")
    
    issues = []
    
    try:
        with open(rtf_path, 'rb') as f:
            content = f.read(1000)  # 读取前1000字节
        
        # 检查RTF头部
        if not content.startswith(b'{\\rtf1'):
            issues.append("❌ 缺少标准RTF头部 ({\\rtf1)")
        
        # 检查字体表
        if b'{\\fonttbl' not in content:
            issues.append("❌ 缺少字体表定义 ({\\fonttbl)")
        
        # 检查Unicode编码
        if b'\\u' in content:
            # 统计Unicode转义数量
            unicode_count = content.count(b'\\u')
            issues.append(f"⚠️  检测到{unicode_count}个Unicode转义，在某些Office版本中可能显示异常")
        
        # 检查文件大小
        file_size = os.path.getsize(rtf_path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            issues.append("⚠️  文件较大，可能影响加载速度")
        
        if issues:
            print("  发现以下兼容性问题:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("  ✅ RTF文件兼容性良好")
        
        return issues
        
    except Exception as e:
        print(f"  ❌ 检查过程中出错: {e}")
        return ["检查失败"]

def check_docx_compatibility(docx_path):
    """检查DOCX文件兼容性"""
    print(f"\n🔍 DOCX文件兼容性检查: {docx_path}")
    
    issues = []
    
    try:
        # 检查是否为有效的ZIP文件
        if not zipfile.is_zipfile(docx_path):
            issues.append("❌ 不是有效的DOCX文件（不是ZIP格式）")
            return issues
        
        # 解压检查关键文件
        temp_dir = tempfile.mkdtemp()
        
        try:
            with zipfile.ZipFile(docx_path, 'r') as zip_ref:
                # 检查必需的文件
                required_files = [
                    '[Content_Types].xml',
                    'word/document.xml',
                    'word/styles.xml'
                ]
                
                for req_file in required_files:
                    if req_file not in zip_ref.namelist():
                        issues.append(f"❌ 缺少必需文件: {req_file}")
                
                # 检查字体表
                if 'word/fontTable.xml' in zip_ref.namelist():
                    zip_ref.extract('word/fontTable.xml', temp_dir)
                    font_table_path = os.path.join(temp_dir, 'word/fontTable.xml')
                    
                    with open(font_table_path, 'r', encoding='utf-8') as f:
                        font_content = f.read()
                    
                    # 检查字体数量
                    font_count = font_content.count('<w:font ')
                    if font_count > 10:
                        issues.append(f"⚠️  字体数量较多 ({font_count}种)，可能影响兼容性")
                    
                    # 检查特殊字体
                    special_fonts = ['幼圆', '仿宋', 'Arial Unicode MS', 'Cambria Math']
                    for font in special_fonts:
                        if font in font_content:
                            issues.append(f"⚠️  使用了特殊字体: {font}，在某些系统中可能不可用")
                
                # 检查文件大小
                file_size = os.path.getsize(docx_path)
                if file_size > 5 * 1024 * 1024:  # 5MB
                    issues.append("⚠️  DOCX文件较大，可能影响打开速度")
                
        finally:
            # 清理临时目录
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        
        if issues:
            print("  发现以下兼容性问题:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("  ✅ DOCX文件兼容性良好")
        
        return issues
        
    except Exception as e:
        print(f"  ❌ 检查过程中出错: {e}")
        return ["检查失败"]

def main():
    if len(sys.argv) < 2:
        print("用法: python3 office_compatibility_check.py <文件1> [文件2] ...")
        print("示例: python3 office_compatibility_check.py 文档.docx 文档.rtf")
        sys.exit(1)
    
    print("=" * 60)
    print("Office兼容性诊断工具")
    print("=" * 60)
    
    all_issues = {}
    
    for file_path in sys.argv[1:]:
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            continue
        
        print(f"\n📋 分析文件: {os.path.basename(file_path)}")
        print("-" * 40)
        
        # 检查文件类型
        file_type = check_file_type(file_path)
        
        # 根据文件类型进行兼容性检查
        if file_type == 'rtf':
            issues = check_rtf_compatibility(file_path)
            all_issues[file_path] = issues
        elif file_type == 'docx':
            issues = check_docx_compatibility(file_path)
            all_issues[file_path] = issues
        else:
            print(f"  ⚠️  不支持的文件类型: {file_type}")
            all_issues[file_path] = ["不支持的文件类型"]
    
    # 总结报告
    print("\n" + "=" * 60)
    print("兼容性诊断总结")
    print("=" * 60)
    
    for file_path, issues in all_issues.items():
        file_name = os.path.basename(file_path)
        if not issues or (len(issues) == 1 and issues[0] == "检查失败"):
            print(f"✅ {file_name}: 通过兼容性检查")
        else:
            print(f"⚠️  {file_name}: 发现{len(issues)}个问题")
    
    print("\n💡 修复建议:")
    print("1. RTF文件问题: 运行 fix_rtf_header.py 添加标准头部")
    print("2. DOCX字体问题: 运行 fix_docx_fonts.py 优化字体兼容性")
    print("3. 文件过大: 压缩图片，减少嵌入字体")
    print("\n🔧 可用修复脚本:")
    print("  - fix_rtf_header.py: 修复RTF文件头部问题")
    print("  - fix_docx_fonts.py: 优化DOCX字体兼容性")
    
    return 0

if __name__ == "__main__":
    # 检查magic库是否安装
    try:
        import magic
    except ImportError:
        print("❌ 需要安装python-magic库: pip install python-magic")
        sys.exit(1)
    
    sys.exit(main())