#!/usr/bin/env python3
import re
import os
import sys
import argparse
import json

# ------------------ 语言映射 ------------------
LANG_KEYWORDS = {
    "python": ["def ", "class ", "import "],
    "java": ["class ", "public ", "void "],
    "swift": ["func ", "class ", "import "],
    "objc": ["@interface", "@implementation"],
    "dart": ["class ", "import ", "void "],
    "cpp": ["#include", "int main", "class "],
    "c": ["#include", "int main"],
    "js": ["function ", "class ", "import "],
    "ts": ["function ", "class ", "import ", "interface"],
    "go": ["package ", "func ", "import "]
}

# ------------------ 检测器核心 ------------------
def detect_language(code: str, filename: str = "") -> str:
    ext_map = {
        ".py": "python", ".java": "java", ".swift": "swift", ".m": "objc",
        ".mm": "objc", ".dart": "dart", ".cpp": "cpp", ".cc": "cpp",
        ".c": "c", ".js": "js", ".ts": "ts", ".go": "go"
    }
    _, ext = os.path.splitext(filename)
    if ext in ext_map:
        return ext_map[ext]
    # fallback by keyword
    for lang, kws in LANG_KEYWORDS.items():
        if any(kw in code for kw in kws):
            return lang
    return "unknown"


def score_code(code: str, language: str = "auto", filename: str = "") -> dict:
    if language == "auto":
        language = detect_language(code, filename)

    lines = code.splitlines()
    n_lines = len(lines)
    avg_len = sum(len(l.rstrip()) for l in lines) / max(1, n_lines)

    # signals
    comment_lines = len([l for l in lines if l.strip().startswith(("#", "//", "/*", "*"))])
    functions = len(re.findall(r"\\b(def |func |function |void |class )", code))
    loops = len(re.findall(r"\\b(for |while )", code))
    dangerous = re.findall(r"(eval|exec|system\(|popen|md5|sha1|password)", code)
    tests = re.search(r"(unittest|pytest|JUnit|XCTest|@Test|describe\(|it\()", code)

    # simple scoring
    readability = max(0, 20 - int(avg_len/5) - abs(comment_lines - n_lines*0.1)//2)
    maintainability = max(0, 20 - loops*2 + functions)
    robustness = 15 if ("try" in code or "catch" in code or "except" in code) else 8
    performance = max(0, 15 - int(n_lines/200))
    security = max(0, 10 - len(dangerous)*2)
    testability = 10 if tests else 4
    consistency = 10 if code.endswith("\n") else 7

    total_score = readability + maintainability + robustness + performance + security + testability + consistency
    shit_index = max(0, 100 - total_score)  # 越高越烂

    suggestions = []
    if avg_len > 100:
        suggestions.append("行太长，考虑拆分")
    if comment_lines < n_lines*0.05:
        suggestions.append("缺少注释，别人看不懂")
    if dangerous:
        suggestions.append(f"危险调用: {dangerous}")
    if not tests:
        suggestions.append("缺少测试")

    return {
        "language": language,
        "total": total_score,
        "shit_index": shit_index,
        "breakdown": {
            "readability": readability,
            "maintainability": maintainability,
            "robustness": robustness,
            "performance": performance,
            "security": security,
            "testability": testability,
            "consistency": consistency,
        },
        "suggestions": suggestions,
        "signals": {
            "lines": n_lines,
            "avg_line_len": avg_len,
            "comment_lines": comment_lines,
            "functions": functions,
            "loops": loops,
            "dangerous_calls": len(dangerous),
        }
    }

# ------------------ 输出风格 ------------------
def format_report(result: dict, lang: str = "zh-CN", markdown: bool = False, summary: bool = False) -> str:
    if lang == "en-US":
        shit_label = "💩 Shit Index"
        score_label = "✨ Score"
        sug_label = "🛠 Suggestions"
        header = f"## Code Quality Report ({result['language']})"
    else:
        shit_label = "💩 屎山指数"
        score_label = "✨ 综合得分"
        sug_label = "🛠 改进建议"
        header = f"## 代码质量报告 ({result['language']})"

    if summary:
        return f"{header}\n- {shit_label}: {result['shit_index']}\n- {score_label}: {result['total']}"

    lines = [header, f"- {shit_label}: {result['shit_index']}", f"- {score_label}: {result['total']}\n"]
    lines.append("### Breakdown")
    for k, v in result["breakdown"].items():
        lines.append(f"- {k}: {v}")
    if result["suggestions"]:
        lines.append(f"\n{ sug_label }:")
        for s in result["suggestions"]:
            lines.append(f"- {s}")
    else:
        lines.append(f"\n{ sug_label }: 没啥要挑剔的，继续保持！")

    return "\n".join(lines) if markdown else "\n".join(lines)

# ------------------ CLI ------------------
def main():
    parser = argparse.ArgumentParser(description="屎山代码检测器")
    parser.add_argument("path", help="代码文件或目录")
    parser.add_argument("--lang", default="auto", help="代码语言，默认 auto")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    parser.add_argument("--markdown", action="store_true", help="输出 Markdown")
    parser.add_argument("--summary", action="store_true", help="只输出概要")
    parser.add_argument("--verbose", action="store_true", help="详细模式")
    args = parser.parse_args()

    files = []
    if os.path.isdir(args.path):
        for root, _, fnames in os.walk(args.path):
            for f in fnames:
                files.append(os.path.join(root, f))
    else:
        files = [args.path]

    results = []
    for f in files:
        try:
            code = open(f, "r", encoding="utf-8", errors="ignore").read()
            results.append(score_code(code, args.lang, filename=f))
        except Exception as e:
            print(f"跳过 {f}: {e}", file=sys.stderr)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(format_report(r, markdown=args.markdown, summary=args.summary))
            print("\n" + "-"*40 + "\n")


if __name__ == "__main__":
    main()
