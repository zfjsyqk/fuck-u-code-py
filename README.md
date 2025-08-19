# Code Scorer

`code_scorer.py` 是一个用于自动分析和评分代码质量的工具，支持多语言代码的静态分析，并提供详细的评分维度和报告。

## 功能

* 支持多种编程语言（通过 `--lang` 参数指定，默认为自动识别）
* 对代码进行评分，涵盖：

  * 可读性
  * 代码规范
  * 复杂度
  * 注释质量
  * 结构设计
* 输出 JSON 格式评分结果，便于进一步处理或集成

## 安装

确保已安装 Python 3.8+，然后克隆本仓库：

```bash
git clone <repository_url>
cd <repository_directory>
pip install -r requirements.txt
```

## 使用方法

基本用法：

```bash
python code_scorer.py <file_path> --lang auto --json
```

示例：

```bash
python code_scorer.py code_scorer.py --lang python --json
```

参数说明：

* `<file_path>`: 需要评分的代码文件路径
* `--lang`: 指定语言（如 `python`, `dart`, `cpp` 等），`auto` 表示自动检测
* `--json`: 输出 JSON 格式评分结果

## 输出示例

```json
{
  "file": "example.py",
  "score": 85,
  "details": {
    "readability": 20,
    "complexity": 18,
    "comments": 15,
    "structure": 17,
    "standards": 15
  }
}
```

## 贡献

欢迎提交 Issue 或 Pull Request，对代码评分算法或支持语言进行优化。
