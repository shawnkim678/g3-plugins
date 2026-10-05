"""HWPX 보고서 만들기 / 서식 채우기 (python-hwpx 6.x, Apache-2.0)

새 문서:  python hwpx_report.py --output 보고.hwpx --title 제목 --para 문단 [--para ...] [--table a,b --table c,d] [--header 머리말]
서식 채우기: python hwpx_report.py --fill 서식.hwpx --output 채운.hwpx --set "{{키}}=값" [--set ...]
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from hwpx.document import HwpxDocument


def make(a: argparse.Namespace) -> HwpxDocument:
    doc = HwpxDocument.new()
    if a.title:
        doc.add_heading(a.title, level=1)
    for p in a.para or []:
        doc.add_paragraph(p)
    rows = [r.split(",") for r in (a.table or [])]
    if rows:
        cols = max(len(r) for r in rows)
        t = doc.add_table(len(rows), cols)
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                t.set_cell_text(r, c, v.strip())
    if a.header:
        doc.page.set_header(text=a.header)
    return doc


def fill(a: argparse.Namespace) -> HwpxDocument:
    src, out = Path(a.fill), Path(a.output)
    if src.resolve() != out.resolve():
        shutil.copyfile(src, out)            # 원본 서식은 그대로 둔다
    doc = HwpxDocument.open(out)
    for kv in a.set or []:
        key, _, val = kv.partition("=")
        n = doc.text.replace(key, val)
        print(f"{key} → {val}: {n}곳" + ("  (없음 — 자리표시를 확인하세요)" if n == 0 else ""))
    return doc


def main() -> int:
    ap = argparse.ArgumentParser(description="HWPX 보고서 만들기 / 서식 채우기")
    ap.add_argument("--output", required=True)
    ap.add_argument("--title")
    ap.add_argument("--para", action="append")
    ap.add_argument("--table", action="append", help="한 행을 쉼표로, 여러 번 주면 여러 행(첫 행이 머리행)")
    ap.add_argument("--header")
    ap.add_argument("--fill", help="채울 서식 .hwpx")
    ap.add_argument("--set", action="append", help='"{{키}}=값"')
    a = ap.parse_args()
    doc = fill(a) if a.fill else make(a)
    doc.save_to_path(a.output)
    check = HwpxDocument.open(a.output)
    print(f"저장: {a.output}")
    print("검증:", "정상" if not check.validate().issues else check.validate().issues)
    print("본문 앞부분:\n" + check.text.plain()[:300])
    return 0


if __name__ == "__main__":
    sys.exit(main())
