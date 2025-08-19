# fuck-u-code (Python 版)

> 一款 **轻量级的多语言屎山代码检测工具**。
> 灵感来自 [fuck-u-code (Go 版)](https://github.com/Done-0/fuck-u-code)，
> 用 Python 实现，便于跨平台快速使用，无需额外依赖。

---

## 功能特点

* **多语言支持**：
  Go / JavaScript / TypeScript / Python / Java / C / C++ / Rust / Swift / Objective-C / Dart
* **代码屎山评分**（0 \~ 100，越高越屎）：

  * 循环复杂度
  * 最大嵌套层数
  * 平均函数长度
  * 注释覆盖率
  * 命名异味（过短/过长/全大写变量）
  * 重复度（滑动窗口重复块）
  * 错误处理令牌（try/except/catch/throw …）
*  **多种输出格式**：

  * 彩色终端摘要/详细视图
  * Markdown 报告（适合 CI/CD 或文档）
*  **灵活控制**：

  * 排除文件/目录
  * 跳过 `index.js/ts` 等文件
  * 仅显示前 N 个最烂文件
  * 中英文支持

---

## 安装

本工具 **无第三方依赖**，只需 Python 3.8+ 即可运行。

```bash
git clone https://github.com/yourname/fuck-u-code-py.git
cd fuck-u-code-py
```

---

## 使用方法

基本用法：

```bash
python fuck_u_code.py [命令] [选项] [路径]
```

### 常见示例

```bash
# 分析当前目录（默认摘要）
python fuck_u_code.py

# 指定 analyze 命令
python fuck_u_code.py analyze .

# 显示详细报告
python fuck_u_code.py --verbose

# 只看最屎的 3 个文件
python fuck_u_code.py --top 3

# 输出 Markdown 格式（可重定向保存）
python fuck_u_code.py --markdown > report.md

# 英文输出
python fuck_u_code.py --lang en-US --verbose

# 排除路径（支持多次）
python fuck_u_code.py -e "**/test/**" -e "**/dist/**"

# 跳过 index 文件
python fuck_u_code.py --skipindex
```

---

## 参数说明

| 参数                              | 说明                          | 默认值       |
| ------------------------------- | --------------------------- | --------- |
| `路径`                            | 要扫描的文件或目录                   | `.`（当前目录） |
| `--lang`                        | 输出语言（`zh-CN` / `en-US`）     | `zh-CN`   |
| `--verbose`                     | 显示详细报告                      | 关闭        |
| `--markdown`                    | 输出 Markdown 表格              | 关闭        |
| `--top N`                       | 只显示前 N 个最烂文件                | 0（不限制）    |
| `-e PATTERN, --exclude PATTERN` | 排除路径（支持多次）                  | 无         |
| `--skipindex`                   | 跳过 `index.js`/`index.ts` 文件 | 关闭        |

---

## 输出示例

### 终端摘要

```
正在分析 12 个文件...

最屎文件 TOP 3:
1. src/utils/helpers.js  分数: 87 (等级: E)
2. main.py               分数: 72 (等级: D)
3. core/service.go       分数: 65 (等级: C)

平均分: 54/100
```

### 详细模式 (`--verbose`)

```
文件: main.py
语言: python
分数: 72 (等级 D)

指标详情:
- 循环复杂度: 12
- 最大嵌套层数: 5
- 平均函数长度: 48 行
- 注释覆盖率: 8%
- 命名异味: 3 个
- 重复度: 15%
- 错误处理: 1 处

-------------------------------------------------------
```

### Markdown 格式 (`--markdown`)

```markdown
| 文件 | 语言 | 分数 | 等级 | 循环复杂度 | 最大嵌套 | 平均函数行数 | 注释覆盖率 | 异味 | 重复度 | 错误处理 |
|------|------|------|------|------------|----------|--------------|------------|------|--------|----------|
| main.py | python | 72 | D | 12 | 5 | 48 | 8% | 3 | 15% | 1 |
| utils.js | javascript | 87 | E | 15 | 6 | 52 | 5% | 6 | 20% | 0 |
```

---

## 支持语言

* Python (`.py`)
* Go (`.go`)
* Java (`.java`)
* JavaScript (`.js`)
* TypeScript (`.ts`)
* C (`.c`)
* C++ (`.cpp`, `.cc`, `.cxx`)
* Rust (`.rs`)
* Swift (`.swift`)
* Objective-C (`.m`, `.mm`)
* Dart (`.dart`)

---

## 实现原理

* **语言识别**：基于扩展名，简单高效
* **循环复杂度**：统计 `if/for/while/switch/&&/||` 等关键字
* **最大嵌套**：括号/缩进层次模拟
* **函数行数**：匹配 `def|func|class|void` 等函数定义
* **注释覆盖率**：行数比例（注释行 / 总行）
* **命名异味**：变量名过短/过长/全大写
* **重复度**：滑动窗口（5 行）检测重复
* **错误处理**：`try/catch/throw/except` 出现次数

---

## 贡献

欢迎提 Issue 或 PR 来改进算法、增加语言支持，或优化评分规则。

---

## 许可证

MIT License

## 关于作者
- 官网：[https://zfjsafe.com](https://zfjsafe.com/)
- 博客：[https://zfj1128.blog.csdn.net](https://zfj1128.blog.csdn.net/)
- Github：[https://github.com/zfjsyqk](https://github.com/zfjsyqk/)
- Gitee：[https://gitee.com/zfj1128](https://gitee.com/zfj1128/)
- 打赏：[https://zfjsafe.com/paycode](https://zfjsafe.com/paycode/)
