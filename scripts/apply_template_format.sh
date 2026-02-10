#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

# 检查模板文件是否存在
TEMPLATE_FILE="03_（2026年）硕士研究生学位论文格式模板.docx"
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "错误: 模板文件不存在: $TEMPLATE_FILE"
    exit 1
fi

echo "=== 北京大学硕士论文格式调整 ==="
echo "使用模板: $TEMPLATE_FILE"
echo ""

# 输出文件命名（包含时间戳以便区分版本）
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PAPER_TITLE="视觉力学传感器企业战略转型研究"
OUTPUT_DOCX="output/${PAPER_TITLE}_格式调整版_${TIMESTAMP}.docx"
OUTPUT_PDF="output/${PAPER_TITLE}_格式调整版_${TIMESTAMP}.pdf"

echo "步骤1: 准备封面页..."
# 创建临时封面页（包含元数据）
cat > /tmp/cover_temp.md << 'EOF'
---
title: 视觉力学传感器企业战略转型研究——以HSM为例
author: 老毕
institute: 北京大学汇丰商学院
program: 高级管理人员工商管理硕士（EMBA）
supervisor: （请填写导师姓名）
date: 二〇二六年二月
abstract: |
  本文以深圳市海塞姆科技有限公司（HSM）为案例，研究视觉力学传感器企业在数字化转型和国产替代背景下的战略转型问题...
keywords: [视觉力学传感器, 企业战略转型, 数字化转型, 硬科技企业, DIC技术, 海塞姆科技]
abstract-en: |
  This paper takes Shenzhen Haytham Technology Co., Ltd. (HSM) as a case study to examine the strategic transformation of visual force sensor enterprises...
keywords-en: [Visual force sensor, Enterprise strategic transformation, Digital transformation, Hard-tech enterprise, DIC technology, Haytham Technology]
---
EOF

echo "步骤2: 合并文档并应用模板样式..."
# 使用pandoc转换，应用模板样式
pandoc /tmp/cover_temp.md complete_paper.md \
    -o "$OUTPUT_DOCX" \
    --reference-doc="$TEMPLATE_FILE" \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例" \
    --metadata institute="北京大学汇丰商学院" \
    --metadata program="高级管理人员工商管理硕士（EMBA）" \
    --metadata supervisor="（请填写导师姓名）" \
    --variable papersize=a4 \
    --variable geometry:margin=2.6cm \
    --variable linestretch=1.0

if [ $? -eq 0 ]; then
    echo "✅ Word文档生成成功: $OUTPUT_DOCX"
else
    echo "❌ Word文档生成失败"
    exit 1
fi

echo "步骤3: 生成PDF版本（使用LaTeX引擎）..."
# 生成PDF版本（使用xelatex支持中文字体）
pandoc /tmp/cover_temp.md complete_paper.md \
    -o "$OUTPUT_PDF" \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例" \
    -V mainfont="Noto Serif CJK SC" \
    -V sansfont="Noto Sans CJK SC" \
    -V monofont="Noto Sans Mono CJK SC" \
    -V geometry:a4paper,margin=2.6cm \
    -V fontsize=12pt \
    -V linestretch=1.0

if [ $? -eq 0 ]; then
    echo "✅ PDF文档生成成功: $OUTPUT_PDF"
else
    echo "❌ PDF文档生成失败，尝试使用默认设置..."
    # 回退方案：从Word生成PDF（如果需要）
    echo "注意：可能需要手动从Word转换PDF"
fi

echo ""
echo "=== 格式调整完成 ==="
echo "生成的文件:"
echo "  - Word文档: $OUTPUT_DOCX"
echo "  - PDF文档:  $OUTPUT_PDF"
echo ""
echo "下一步: 请验证格式是否符合模板要求"
echo "关键检查点:"
echo "  1. 论文题目: 一号黑体，居中"
echo "  2. 章标题: 中文数字，黑体三号，居中"
echo "  3. 节标题: 阿拉伯数字，黑体四号，居左"
echo "  4. 正文: 小四宋体/Times New Roman，固定行距20磅"
echo "  5. 页面设置: A4，页边距上3.0cm/下2.5cm/左右2.6cm"

# 清理临时文件
rm -f /tmp/cover_temp.md

echo ""
echo "✅ 格式调整脚本执行完成"