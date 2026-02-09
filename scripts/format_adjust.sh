#!/bin/bash

cd "/workspace/论文/视觉力学传感器企业战略转型研究-HSM"

case "$1" in
    --double-spacing)
        echo "生成2倍行距版本..."
        pandoc cover_text.md complete_paper.md -o output/双倍行距版.docx --toc --toc-depth=3 -V line-spacing=2.0
        echo "已生成: output/双倍行距版.docx"
        ;;
    --single-spacing)
        echo "生成单倍行距版本..."
        pandoc cover_text.md complete_paper.md -o output/单倍行距版.docx --toc --toc-depth=3 -V line-spacing=1.0
        echo "已生成: output/单倍行距版.docx"
        ;;
    --margin-2cm)
        echo "生成2cm页边距版本..."
        pandoc cover_simple.md complete_paper.md -o output/2cm边距版.pdf --pdf-engine=xelatex --toc --toc-depth=3 -V mainfont="Noto Serif CJK SC" -V geometry:a4paper,margin=2cm
        echo "已生成: output/2cm边距版.pdf"
        ;;
    --margin-3cm)
        echo "生成3cm页边距版本..."
        pandoc cover_simple.md complete_paper.md -o output/3cm边距版.pdf --pdf-engine=xelatex --toc --toc-depth=3 -V mainfont="Noto Serif CJK SC" -V geometry:a4paper,margin=3cm
        echo "已生成: output/3cm边距版.pdf"
        ;;
    --font-size-11)
        echo "生成11pt字体版本..."
        pandoc cover_simple.md complete_paper.md -o output/11pt字体版.pdf --pdf-engine=xelatex --toc --toc-depth=3 -V mainfont="Noto Serif CJK SC" -V fontsize=11pt -V geometry:a4paper,margin=2.5cm
        echo "已生成: output/11pt字体版.pdf"
        ;;
    --font-size-13)
        echo "生成13pt字体版本..."
        pandoc cover_simple.md complete_paper.md -o output/13pt字体版.pdf --pdf-engine=xelatex --toc --toc-depth=3 -V mainfont="Noto Serif CJK SC" -V fontsize=13pt -V geometry:a4paper,margin=2.5cm
        echo "已生成: output/13pt字体版.pdf"
        ;;
    --custom)
        echo "交互式格式调整"
        read -p "行距 (1.0, 1.5, 2.0): " line_spacing
        read -p "字体大小 (10, 11, 12, 13, 14): " font_size
        read -p "页边距 (cm): " margin
        read -p "输出文件名 (不含扩展名): " filename
        
        echo "生成自定义格式版本..."
        pandoc cover_text.md complete_paper.md -o "output/${filename}.docx" --toc --toc-depth=3 -V line-spacing=${line_spacing} -V fontsize=${font_size}pt
        
        pandoc cover_simple.md complete_paper.md -o "output/${filename}.pdf" --pdf-engine=xelatex --toc --toc-depth=3 -V mainfont="Noto Serif CJK SC" -V fontsize=${font_size}pt -V geometry:a4paper,margin=${margin}cm
        
        echo "已生成: output/${filename}.docx 和 output/${filename}.pdf"
        ;;
    *)
        echo "格式调整脚本"
        echo "用法: bash format_adjust.sh [选项]"
        echo ""
        echo "选项:"
        echo "  --double-spacing    生成2倍行距版本"
        echo "  --single-spacing    生成单倍行距版本"
        echo "  --margin-2cm        生成2cm页边距版本"
        echo "  --margin-3cm        生成3cm页边距版本"
        echo "  --font-size-11      生成11pt字体版本"
        echo "  --font-size-13      生成13pt字体版本"
        echo "  --custom            交互式自定义格式"
        echo ""
        echo "示例:"
        echo "  bash format_adjust.sh --double-spacing"
        echo "  bash format_adjust.sh --custom"
        ;;
esac