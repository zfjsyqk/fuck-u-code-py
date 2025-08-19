#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import argparse
import re
import json
import sys
import fnmatch
import hashlib
from collections import Counter

ANSI = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "gray": "\033[90m",
}

SUPPORTED_EXTS = {
    "go": [".go"],
    "javascript": [".js", ".mjs", ".cjs"],
    "typescript": [".ts", ".tsx"],
    "python": [".py"],
    "java": [".java"],
    "c": [".c", ".h"],
    "cpp": [".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx"],
    "rust": [".rs"],
    "swift": [".swift"],
    "objective-c": [".m", ".mm", ".h"],
    "dart": [".dart"],
}

DEFAULT_EXCLUDES = [
    "**/node_modules/**", "**/bower_components/**",
    "**/dist/**", "**/build/**", "**/.next/**", "**/out/**",
    "**/.cache/**", "**/.nuxt/**", "**/.output/**",
    "**/vendor/**", "**/bin/**", "**/target/**", "**/obj/**",
    "**/tmp/**", "**/temp/**", "**/logs/**",
    "**/generated/**", "**/migrations/**",
    "**/testdata/**", "**/test-results/**",
    "**/.git/**", "**/.svn/**", "**/.hg/**",
]
MIN_BLOCK_LINES = 3

def guess_language_by_ext(path: Path):
    ext = path.suffix.lower()
    for lang, exts in SUPPORTED_EXTS.items():
        if ext in exts:
            return lang
    return None

def is_binary(data: bytes) -> bool:
    if not data:
        return False
    return b"\x00" in data

def read_text(path: Path):
    try:
        data = path.read_bytes()
        if is_binary(data):
            return None
        return data.decode("utf-8", errors="ignore")
    except Exception:
        return None

COMMENT_SYNTAX = {
    "python": {"line": r"#", "block_start": None, "block_end": None},
    "go": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "javascript": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "typescript": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "java": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "c": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "cpp": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "rust": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "swift": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "objective-c": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
    "dart": {"line": r"//", "block_start": r"/\*", "block_end": r"\*/"},
}

COMPLEXITY_TOKENS = [
    r"\bif\b", r"\belse if\b", r"\bfor\b", r"\bwhile\b", r"\bcase\b", r"\bwhen\b",
    r"\bcatch\b", r"\?\s*:", r"&&", r"\|\|", r"\bguard\b", r"\belif\b",
]

ERROR_HANDLING_TOKENS = [
    r"\btry\b", r"\bcatch\b", r"\bexcept\b", r"\bthrows\b", r"\bthrow\b",
]

FUNCTION_PATTERNS = {
    "python": re.compile(r"^\s*def\s+\w+\s*\(", re.M),
    "go": re.compile(r"^\s*func\s+\w+\s*\(", re.M),
    "javascript": re.compile(r"^\s*(function\s+\w+\s*\(|\w+\s*=\s*\(.*\)\s*=>)", re.M),
    "typescript": re.compile(r"^\s*(function\s+\w+\s*\(|\w+\s*=\s*\(.*\)\s*=>)", re.M),
    "java": re.compile(r"^\s*(public|private|protected)?\s*(static\s+)?[\w<>\[\]]+\s+\w+\s*\(.*\)\s*\{", re.M),
    "c": re.compile(r"^\s*[\w\*\s]+\s+\w+\s*\([^;]*\)\s*\{", re.M),
    "cpp": re.compile(r"^\s*[\w\*\s:<>]+\s+\w+::?\w*\s*\([^;]*\)\s*\{", re.M),
    "rust": re.compile(r"^\s*fn\s+\w+\s*\(", re.M),
    "swift": re.compile(r"^\s*func\s+\w+\s*\(", re.M),
    "objective-c": re.compile(r"^\s*[-+]\s*\([^)]+\)\s*\w+", re.M),
    "dart": re.compile(r"^\s*[\w<>\[\]]+\s+\w+\s*\([^;]*\)\s*\{", re.M),
}

I18N = {
    "zh-CN": {
        "title": "屎山代码检测报告",
        "overall": "总体评分（分越高越像屎山）",
        "files": "分析文件数",
        "worst_files": "问题最多的文件（前{n}个）",
        "metrics": "质量指标",
        "readability": "可读性",
        "complexity": "循环复杂度",
        "comments": "注释覆盖率",
        "structure": "结构与嵌套",
        "duplication": "重复度",
        "naming": "命名规范",
        "error_handling": "错误处理",
        "issues": "问题列表（最多 {n} 条）",
        "no_issues": "未发现显著问题。继续保持！",
        "summary": "摘要",
        "suggestions": "改进建议",
        "file": "文件",
        "score": "得分",
        "lang": "语言",
        "grade": "等级",
        "A": "A 优秀",
        "B": "B 良好",
        "C": "C 一般",
        "D": "D 较差",
        "E": "E 糟糕",
    },
    "en-US": {
        "title": "Spaghetti Code Inspection Report",
        "overall": "Overall Score (higher = worse)",
        "files": "Files analyzed",
        "worst_files": "Worst files (top {n})",
        "metrics": "Quality Metrics",
        "readability": "Readability",
        "complexity": "Cyclomatic complexity",
        "comments": "Comment coverage",
        "structure": "Structure & nesting",
        "duplication": "Duplication",
        "naming": "Naming conventions",
        "error_handling": "Error handling",
        "issues": "Issues (up to {n})",
        "no_issues": "No significant issues found. Keep it up!",
        "summary": "Summary",
        "suggestions": "Suggestions",
        "file": "File",
        "score": "Score",
        "lang": "Language",
        "grade": "Grade",
        "A": "A Excellent",
        "B": "B Good",
        "C": "C Fair",
        "D": "D Poor",
        "E": "E Terrible",
    },
}

def grade(score):
    if score < 20: return "A"
    if score < 40: return "B"
    if score < 60: return "C"
    if score < 80: return "D"
    return "E"

def count_comment_coverage(text, lang):
    syntax = COMMENT_SYNTAX.get(lang) or {"line": r"//", "block_start": None, "block_end": None}
    lines = text.splitlines()
    total = 0
    comment = 0
    in_block = False
    bs, be = syntax.get("block_start"), syntax.get("block_end")
    line_pat = syntax.get("line")
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        total += 1
        if bs and be and re.search(bs, stripped):
            in_block = True
            comment += 1
            continue
        if in_block:
            comment += 1
            if be and re.search(be, stripped):
                in_block = False
            continue
        if line_pat and re.match(rf"\s*{line_pat}", line):
            comment += 1
    return comment / total if total else 0.0

def count_complexity(text):
    s = 0
    for tok in COMPLEXITY_TOKENS:
        s += len(re.findall(tok, text))
    return s

def measure_nesting(text):
    depth = 0
    max_depth = 0
    for ch in text:
        if ch == '{':
            depth += 1
            if depth > max_depth:
                max_depth = depth
        elif ch == '}':
            depth = max(depth - 1, 0)
    for line in text.splitlines():
        indent = len(line) - len(line.lstrip())
        max_depth = max(max_depth, indent // 4)
    return max_depth

def detect_functions(text, lang):
    pat = FUNCTION_PATTERNS.get(lang)
    if not pat:
        return []
    positions = [m.start() for m in pat.finditer(text)]
    if not positions:
        return []
    positions.append(len(text))
    slices = []
    for i in range(len(positions)-1):
        chunk = text[positions[i]:positions[i+1]]
        line_count = chunk.count("\\n") + 1
        slices.append(line_count)
    return slices

def naming_smells(text):
    idents = re.findall(r"\\b([A-Za-z_][A-Za-z0-9_]{0,})\\b", text)
    short = sum(1 for x in idents if len(x) == 1)
    long_ = sum(1 for x in idents if len(x) >= 30)
    screaming = sum(1 for x in idents if x.isupper() and len(x) >= 8)
    return {"short": short, "long": long_, "screaming": screaming}

def error_handling_presence(text):
    c = 0
    for tok in ERROR_HANDLING_TOKENS:
        c += len(re.findall(tok, text))
    return c

def duplication_ratio(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if len(lines) < MIN_BLOCK_LINES * 2:
        return 0.0
    hashes = []
    for i in range(len(lines) - MIN_BLOCK_LINES + 1):
        block = "\\n".join(lines[i:i+MIN_BLOCK_LINES])
        h = hashlib.md5(block.encode("utf-8")).hexdigest()
        hashes.append(h)
    cnt = Counter(hashes)
    dup_blocks = sum(v for v in cnt.values() if v > 1)
    total_blocks = max(len(hashes), 1)
    return dup_blocks / total_blocks

def normalize(value, lo, hi):
    if hi <= lo:
        return 0.0
    v = (value - lo) / (hi - lo)
    return max(0.0, min(1.0, v))

def compute_file_score(text, lang):
    comment_cov = count_comment_coverage(text, lang)
    complexity = count_complexity(text)
    nest = measure_nesting(text)
    funcs = detect_functions(text, lang)
    avg_func_len = sum(funcs) / len(funcs) if funcs else 0
    names = naming_smells(text)
    errors = error_handling_presence(text)
    dup = duplication_ratio(text)

    n_complexity = normalize(complexity, 0, 50)
    n_nest = normalize(nest, 0, 8)
    n_avg_len = normalize(avg_func_len, 0, 120)
    n_names = normalize(names["short"] + names["long"] + names["screaming"], 0, 200)
    n_dup = dup
    n_comments = 1.0 - max(min(comment_cov, 1.0), 0.0)
    n_errors = 1.0 - normalize(errors, 0, 10)

    weights = {
        "complexity": 0.22,
        "structure": 0.18,
        "function_length": 0.15,
        "naming": 0.12,
        "duplication": 0.13,
        "comments": 0.12,
        "error_handling": 0.08,
    }
    composite = (
        n_complexity * weights["complexity"]
        + n_nest * weights["structure"]
        + n_avg_len * weights["function_length"]
        + n_names * weights["naming"]
        + n_dup * weights["duplication"]
        + n_comments * weights["comments"]
        + n_errors * weights["error_handling"]
    )
    score = int(round(composite * 100))
    metrics = {
        "comment_coverage": round(comment_cov, 3),
        "complexity_tokens": complexity,
        "max_nesting": nest,
        "avg_function_lines": round(avg_func_len, 2),
        "naming_smells": names,
        "error_handling_tokens": errors,
        "duplication_ratio": round(dup, 3),
    }
    return score, metrics

def enumerate_files(root: Path, excludes, skipindex):
    files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        skip = False
        for pat in DEFAULT_EXCLUDES + list(excludes):
            if fnmatch.fnmatch(str(rel), pat):
                skip = True
                break
        if skip:
            continue
        lang = guess_language_by_ext(p)
        if not lang:
            continue
        if skipindex and p.name in ("index.js", "index.ts"):
            continue
        files.append((p, lang))
    return files

def extract_issues(text, lang):
    issues = []
    lines = text.splitlines()
    if len(lines) > 800:
        issues.append(f"文件过长：{len(lines)} 行，建议拆分模块。")
    long_lines = [i+1 for i, ln in enumerate(lines) if len(ln) > 160]
    if long_lines:
        issues.append(f"存在超长行（>160列），示例行号：{long_lines[:5]}")
    nest = measure_nesting(text)
    if nest >= 6:
        issues.append(f"嵌套过深：最大嵌套深度 {nest}，建议函数拆分。")
    cov = count_comment_coverage(text, lang)
    if cov < 0.05:
        issues.append(f"注释极少：覆盖率 {cov:.1%}，建议补充关键函数与模块说明。")
    dup = duplication_ratio(text)
    if dup > 0.2:
        issues.append(f"重复代码较多：重复块比例 {dup:.1%}，建议抽取公用函数。")
    cx = count_complexity(text)
    if cx > 80:
        issues.append(f"分支复杂度高：关键字计数 {cx}，建议减少条件与分支。")
    return issues

I18N = I18N  # keep dictionary in scope

def format_terminal_report(results, lang_key, top_n, issues_n, summary_only):
    L = I18N[lang_key]
    total_files = len(results)
    overall = int(round(sum(r["score"] for r in results) / max(total_files, 1)))
    grd = grade(overall)
    worst = sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]

    lines = []
    header = f"{ANSI['bold']}{ANSI['magenta']}{L['title']}{ANSI['reset']}"
    lines.append(header)
    lines.append(f"{L['overall']}: {ANSI['red']}{overall}{ANSI['reset']}  {L['grade']}: {L[grd]}  {L['files']}: {total_files}")
    if summary_only:
        return "\\n".join(lines)

    lines.append("")
    lines.append(f"{ANSI['bold']}{L['worst_files'].format(n=top_n)}{ANSI['reset']}")
    for item in worst:
        lines.append(f"  - {item['path']}  {L['score']}: {ANSI['yellow']}{item['score']}{ANSI['reset']}  {L['lang']}: {item['language']}")

    lines.append("")
    lines.append(f"{ANSI['bold']}{L['metrics']}{ANSI['reset']}")
    lines.append(f"  {L['complexity']}, {L['structure']}, {L['comments']}, {L['duplication']}, {L['naming']}, {L['error_handling']}")

    lines.append("")
    lines.append(f"{ANSI['bold']}{L['issues'].format(n=issues_n)}{ANSI['reset']}")
    any_issue = False
    for item in worst:
        if not item['issues']:
            continue
        any_issue = True
        lines.append(f"  {ANSI['blue']}{item['path']}{ANSI['reset']}")
        for s in item['issues'][:issues_n]:
            lines.append(f"    - {s}")
    if not any_issue:
        lines.append(f"  {L['no_issues']}")

    return "\\n".join(lines)

def format_markdown(results, lang_key, top_n, summary_only):
    L = I18N[lang_key]
    total_files = len(results)
    overall = int(round(sum(r['score'] for r in results) / max(total_files, 1)))
    grd = grade(overall)
    worst = sorted(results, key=lambda x: x['score'], reverse=True)[:top_n]

    md = []
    md.append(f"# {L['title']}")
    md.append("")
    md.append(f"- **{L['overall']}**: `{overall}`  - **{L['grade']}**: `{L[grd]}`  - **{L['files']}**: `{total_files}`")
    md.append("")
    if summary_only:
        return "\\n".join(md)

    md.append(f"## {L['worst_files'].format(n=top_n)}")
    for item in worst:
        md.append(f"- `{item['path']}` — **{L['score']}**: `{item['score']}`  **{L['lang']}**: `{item['language']}`")

    md.append("")
    md.append(f"## {L['metrics']}（per file）")
    md.append("")
    md.append("| File | Score | Comment% | Complexity | Max Nest | Avg Func Lines | Dup Ratio | Error Tokens |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for item in worst:
        m = item['metrics']
        md.append(f"| `{item['path']}` | {item['score']} | {m['comment_coverage']:.0%} | {m['complexity_tokens']} | {m['max_nesting']} | {m['avg_function_lines']} | {m['duplication_ratio']:.0%} | {m['error_handling_tokens']} |")

    md.append("")
    md.append(f"## {I18N[lang_key]['issues'].format(n=5)}")
    for item in worst:
        md.append(f"### `{item['path']}`")
        if not item['issues']:
            md.append(f"- {L['no_issues']}")
        else:
            for s in item['issues'][:5]:
                md.append(f"- {s}")
        md.append("")
    return "\\n".join(md)

def enumerate_files(root: Path, excludes, skipindex):
    files = []
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        rel = p.relative_to(root)
        skip = False
        for pat in DEFAULT_EXCLUDES + list(excludes):
            if fnmatch.fnmatch(str(rel), pat):
                skip = True
                break
        if skip:
            continue
        lang = guess_language_by_ext(p)
        if not lang:
            continue
        if skipindex and p.name in ('index.js', 'index.ts'):
            continue
        files.append((p, lang))
    return files

def main(argv=None):
    parser = argparse.ArgumentParser(description="屎山代码检测器（Python版） — 评估代码的屎山等级")
    parser.add_argument("target", nargs="?", default=".", help="要分析的项目路径（默认：当前目录）")
    parser.add_argument("command", nargs="?", choices=["analyze"], help="命令（目前仅支持 analyze）")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细分析报告")
    parser.add_argument("--top", "-t", type=int, default=5, help="显示问题最多的前 N 个文件")
    parser.add_argument("--issues", "-i", type=int, default=5, help="每个文件显示 N 个问题")
    parser.add_argument("--summary", "-s", action="store_true", help="只显示总结信息")
    parser.add_argument("--markdown", "-m", action="store_true", help="输出 Markdown 格式报告")
    parser.add_argument("--lang", "-l", default="zh-CN", choices=["zh-CN", "en-US"], help="输出语言")
    parser.add_argument("--exclude", "-e", action="append", default=[], help="排除模式（可多次使用）")
    parser.add_argument("--skipindex", "-x", action="store_true", help="跳过 index.js / index.ts 文件")
    parser.add_argument("--json", action="store_true", help="输出 JSON 结果（便于机器处理）")
    args = parser.parse_args(argv)

    target = Path(args.target)
    root = target if target.exists() else Path(".")
    files = enumerate_files(root, args.exclude, args.skipindex)

    results = []
    for p, lang in files:
        text = read_text(p)
        if text is None:
            continue
        score, metrics = compute_file_score(text, lang)
        issues = extract_issues(text, lang)
        results.append({
            "path": str(p.relative_to(root)),
            "language": lang,
            "score": score,
            "metrics": metrics,
            "issues": issues,
        })
    results.sort(key=lambda x: x["score"], reverse=True)

    if args.json:
        out = {
            "overall": int(round(sum(r["score"] for r in results) / max(len(results), 1))),
            "grade": grade(int(round(sum(r["score"] for r in results) / max(len(results), 1)))),
            "files": len(results),
            "results": results[:args.top],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if args.markdown:
        md = format_markdown(results, args.lang, args.top, args.summary)
        print(md)
        return

    report = format_terminal_report(results, args.lang, args.top, args.issues, args.summary or not args.verbose)
    print(report)

if __name__ == "__main__":
    main()
