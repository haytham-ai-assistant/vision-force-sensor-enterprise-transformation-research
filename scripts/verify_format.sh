#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

echo "=== 格式验证脚本 ==="
echo "检查最新生成的格式调整文档..."
echo ""

# 查找最新的格式调整文档
LATEST_DOCX=$(ls -t output/视觉力学传感器企业战略转型研究_格式调整版_*.docx 2>/dev/null | head -1)
LATEST_PDF=$(ls -t output/视觉力学传感器企业战略转型研究_格式调整版_*.pdf 2>/dev/null | head -1)

if [ -z "$LATEST_DOCX" ]; then
    echo "错误: 未找到格式调整版Word文档"
    exit 1
fi

echo "最新Word文档: $LATEST_DOCX"
echo "最新PDF文档:  $LATEST_PDF"
echo ""

# 提取文档结构进行验证
echo "步骤1: 检查文档结构..."
# 使用pandoc提取标题结构
pandoc "$LATEST_DOCX" -t markdown --toc --number-sections 2>/dev/null | grep -E "^#{1,3}" | head -20 > /tmp/doc_structure.txt

echo "文档标题结构（前20个）:"
echo "------------------------"
cat /tmp/doc_structure.txt
echo "------------------------"
echo ""

# 检查常见的格式问题
echo "步骤2: 检查常见格式问题..."

# 1. 检查是否有重复编号（如"3.1 1.1"）
REPEAT_PATTERN="[0-9]+\.[0-9]+ [0-9]+\.[0-9]+"
if grep -E "$REPEAT_PATTERN" /tmp/doc_structure.txt > /dev/null; then
    echo "❌ 发现重复编号问题（如'3.1 1.1'）"
    grep -E "$REPEAT_PATTERN" /tmp/doc_structure.txt
else
    echo "✅ 无重复编号问题"
fi

# 2. 检查章节编号是否连续
echo ""
echo "步骤3: 检查章节连续性..."
# 提取所有章节标题
CHAPTERS=$(grep -E "^# " /tmp/doc_structure.txt | wc -l)
SECTIONS=$(grep -E "^## " /tmp/doc_structure.txt | wc -l)
SUBSECTIONS=$(grep -E "^### " /tmp/doc_structure.txt | wc -l)

echo "章标题数量: $CHAPTERS"
echo "节标题数量: $SECTIONS"
echo "小节标题数量: $SUBSECTIONS"

# 3. 检查文件完整性
echo ""
echo "步骤4: 检查文件完整性..."
DOCX_SIZE=$(stat -c%s "$LATEST_DOCX")
PDF_SIZE=$(stat -c%s "$LATEST_PDF")

echo "Word文档大小: $DOCX_SIZE 字节"
echo "PDF文档大小:  $PDF_SIZE 字节"

if [ $DOCX_SIZE -lt 100000 ]; then
    echo "⚠️  Word文档可能过小，请检查内容完整性"
else
    echo "✅ Word文档大小正常"
fi

if [ $PDF_SIZE -lt 100000 ]; then
    echo "⚠️  PDF文档可能过小，请检查内容完整性"
else
    echo "✅ PDF文档大小正常"
fi

echo ""
echo "=== 验证完成 ==="
echo "建议: 请在Microsoft Word中打开文档进行最终验证"
echo "关键检查点:"
echo "1. 封面页是否正常显示（无乱码）"
echo "2. 目录是否正常生成（无乱码）"
echo "3. 标题编号是否正确（第一章、1.1、1.2...）"
echo "4. 正文格式是否符合模板要求"