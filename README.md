# Code Scorer

`code_scorer.py` 是一个 **多语言代码质量评分工具**，支持自动检测代码语言并进行静态评分，帮助开发者快速评估代码质量。

## 功能特点

* ✅ 支持多语言代码分析：

  * Python、Java、Swift、Objective-C、Dart、C、C++、JavaScript、TypeScript、Go
* ✅ 自动检测代码语言（根据文件扩展名或关键字）
* ✅ 代码质量评分维度：

  * 可读性 (Readability)
  * 复杂度 (Complexity)
  * 注释质量 (Comments)
  * 结构设计 (Structure)
  * 代码规范 (Standards)
* ✅ 支持 JSON 格式输出，方便集成 CI/CD 或其他工具
* ✅ 命令行工具，使用简单

---

## 安装

克隆仓库：

```bash
git clone <repository_url>
cd <repository_directory>
```

（可选）安装依赖：

```bash
pip install -r requirements.txt
```

> 本工具主要依赖 Python 标准库，无额外依赖。

---

## 使用方法

命令行运行：

```bash
python code_scorer.py <file_path> [--lang <language>] [--json]
```

### 参数说明

* `<file_path>`: 需要分析的代码文件路径
* `--lang <language>`: 指定语言（如 `python`, `java`, `cpp` 等），默认 `auto` 自动识别
* `--json`: 输出 JSON 格式评分结果

---

### 示例

分析一个 Python 文件：

```bash
python code_scorer.py example.py --lang python
```

自动检测语言：

```bash
python code_scorer.py example.swift
```

输出 JSON 格式：

```bash
python code_scorer.py code_scorer.py --json
```

---

## 输出示例

### 默认输出（文本形式）

```
文件: example.py
语言: python
总分: 83/100

详细评分:
- 可读性(Readability): 20/25
- 复杂度(Complexity): 18/20
- 注释质量(Comments): 15/20
- 结构设计(Structure): 15/20
- 代码规范(Standards): 15/15
```

### JSON 输出

```json
{
  "file": "example.py",
  "language": "python",
  "score": 83,
  "details": {
    "readability": 20,
    "complexity": 18,
    "comments": 15,
    "structure": 15,
    "standards": 15
  }
}
```

---

## 支持的语言

* Python (`.py`)
* Java (`.java`)
* Swift (`.swift`)
* Objective-C (`.m`, `.mm`)
* Dart (`.dart`)
* C (`.c`)
* C++ (`.cpp`, `.cc`)
* JavaScript (`.js`)
* TypeScript (`.ts`)
* Go (`.go`)

---

## 贡献

欢迎提交 Issue 或 Pull Request，改进评分算法或扩展支持语言。

---

## 许可证

MIT License

## 关于作者
- 官网：[https://zfjsafe.com](https://zfjsafe.com/)
- 博客：[https://zfj1128.blog.csdn.net](https://zfj1128.blog.csdn.net/)
- Github：[https://github.com/zfjsyqk](https://github.com/zfjsyqk/)
- Gitee：[https://gitee.com/zfj1128](https://gitee.com/zfj1128/)
- 打赏：[https://zfjsafe.com/paycode](https://zfjsafe.com/paycode/)
