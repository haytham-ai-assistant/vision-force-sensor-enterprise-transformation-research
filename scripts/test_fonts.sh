#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

echo "=== 测试不同的字体设置 ==="
echo ""

# 测试1: 原始命令（当前使用）
echo "测试1: 原始命令（参考模板）..."
pandoc /tmp/cover_temp.md complete_paper.md \
    -o output/test_original.docx \
    --reference-doc="03_（2026年）硕士研究生学位论文格式模板.docx" \
    --toc \
    --toc-depth=3 \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例"

# 测试2: 添加字体变量
echo "测试2: 添加中文字体变量..."
pandoc /tmp/cover_temp.md complete_paper.md \
    -o output/test_with_fonts.docx \
    --reference-doc="03_（2026年）硕士研究生学位论文格式模板.docx" \
    --toc \
    --toc-depth=3 \
    --variable mainfont="SimSun" \
    --variable sansfont="SimHei" \
    --variable monofont="NSimSun" \
    --metadata date="二〇二六年二月" \
    --metadata author="老毕" \
    --metadata title="视觉力学传感器企业战略转型研究——以HSM为例"

# 测试3: 使用不同的模板方法
echo "测试3: 使用自定义reference-doc..."
# 首先创建一个带有明确中文字体设置的模板副本
if [ ! -f "template_with_fonts.docx" ]; then
    echo "创建带有明确字体设置的模板..."
    # 这里可以添加自定义模板创建逻辑
    cp "03_（2026年）硕士研究生学位论文格式模板.docx" "template_with_fonts.docx"
fi

echo ""
echo "测试完成。生成的文件:"
ls -lh output/test_*.docx 2>/dev/null || echo "未找到测试文件"