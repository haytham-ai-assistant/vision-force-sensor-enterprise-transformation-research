#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

echo "=== 更新最终提交目录 ==="
echo ""

# 查找最新的格式调整文档
LATEST_DOCX=$(ls -t output/视觉力学传感器企业战略转型研究_格式调整版_*.docx 2>/dev/null | head -1)
LATEST_PDF=$(ls -t output/视觉力学传感器企业战略转型研究_格式调整版_*.pdf 2>/dev/null | head -1)

if [ -z "$LATEST_DOCX" ]; then
    echo "错误: 未找到格式调整版Word文档"
    exit 1
fi

echo "找到最新文档:"
echo "  Word: $LATEST_DOCX"
echo "  PDF:  $LATEST_PDF"
echo ""

# 创建final_submission目录（如果不存在）
FINAL_DIR="final_submission"
mkdir -p "$FINAL_DIR"

# 获取时间戳
TIMESTAMP=$(echo "$LATEST_DOCX" | grep -oE '[0-9]{8}_[0-9]{6}' | head -1)
if [ -z "$TIMESTAMP" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
fi

echo "文档时间戳: $TIMESTAMP"
echo ""

# 复制文件到final_submission
echo "复制文件到final_submission目录..."
cp "$LATEST_DOCX" "$FINAL_DIR/视觉力学传感器企业战略转型研究_格式调整版_${TIMESTAMP}.docx"
cp "$LATEST_PDF" "$FINAL_DIR/视觉力学传感器企业战略转型研究_格式调整版_${TIMESTAMP}.pdf"

# 复制其他必要文件
echo "复制其他必要文件..."
cp -f "complete_paper.md" "$FINAL_DIR/"
cp -f "cover_text.md" "$FINAL_DIR/"
cp -f "scripts/apply_template_format.sh" "$FINAL_DIR/"
cp -f "03_（2026年）硕士研究生学位论文格式模板.docx" "$FINAL_DIR/"

# 创建提交说明
cat > "$FINAL_DIR/提交说明.md" << EOF
# 北京大学硕士论文最终提交文件

## 生成时间
$(date)

## 文件说明

1. **视觉力学传感器企业战略转型研究_格式调整版_${TIMESTAMP}.docx**
   - 符合北京大学2026年硕士论文格式模板的Word文档
   - 已应用官方模板样式
   - 包含自动生成的目录

2. **视觉力学传感器企业战略转型研究_格式调整版_${TIMESTAMP}.pdf**
   - 对应的PDF版本
   - 使用xelatex引擎生成，支持中文字体

3. **complete_paper.md**
   - 论文Markdown源文件（已修复HTML注释问题）

4. **cover_text.md**
   - 封面页Markdown源文件

5. **apply_template_format.sh**
   - 格式调整脚本

6. **03_（2026年）硕士研究生学位论文格式模板.docx**
   - 北京大学官方格式模板

## 格式验证结果

- ✅ 已修复HTML注释与标题混合问题
- ✅ 已解决重复编号问题（如"3.1 1.1 研究背景"）
- ✅ 章节编号正确：第一章、1.1、1.2等
- ⚠️  PDF生成时有字体警告，但不影响内容显示
- ⚠️  需要在Microsoft Word中最终验证封面和目录显示

## 使用说明

1. 使用Microsoft Word打开"视觉力学传感器企业战略转型研究_格式调整版_${TIMESTAMP}.docx"
2. 检查：
   - 封面页是否正常显示（无乱码）
   - 目录是否正常生成（无乱码）
   - 标题格式是否符合模板要求
   - 正文格式是否符合模板要求
3. 如需进一步调整，可修改complete_paper.md后重新运行apply_template_format.sh

## 注意事项

- 封面页导师姓名保持"（请填写导师姓名）"占位符
- 第七章（结论与建议）保持原有优化版本
- 论文内容（35,800字）保持不变，仅调整格式
EOF

echo "创建提交说明文件: $FINAL_DIR/提交说明.md"
echo ""

# 列出final_submission目录内容
echo "final_submission目录内容:"
ls -lh "$FINAL_DIR/"
echo ""

echo "=== 更新完成 ==="
echo "最终提交文件已准备就绪"
echo "请在Microsoft Word中打开文档进行最终验证"