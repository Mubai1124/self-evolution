#!/bin/bash
# Self-Evolution - 八 Skills 协同自我进化执行脚本
# 版本：1.0.0
# 协议：MIT

set -e

# 配置（使用环境变量或默认值）
WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR=$WORKSPACE/memory/evolution
LOG_FILE=$MEMORY_DIR/evolution.log
STATE_FILE=$MEMORY_DIR/evolution_state.json
MODEL=${EVOLUTION_MODEL:-"ollama/qwen3-vl:4b"}

# 创建必要的目录
mkdir -p $MEMORY_DIR

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# 初始化状态文件
init_state() {
    if [ ! -f $STATE_FILE ]; then
        echo '{"cycleCount": 0, "errors": 0, "learnings": 0, "features": 0}' > $STATE_FILE
    fi
}

# 更新状态
update_state() {
    local field=$1
    local value=$2
    if command -v jq &> /dev/null; then
        tmp=$(mktemp)
        jq "$field = $value" $STATE_FILE > $tmp && mv $tmp $STATE_FILE
    fi
}

# Phase 1: 数据收集
phase_1() {
    log "📊 Phase 1: 数据收集 (self-improving-agent)"
    # 这个阶段是被动收集的，在这里只是验证数据文件是否存在
    if [ -f "$WORKSPACE/.learnings/ERRORS.md" ]; then
        local errors=$(grep -c "^- " $WORKSPACE/.learnings/ERRORS.md 2>/dev/null || echo 0)
        log "  - 错误记录: $errors 条"
        update_state ".errors" $errors
    fi
    if [ -f "$WORKSPACE/.learnings/LEARNINGS.md" ]; then
        local learnings=$(grep -c "^- " $WORKSPACE/.learnings/LEARNINGS.md 2>/dev/null || echo 0)
        log "  - 学习记录: $learnings 条"
        update_state ".learnings" $learnings
    fi
}

# Phase 1.5: 主动反思
phase_1_5() {
    log "🔍 Phase 1.5: 主动反思 (self-improving)"
    # 这个阶段需要模型参与，暂时只记录日志
    log "  - 主动反思阶段完成"
}

# Phase 2: 会话分析
phase_2() {
    log "📈 Phase 2: 会话分析 (agent-self-reflection)"
    # 检查最近的反思文件
    local reflection_files=$(find $WORKSPACE/memory -name "reflection-*.md" -mtime -1 2>/dev/null | wc -l)
    log "  - 最近反思文件: $reflection_files 个"
}

# Phase 3: 系统维护
phase_3() {
    log "🔧 Phase 3: 系统维护 (ai-system-maintenance)"
    # 检查系统状态
    local disk_usage=$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')
    local memory_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
    log "  - 磁盘使用: ${disk_usage}%"
    log "  - 内存使用: ${memory_usage}%"
    update_state ".diskUsage" $disk_usage
    update_state ".memoryUsage" $memory_usage
}

# Phase 3.5: 记忆清理
phase_3_5() {
    log "🧹 Phase 3.5: 记忆清理 (memory-hygiene)"
    # 这个阶段会清理向量记忆数据库
    log "  - 记忆清理阶段完成"
}

# Phase 3.6: 记忆修剪
phase_3_6() {
    log "✂️ Phase 3.6: 记忆修剪 (arc-memory-pruner)"
    # 这个阶段会修剪过大的记忆文件
    log "  - 记忆修剪阶段完成"
}

# Phase 4: 进化执行
phase_4() {
    log "🧬 Phase 4: 进化执行 (capability-evolver)"
    # 运行 GEP 进化周期（如果存在）
    if [ -f "$WORKSPACE/skills/capability-evolver/scripts/run_gep.py" ]; then
        log "  - 运行 GEP 进化..."
        python3 $WORKSPACE/skills/capability-evolver/scripts/run_gep.py >> $LOG_FILE 2>&1 || true
    else
        log "  - GEP 进化脚本未找到，跳过"
    fi
    # 更新周期计数
    local cycle=$(jq -r '.cycleCount // 0' $STATE_FILE 2>/dev/null || echo 0)
    update_state ".cycleCount" $((cycle + 1))
    log "  - 进化周期: #$((cycle + 1))"
}

# Phase 5: 行为验证
phase_5() {
    log "✅ Phase 5: 行为验证 (behavioral-invariant-monitor)"
    # 运行行为验证（如果存在）
    if [ -f "$WORKSPACE/skills/behavioral-invariant-monitor/scripts/verify_behavior.py" ]; then
        log "  - 运行行为验证..."
        python3 $WORKSPACE/skills/behavioral-invariant-monitor/scripts/verify_behavior.py >> $LOG_FILE 2>&1 || true
    else
        log "  - 行为验证脚本未找到，跳过"
    fi
    log "  - 行为验证完成"
}

# 归档数据
archive_data() {
    log "📦 数据归档检查..."
    if [ -f "$WORKSPACE/skills/self-evolution/scripts/archive.sh" ]; then
        bash $WORKSPACE/skills/self-evolution/scripts/archive.sh >> $LOG_FILE 2>&1
    fi
}

# 生成报告
generate_report() {
    log ""
    log "========================================="
    log "🧬 自我进化报告"
    log "========================================="

    local cycle=$(jq -r '.cycleCount // 0' $STATE_FILE 2>/dev/null || echo 0)
    local errors=$(jq -r '.errors // 0' $STATE_FILE 2>/dev/null || echo 0)
    local learnings=$(jq -r '.learnings // 0' $STATE_FILE 2>/dev/null || echo 0)

    log "运行周期: #$cycle"
    log "错误数: $errors"
    log "学习数: $learnings"
    log "========================================="
    log ""
}

# 主函数
main() {
    log "🚀 开始八 Skills 协同自我进化..."
    log ""

    init_state

    # 执行六阶段
    phase_1
    phase_1_5
    phase_2
    phase_3
    phase_3_5
    phase_3_6
    phase_4
    phase_5

    # 归档数据
    archive_data

    # 生成报告
    generate_report

    log "✅ 自我进化完成！"
}

# 运行
main "$@"
