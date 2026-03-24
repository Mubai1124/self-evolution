---
name: self-evolution
description: 八 Skills 协同自我进化系统。自动化运行六阶段进化流程：数据收集 → 主动反思 → 会话分析 → 系统维护 → 进化执行 → 行为验证。支持手动触发和定时运行。
tags:
  - evolution
  - self-improvement
  - automation
  - orchestration
---

# Self-Evolution - 八 Skills 协同自我进化系统

## 概述

这是一个编排型 Skill，负责协调八个专门的 Skills 完成六阶段的自我进化流程。

## 八个协同 Skills

| # | Skill | 类型 | 阶段 | 职责 |
|---|-------|------|------|------|
| 1 | self-improving-agent | 核心 | Phase 1 | 被动收集错误与学习记录 |
| 2 | self-improving | 核心 | Phase 1.5 | 主动式自我反思与批评 |
| 3 | agent-self-reflection | 核心 | Phase 2 | 反思近期会话，提取洞察 |
| 4 | ai-system-maintenance | 核心 | Phase 3 | 系统健康检查与维护 |
| 5 | memory-hygiene | 支持 | Phase 3.5 | 清理优化向量记忆 |
| 6 | arc-memory-pruner | 支持 | Phase 3.6 | 自动修剪记忆文件 |
| 7 | capability-evolver | 核心 | Phase 4 | 自动进化与修复 |
| 8 | behavioral-invariant-monitor | 验证 | Phase 5 | 验证行为一致性，检测漂移 |

## 六阶段进化流程

```
┌──────────────────────────────────────────────────────┐
│              六阶段协同进化流程                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Phase 1: self-improving-agent (被动)               │
│  └─ 收集 ERRORS.md / LEARNINGS.md                   │
│                                                      │
│  Phase 1.5: self-improving (主动)                   │
│  └─ 主动式自我反思与批评                             │
│                                                      │
│  Phase 2: agent-self-reflection                     │
│  └─ 分析近期会话，提取洞察                           │
│                                                      │
│  Phase 3: ai-system-maintenance                     │
│  └─ 检查磁盘/内存/GPU，验证服务状态                  │
│                                                      │
│  Phase 3.5: memory-hygiene                          │
│  └─ 清理向量记忆数据库                               │
│                                                      │
│  Phase 3.6: arc-memory-pruner                       │
│  └─ 自动修剪过大的记忆文件                           │
│                                                      │
│  Phase 4: capability-evolver                        │
│  └─ 分析所有信号，执行进化                           │
│                                                      │
│  Phase 5: behavioral-invariant-monitor              │
│  └─ 验证进化后的行为一致性                           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

## 使用方法

### 手动触发

```
运行自我进化
```

或更明确地：

```
使用 self-evolution skill 运行完整的六阶段进化流程
```

### 定时运行（推荐）

在 OpenClaw 中配置 Cron 任务：

```bash
# 每天早上 6:00 和晚上 18:00 运行自我进化
0 6,18 * * * ~/.openclaw/skills/self-evolution/scripts/evolve.sh
```

## 配置

配置文件位置：`~/.openclaw/skills/self-evolution/.env`

```env
# 进化配置
EVOLUTION_MODEL=ollama/qwen3-vl:4b
EVOLUTION_INTERVAL_HOURS=12
EVOLUTION_AUTO_RUN=true

# 各阶段开关
PHASE_1_ENABLED=true
PHASE_1_5_ENABLED=true
PHASE_2_ENABLED=true
PHASE_3_ENABLED=true
PHASE_3_5_ENABLED=true
PHASE_3_6_ENABLED=true
PHASE_4_ENABLED=true
PHASE_5_ENABLED=true

# 通知配置
NOTIFY_ON_EVOLUTION=true
NOTIFY_ON_ERROR=true
NOTIFY_CHANNEL=telegram
```

## 输出

每次进化运行后，会生成报告：

- **状态文件**：`~/.openclaw/workspace/memory/evolution/evolution_state.json`
- **进化日志**：`~/.openclaw/workspace/memory/evolution/evolution.log`
- **进化胶囊**：`~/.openclaw/workspace/skills/capability-evolver/assets/gep/`

## 数据管理

### 自动归档

| 文件 | 触发条件 | 操作 |
|------|----------|------|
| ERRORS.md | > 300 行 | 归档到 `archive/`，保留最近 50 行 |
| LEARNINGS.md | > 500 行 | 归档到 `archive/`，保留最近 50 行 |

### 重要内容保护

归档脚本会自动检测标记为"重要"的学习，提示用户手动提取到长期记忆。

## 最佳实践

1. **定期运行**：建议每天运行 2 次（早上和晚上）
2. **监控日志**：定期检查进化日志，确保没有异常
3. **人工审查**：重大进化（如新增 Skill）应该人工审查
4. **备份数据**：进化前自动备份关键数据
5. **回滚准备**：确保有回滚机制

## 注意事项

- 进化过程可能需要 5-15 分钟
- 运行期间会占用一定的 CPU 和内存
- 建议在空闲时段运行
- 进化失败不会影响正常功能

---

*版本：1.0.0*
*协议：MIT*
