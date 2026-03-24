#!/usr/bin/env python3
"""
Memory Hygiene - Clean and optimize LanceDB vector memory
Based on: https://github.com/xdylanbaker/memory-hygiene
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

# 配置
LANCEDB_PATH = Path.home() / ".clawdbot" / "memory" / "lancedb"
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
STATE_FILE = WORKSPACE / "memory" / "evolution" / "memory_hygiene_state.json"

# 大小阈值（超过此值触发清理）
SIZE_THRESHOLD_MB = 100


def get_dir_size(path):
    """获取目录大小（MB）"""
    if not path.exists():
        return 0
    total = 0
    for entry in path.rglob("*"):
        if entry.is_file():
            total += entry.stat().st_size
    return total / (1024 * 1024)  # 转换为 MB


def extract_key_facts(memory_file):
    """从 MEMORY.md 提取关键事实"""
    if not memory_file.exists():
        return []
    
    facts = []
    with open(memory_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 简单提取：找到重要的段落（以 ## 或 ### 开头）
    lines = content.split('\n')
    current_section = ""
    
    for line in lines:
        if line.startswith('## '):
            current_section = line[3:].strip()
        elif line.startswith('### '):
            current_section = line[4:].strip()
        elif line.strip() and not line.startswith('#'):
            # 提取重要信息（包含关键词的行）
            keywords = ['规则', '准则', '要求', '偏好', '路径', '密码', '用户', '服务器', '域名']
            if any(kw in line for kw in keywords):
                facts.append({
                    'section': current_section,
                    'text': line.strip()[:100]  # 限制长度
                })
    
    return facts[:20]  # 最多 20 条


def clean_memory(dry_run=False):
    """清理向量记忆数据库"""
    print("🔍 Memory Hygiene - 向量记忆清理")
    print("=" * 50)
    
    # 1. 检查 LanceDB 大小
    size_mb = get_dir_size(LANCEDB_PATH)
    print(f"📊 LanceDB 大小: {size_mb:.2f} MB")
    
    if not LANCEDB_PATH.exists():
        print("✅ LanceDB 目录不存在，无需清理")
        return
    
    # 2. 检查是否需要清理
    if size_mb < SIZE_THRESHOLD_MB:
        print(f"✅ 记忆库大小正常（阈值: {SIZE_THRESHOLD_MB} MB）")
        return
    
    # 3. 提取关键事实
    print(f"\n📝 提取关键事实...")
    facts = extract_key_facts(MEMORY_FILE)
    print(f"   发现 {len(facts)} 条关键事实")
    
    if dry_run:
        print("\n🔍 DRY RUN: 将执行以下操作：")
        print(f"   1. 备份 LanceDB ({size_mb:.2f} MB)")
        print(f"   2. 删除 LanceDB")
        print(f"   3. 重新存储 {len(facts)} 条关键事实")
        return
    
    # 4. 备份并清理
    print(f"\n🧹 清理 LanceDB...")
    backup_path = LANCEDB_PATH.parent / f"lancedb_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # 备份
        shutil.copytree(LANCEDB_PATH, backup_path)
        print(f"   ✅ 已备份到: {backup_path}")
        
        # 删除
        shutil.rmtree(LANCEDB_PATH)
        print(f"   ✅ 已删除 LanceDB")
        
        # 创建状态文件
        state = {
            "last_clean": datetime.now().isoformat(),
            "size_before_mb": size_mb,
            "facts_extracted": len(facts),
            "backup_path": str(backup_path)
        }
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"\n✅ 清理完成！")
        print(f"   原大小: {size_mb:.2f} MB")
        print(f"   关键事实: {len(facts)} 条")
        print(f"   备份位置: {backup_path}")
        
    except Exception as e:
        print(f"❌ 清理失败: {e}")
        # 恢复备份
        if backup_path.exists():
            shutil.copytree(backup_path, LANCEDB_PATH)
            print(f"   ✅ 已从备份恢复")


def show_stats():
    """显示记忆统计"""
    print("\n📊 记忆统计")
    print("=" * 50)
    
    # LanceDB 大小
    size_mb = get_dir_size(LANCEDB_PATH)
    print(f"LanceDB: {size_mb:.2f} MB")
    
    # 检查状态文件
    if STATE_FILE.exists():
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
        print(f"上次清理: {state.get('last_clean', 'N/A')}")
        print(f"清理前大小: {state.get('size_before_mb', 0):.2f} MB")
    
    # MEMORY.md 大小
    if MEMORY_FILE.exists():
        mem_size = MEMORY_FILE.stat().st_size / 1024
        print(f"MEMORY.md: {mem_size:.2f} KB")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "clean":
            dry_run = "--dry-run" in sys.argv
            clean_memory(dry_run)
        elif sys.argv[1] == "stats":
            show_stats()
        else:
            print("用法: memory_hygiene.py [clean|stats] [--dry-run]")
    else:
        # 默认显示统计
        show_stats()
        print("\n使用 'memory_hygiene.py clean' 清理记忆库")
