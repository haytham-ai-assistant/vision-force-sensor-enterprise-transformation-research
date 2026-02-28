#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

echo "=== V10文档格式验证脚本 ==="
echo "检查V10版本文档格式..."
echo ""

# 指定V10文档路径
V10_DOCX="final_submission/视觉力学传感器企业战略转型研究以HSM为例_毕胜昔_20260228_V10_20260228_072812.docx"

if [ ! -f "$V10_DOCX" ]; then
    echo "错误: 未找到V10 Word文档: $V10_DOCX"
    exit 1
fi

echo "V10 Word文档: $V10_DOCX"
echo "文档大小: $(stat -c%s "$V10_DOCX") 字节"
echo ""

# 提取文档结构进行验证
echo "步骤1: 检查文档结构..."
# 使用pandoc提取标题结构
if command -v pandoc >/dev/null 2>&1; then
    pandoc "$V10_DOCX" -t markdown --toc --number-sections 2>/dev/null | grep -E "^#{1,3}" | head -20 > /tmp/doc_structure_v10.txt
    echo "文档标题结构（前20个）:"
    echo "------------------------"
    cat /tmp/doc_structure_v10.txt
    echo "------------------------"
    echo ""
    
    # 检查常见的格式问题
    echo "步骤2: 检查常见格式问题..."
    
    # 1. 检查是否有重复编号（如"3.1 1.1"）
    REPEAT_PATTERN="[0-9]+\.[0-9]+ [0-9]+\.[0-9]+"
    if grep -E "$REPEAT_PATTERN" /tmp/doc_structure_v10.txt > /dev/null; then
        echo "❌ 发现重复编号问题（如'3.1 1.1'）"
        grep -E "$REPEAT_PATTERN" /tmp/doc_structure_v10.txt
    else
        echo "✅ 无重复编号问题"
    fi
    
    # 2. 检查章节编号是否连续
    echo ""
    echo "步骤3: 检查章节连续性..."
    # 提取所有章节标题
    CHAPTERS=$(grep -E "^# " /tmp/doc_structure_v10.txt | wc -l)
    SECTIONS=$(grep -E "^## " /tmp/doc_structure_v10.txt | wc -l)
    SUBSECTIONS=$(grep -E "^### " /tmp/doc_structure_v10.txt | wc -l)
    
    echo "章标题数量: $CHAPTERS"
    echo "节标题数量: $SECTIONS"
    echo "小节标题数量: $SUBSECTIONS"
    
    # 预期至少7章（绪论到结论）
    if [ $CHAPTERS -ge 7 ]; then
        echo "✅ 章节数量充足（7章以上）"
    else
        echo "⚠️  章节数量可能不足（预期至少7章）"
    fi
else
    echo "⚠️  pandoc未安装，跳过文档结构分析"
fi

# 3. 检查文件完整性
echo ""
echo "步骤4: 检查文件完整性..."
DOCX_SIZE=$(stat -c%s "$V10_DOCX")

echo "Word文档大小: $DOCX_SIZE 字节"

if [ $DOCX_SIZE -lt 100000 ]; then
    echo "⚠️  Word文档可能过小，请检查内容完整性"
else
    echo "✅ Word文档大小正常"
fi

# 检查关键内容是否存在
echo ""
echo "步骤5: 检查关键内容..."
echo "关键内容检查结果："

# 使用strings检查文档中是否包含关键内容
if strings "$V10_DOCX" | grep -q "SWOT"; then
    echo "✅ SWOT分析内容存在"
else
    echo "❌ 未找到SWOT分析内容"
fi

if strings "$V10_DOCX" | grep -q "参考文献"; then
    echo "✅ 参考文献部分存在"
else
    echo "❌ 未找到参考文献部分"
fi

if strings "$V10_DOCX" | grep -q "北京大学"; then
    echo "✅ 北京大学模板标识存在"
else
    echo "⚠️  未找到北京大学模板标识"
fi

echo ""
echo "=== 验证完成 ==="
echo "建议: 请在Microsoft Word中打开文档进行最终验证"
echo "关键检查点:"
echo "1. 封面页是否正常显示（无乱码）"
echo "2. 目录是否正常生成（无乱码）"
echo "3. 标题编号是否正确（第一章、1.1、1.2...）"
echo "4. 正文格式是否符合模板要求"
echo "5. 表格编号是否正确（表4.8等）"
echo "6. 参考文献格式是否正确"
