#!/usr/bin/env python3
"""
Memory Pruner - Keep agent memory lean
Automatically prune logs, compact state files, and enforce size limits.
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime


def get_file_stats(file_path):
    """Get file statistics"""
    path = Path(file_path).expanduser()
    if not path.exists():
        return None
    
    stat = path.stat()
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    return {
        'path': str(path),
        'size': stat.st_size,
        'size_human': format_size(stat.st_size),
        'lines': len(lines),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
    }


def format_size(size):
    """Format size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}TB"


def prune_file(file_path, max_lines, dry_run=False):
    """Prune file to keep only last N lines"""
    path = Path(file_path).expanduser()
    if not path.exists():
        print(f"❌ File not found: {path}")
        return False
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    total_lines = len(lines)
    if total_lines <= max_lines:
        print(f"✅ {path.name}: {total_lines} lines (under limit {max_lines})")
        return True
    
    # Keep last max_lines
    new_lines = lines[-max_lines:]
    removed_lines = total_lines - max_lines
    
    if dry_run:
        print(f"🔍 DRY RUN: Would prune {path.name}")
        print(f"   Current: {total_lines} lines")
        print(f"   After:   {max_lines} lines")
        print(f"   Removed: {removed_lines} lines")
        return True
    
    # Write pruned content
    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f"✂️ Pruned {path.name}: {total_lines} → {max_lines} lines (removed {removed_lines})")
    return True


def stats_directory(dir_path, pattern="*.md"):
    """Show stats for all memory files in directory"""
    path = Path(dir_path).expanduser()
    if not path.exists():
        print(f"❌ Directory not found: {path}")
        return
    
    print(f"\n📊 Memory Files in {path}")
    print("=" * 60)
    
    total_size = 0
    files = sorted(path.glob(pattern), key=lambda x: x.stat().st_size, reverse=True)
    
    for file in files:
        stats = get_file_stats(file)
        if stats:
            print(f"  {stats['size_human']:>8}  {stats['lines']:>6} lines  {file.name}")
            total_size += stats['size']
    
    print("=" * 60)
    print(f"  Total: {format_size(total_size)} in {len(files)} files")


def main():
    parser = argparse.ArgumentParser(description='Memory Pruner - Keep agent memory lean')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Prune command
    prune_parser = subparsers.add_parser('prune', help='Prune memory files')
    prune_parser.add_argument('--file', '-f', required=True, help='File to prune')
    prune_parser.add_argument('--max-lines', '-n', type=int, default=200, help='Max lines to keep')
    prune_parser.add_argument('--dry-run', action='store_true', help='Preview changes without modifying')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show memory file statistics')
    stats_parser.add_argument('--dir', '-d', default='~/.openclaw/workspace/memory', help='Directory to scan')
    stats_parser.add_argument('--pattern', '-p', default='*.md', help='File pattern')
    
    args = parser.parse_args()
    
    if args.command == 'prune':
        prune_file(args.file, args.max_lines, args.dry_run)
    elif args.command == 'stats':
        stats_directory(args.dir, args.pattern)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
