# 贡献指南

感谢你考虑为 Self-Evolution 项目做出贡献！

## 🤔 如何贡献

### 报告问题

如果你发现了 bug 或有功能建议：

1. 在 [GitHub Issues](https://github.com/your-username/self-evolution/issues) 中搜索，确认问题未被报告
2. 创建新 Issue，包含：
   - 清晰的标题
   - 详细的问题描述
   - 复现步骤（如果是 bug）
   - 期望行为
   - 实际行为
   - 系统环境信息

### 提交代码

1. **Fork 仓库**
   ```bash
   git clone https://github.com/your-username/self-evolution.git
   cd self-evolution
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **进行修改**
   - 遵循现有代码风格
   - 添加必要的注释
   - 更新相关文档

4. **测试修改**
   ```bash
   # 运行进化脚本测试
   ./scripts/evolve.sh
   
   # 运行归档脚本测试
   ./scripts/archive.sh
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

6. **推送到 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 清晰描述更改内容
   - 关联相关 Issue
   - 等待代码审查

## 📝 代码规范

### Bash 脚本

- 使用 `set -e` 在脚本开头
- 使用有意义的变量名
- 添加必要的注释
- 使用 `log()` 函数记录日志
- 错误处理要完善

### 文档

- Markdown 格式
- 清晰的标题和子标题
- 代码示例要完整可运行
- 保持简洁明了

## 🏗️ 开发路线图

### 短期目标

- [ ] 添加更详细的日志输出
- [ ] 支持自定义进化策略
- [ ] 改进错误处理机制
- [ ] 添加单元测试

### 中期目标

- [ ] Web UI 查看进化历史
- [ ] 集成更多 AI 模型
- [ ] 支持分布式进化
- [ ] 添加进化回滚机制

### 长期目标

- [ ] 云端部署支持
- [ ] 多语言文档
- [ ] 社区插件系统

## 🧪 测试

### 测试环境

确保你有以下依赖：

- Bash 4.0+
- `jq` (JSON 处理)
- Python 3.x (GEP 进化)

### 运行测试

```bash
# 测试进化脚本
./scripts/evolve.sh

# 测试归档脚本
./scripts/archive.sh

# 检查日志
cat ~/.openclaw/workspace/memory/evolution/evolution.log
```

## 📖 文档贡献

文档改进也是重要的贡献：

- 修复拼写错误
- 改进示例代码
- 添加使用场景
- 翻译文档

## 🙏 行为准则

- 尊重所有贡献者
- 接受建设性批评
- 专注于对项目最有利的事情
- 对社区表现出同理心和友善

## 📮 联系方式

- 问题反馈：[GitHub Issues](https://github.com/your-username/self-evolution/issues)
- 功能建议：[GitHub Discussions](https://github.com/your-username/self-evolution/discussions)

---

再次感谢你的贡献！💜
