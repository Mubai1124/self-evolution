#!/usr/bin/env python3
"""
Self-Reflection Script - Phase 1.5 of Self-Evolution
使用 LCM 分析最近对话，提取学习模式
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# 路径配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
LEARNINGS_FILE = WORKSPACE / ".learnings" / "LEARNINGS.md"
ERRORS_FILE = WORKSPACE / ".learnings" / "ERRORS.md"
MEMORY_FILE = Path.home() / "self-improving" / "memory.md"
CORRECTIONS_FILE = Path.home() / "self-improving" / "corrections.md"
STATE_FILE = WORKSPACE / "memory" / "evolution" / "reflection_state.json"

def load_state():
    """加载反思状态"""
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "last_reflection": None,
        "patterns_found": 0,
        "learnings_added": 0
    }

def save_state(state):
    """保存反思状态"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def analyze_recent_sessions():
    """分析最近的会话文件，提取学习模式"""
    sessions_dir = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
    if not sessions_dir.exists():
        return []
    
    # 获取最近 24 小时的会话文件
    recent_files = []
    cutoff = datetime.now() - timedelta(hours=24)
    
    for f in sessions_dir.glob("*.jsonl"):
        mtime = datetime.fromtimestamp(f.stat().st_mtime)
        if mtime > cutoff:
            recent_files.append(f)
    
    if not recent_files:
        return []
    
    patterns = []
    
    for session_file in recent_files:
        try:
            with open(session_file, 'r') as f:
                for line in f:
                    try:
                        msg = json.loads(line.strip())
                        
                        # 检查是否是消息类型
                        if msg.get('type') != 'message':
                            continue
                        
                        message = msg.get('message', {})
                        role = message.get('role', '')
                        content_array = message.get('content', [])
                        
                        # 提取文本内容
                        content = ''
                        for item in content_array:
                            if item.get('type') == 'text':
                                content = item.get('text', '')
                                break
                        
                        # 跳过太短的消息
                        if len(content) < 50:
                            continue
                        
                        # 检测错误模式
                        if 'error' in content.lower() or 'failed' in content.lower():
                            if role == 'user':
                                patterns.append({
                                    "type": "error",
                                    "content": content[:500],
                                    "source": "session"
                                })
                        
                        # 检测用户纠正
                        correction_keywords = ['不对', '错了', '应该是', 'actually', 'wrong', 'no,', '不是', '修改', '改一下', '不对', '修正']
                        if any(kw in content.lower() for kw in correction_keywords):
                            if role == 'user':
                                patterns.append({
                                    "type": "correction",
                                    "content": content[:500],
                                    "source": "session"
                                })
                        
                        # 检测用户偏好
                        preference_keywords = ['我喜欢', '我讨厌', 'prefer', 'always do', 'never do', '记得', '记住', '以后', '以后都', '以后要', '以后不要', '希望', '想要', '不要']
                        if any(kw in content.lower() for kw in preference_keywords):
                            if role == 'user':
                                patterns.append({
                                    "type": "preference",
                                    "content": content[:500],
                                    "source": "session"
                                })
                        
                        # 检测问题/疑问（可能需要改进）
                        question_keywords = ['为什么', '怎么', '如何', 'why', 'how', 'what']
                        if any(kw in content.lower() for kw in question_keywords):
                            if role == 'user' and len(content) > 100:
                                patterns.append({
                                    "type": "question",
                                    "content": content[:500],
                                    "source": "session"
                                })
                    
                    except json.JSONDecodeError:
                        continue
        
        except Exception as e:
            print(f"Error reading {session_file}: {e}", file=sys.stderr)
    
    return patterns

def extract_learning_from_pattern(pattern):
    """从模式中提取学习内容"""
    content = pattern.get('content', '')
    ptype = pattern.get('type', '')
    
    # 简单的学习提取
    if ptype == 'correction':
        # 尝试提取纠正的内容
        return {
            "category": "correction",
            "learning": content[:200],
            "timestamp": datetime.now().isoformat()
        }
    elif ptype == 'preference':
        return {
            "category": "preference",
            "learning": content[:200],
            "timestamp": datetime.now().isoformat()
        }
    elif ptype == 'error':
        return {
            "category": "error",
            "learning": content[:200],
            "timestamp": datetime.now().isoformat()
        }
    
    return None

def write_learning(learning):
    """写入学习到 LEARNINGS.md"""
    LEARNINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 创建文件如果不存在
    if not LEARNINGS_FILE.exists():
        with open(LEARNINGS_FILE, 'w') as f:
            f.write("# Learnings Log\n\nRecord important learnings, corrections, and best practices here.\n\n")
    
    # 追加学习
    with open(LEARNINGS_FILE, 'a') as f:
        timestamp = learning.get('timestamp', datetime.now().isoformat())
        category = learning.get('category', 'unknown')
        content = learning.get('learning', '')
        
        f.write(f"\n### [{timestamp}] 自动反思发现 ({category})\n")
        f.write(f"- **Category**: {category}\n")
        f.write(f"- **Source**: 自动反思\n")
        f.write(f"- **Learning**: {content}\n")
        f.write(f"- **Impact**: 需要人工确认\n")

def write_correction(learning):
    """写入纠正到 corrections.md"""
    CORRECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # 创建文件如果不存在
    if not CORRECTIONS_FILE.exists():
        with open(CORRECTIONS_FILE, 'w') as f:
            f.write("# Corrections Log\n\n")
    
    # 追加纠正
    with open(CORRECTIONS_FILE, 'a') as f:
        timestamp = learning.get('timestamp', datetime.now().isoformat())
        content = learning.get('learning', '')
        
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} — 自动反思发现\n")
        f.write(f"- **Correction**: {content[:100]}\n")
        f.write(f"- **Context**: 自动分析会话\n")
        f.write(f"- **Count**: 1\n")

def main():
    """主函数"""
    print("🔍 开始主动反思...")
    
    # 加载状态
    state = load_state()
    
    # 分析最近会话
    patterns = analyze_recent_sessions()
    
    if not patterns:
        print("  - 未发现新的学习模式")
        # 即使没有发现模式，也要更新状态
        state["last_reflection"] = datetime.now().isoformat()
        save_state(state)
        return
    
    print(f"  - 发现 {len(patterns)} 个潜在学习模式")
    
    # 提取学习
    learnings_added = 0
    for pattern in patterns[:5]:  # 限制每次最多 5 个
        learning = extract_learning_from_pattern(pattern)
        if learning:
            write_learning(learning)
            
            # 如果是纠正，也写入 corrections.md
            if learning.get('category') == 'correction':
                write_correction(learning)
            
            learnings_added += 1
    
    # 更新状态
    state["last_reflection"] = datetime.now().isoformat()
    state["patterns_found"] = state.get("patterns_found", 0) + len(patterns)
    state["learnings_added"] = state.get("learnings_added", 0) + learnings_added
    save_state(state)
    
    print(f"  - 添加了 {learnings_added} 条学习记录")
    print(f"  - 累计发现 {state['patterns_found']} 个模式")

if __name__ == "__main__":
    main()
