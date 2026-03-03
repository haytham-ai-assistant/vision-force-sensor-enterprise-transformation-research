#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

TEMPLATE_FILE="03_（2026年）硕士研究生学位论文格式模板.docx"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PAPER_TITLE="视觉力学传感器企业战略转型研究"

echo "=== 生成兼容性更好的Word文档 ==="

# 方法1: 使用最简单的设置（最可能兼容）
echo "方法1: 简单设置（推荐）"
pandoc cover_text.md complete_paper.md \
    -o "output/${PAPER_TITLE}_简单设置_${TIMESTAMP}.docx" \
    --reference-doc="$TEMPLATE_FILE" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例"

# 方法2: 不使用模板，生成基本docx
echo "方法2: 基本docx（无模板）"
pandoc cover_text.md complete_paper.md \
    -o "output/${PAPER_TITLE}_基本格式_${TIMESTAMP}.docx" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例"

# 方法3: 生成RTF格式（兼容性最好）
echo "方法3: RTF格式（老版本Office兼容）"
pandoc cover_text.md complete_paper.md \
    -o "output/${PAPER_TITLE}_RTF格式_${TIMESTAMP}.rtf" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例"

# 方法4: 生成ODT格式（LibreOffice兼容）
echo "方法4: ODT格式（开源格式）"
pandoc cover_text.md complete_paper.md \
    -o "output/${PAPER_TITLE}_ODT格式_${TIMESTAMP}.odt" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例"

echo ""
echo "=== 生成完成 ==="
echo "推荐按以下顺序尝试："
echo "1. output/${PAPER_TITLE}_简单设置_${TIMESTAMP}.docx - 最可能兼容"
echo "2. output/${PAPER_TITLE}_基本格式_${TIMESTAMP}.docx - 无模板，更简单"
echo "3. output/${PAPER_TITLE}_RTF格式_${TIMESTAMP}.rtf - RTF格式，兼容性最好"
echo "4. output/${PAPER_TITLE}_ODT格式_${TIMESTAMP}.odt - 可用LibreOffice打开"
echo ""
echo "如果所有格式都乱码，请检查："
echo "1. Office是否为最新版本"
echo "2. 是否安装了中文字体包"
echo "3. 尝试使用WPS Office或LibreOffice"
echo "4. 尝试在线转换工具：将docx上传到Google Docs或Office Online"