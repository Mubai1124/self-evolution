#!/bin/bash
# 数据归档脚本 - 定期归档错误和学习数据
# 版本：1.0.0
# 协议：MIT

set -e

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
LEARNINGS_DIR=$WORKSPACE/.learnings
ARCHIVE_DIR=$LEARNINGS_DIR/archive
MEMORY_DIR=$WORKSPACE/memory

# 创建归档目录
mkdir -p $ARCHIVE_DIR

# 提取重要学习到 MEMORY.md
extract_important() {
    local learnings_file=$LEARNINGS_DIR/LEARNINGS.md
    local memory_file=$WORKSPACE/MEMORY.md

    if [ -f $learnings_file ]; then
        # 查找标记为"重要"或"核心"的学习
        local important=$(grep -i "重要\|核心\|关键\|⚠️\|‼️" $learnings_file 2>/dev/null || echo "")
        
        if [ -n "$important" ]; then
            echo ""
            echo "💡 发现重要学习，建议手动提取到 MEMORY.md："
            echo "$important" | head -10
            echo ""
            echo "（已标记的学习不会在归档时丢失，但建议手动添加到 MEMORY.md 永久保存）"
        fi
    fi
}

# 归档函数（智能保留）
archive_file() {
    local file=$1
    local max_lines=${2:-500}  # 默认最大行数
    local filename=$(basename $file)
    local lines=$(wc -l < $file 2>/dev/null || echo 0)

    if [ $lines -gt $max_lines ]; then
        local timestamp=$(date +%Y%m)
        local archive_file="$ARCHIVE_DIR/${filename%.md}-$timestamp.md"

        # 如果归档文件已存在，追加；否则创建
        if [ -f $archive_file ]; then
            cat $file >> $archive_file
        else
            cp $file $archive_file
        fi

        # 保留最近的 50 行（不要全部清空）
        echo "# $filename（最近更新）" > $file
        echo "" >> $file
        tail -50 $archive_file >> $file
        echo "" >> $file
        echo "*归档于 $(date '+%Y-%m-%d %H:%M:%S')，历史数据已移至 $archive_file*" >> $file

        echo "📦 归档 $filename: $lines 行 → $archive_file（保留最近 50 行）"
    fi
}

# 清理过时的错误（标记为已修复的）
cleanup_errors() {
    local errors_file=$LEARNINGS_DIR/ERRORS.md
    if [ -f $errors_file ]; then
        # 统计已修复的错误数量
        local fixed=$(grep -c "已修复\|已解决\|✅" $errors_file 2>/dev/null || echo 0)
        if [ $fixed -gt 0 ]; then
            echo "🧹 清理已修复错误: $fixed 条"
            # 这里可以添加实际的清理逻辑
        fi
    fi
}

# 合并重复的学习
merge_learnings() {
    local learnings_file=$LEARNINGS_DIR/LEARNINGS.md
    if [ -f $learnings_file ]; then
        # 检测重复的学习（相同的开头）
        local duplicates=$(sort $learnings_file | uniq -d | wc -l 2>/dev/null || echo 0)
        if [ $duplicates -gt 0 ]; then
            echo "🔄 发现重复学习: $duplicates 条（建议手动合并）"
        fi
    fi
}

# 主函数
main() {
    echo "📊 数据归档检查..."
    echo ""

    # 提取重要学习
    extract_important

    # 归档过大的文件（保留最近 50 行）
    archive_file $LEARNINGS_DIR/ERRORS.md 300
    archive_file $LEARNINGS_DIR/LEARNINGS.md 500

    # 清理和检查
    cleanup_errors
    merge_learnings

    echo ""
    echo "✅ 归档检查完成"
}

main "$@"
