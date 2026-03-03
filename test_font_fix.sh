#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

TEMPLATE_FILE="03_（2026年）硕士研究生学位论文格式模板.docx"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo "=== 测试不同字体设置 ==="

# 测试1: 无字体设置（使用默认）
echo "测试1: 无字体设置"
pandoc cover_text.md complete_paper.md \
    -o "output/test_no_font_${TIMESTAMP}.docx" \
    --reference-doc="$TEMPLATE_FILE" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例" \
    --variable papersize=a4

# 测试2: 使用通用字体名称
echo "测试2: 使用通用字体名称"
pandoc cover_text.md complete_paper.md \
    -o "output/test_generic_font_${TIMESTAMP}.docx" \
    --reference-doc="$TEMPLATE_FILE" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例" \
    --variable papersize=a4 \
    --variable mainfont="宋体" \
    --variable sansfont="黑体" \
    --variable monofont="新宋体"

# 测试3: 使用英文字体名称
echo "测试3: 使用英文字体名称"
pandoc cover_text.md complete_paper.md \
    -o "output/test_english_font_${TIMESTAMP}.docx" \
    --reference-doc="$TEMPLATE_FILE" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例" \
    --variable papersize=a4 \
    --variable mainfont="SimSun" \
    --variable sansfont="SimHei" \
    --variable monofont="NSimSun"

# 测试4: 使用UTF-8编码明确指定
echo "测试4: 使用UTF-8编码"
pandoc cover_text.md complete_paper.md \
    -o "output/test_utf8_${TIMESTAMP}.docx" \
    --reference-doc="$TEMPLATE_FILE" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例" \
    --variable papersize=a4 \
    --from markdown+smart

# 测试5: 使用docx原生转换（不使用模板）
echo "测试5: 原生docx转换"
pandoc cover_text.md complete_paper.md \
    -o "output/test_native_${TIMESTAMP}.docx" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例"

echo "=== 测试完成 ==="
echo "生成的测试文件:"
ls -la output/test_*_${TIMESTAMP}.docx