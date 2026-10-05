#!/usr/bin/env python3
"""
DOCX 스킬 보조: 복잡한 표 생성 유틸리티

사용 예:
python table_builder.py --output 보고서.docx --rows 5 --cols 4 --title "판매 현황"
"""

import argparse
import sys
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Inches
    from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
    from docx.oxml.ns import qn
except ImportError:
    print("ERROR: python-docx not found. Install with: pip install python-docx")
    sys.exit(1)


def set_korean_font(run, font_name="맑은 고딕", size=11, bold=False):
    """한글 글꼴 설정 (eastAsia 속성 필수)"""
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    # eastAsia 속성 설정
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        from docx.oxml import parse_xml
        rFonts = parse_xml(r'<w:rFonts {} w:eastAsia="{}"/>'.format(
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"',
            font_name
        ))
        rPr.append(rFonts)
    else:
        rFonts.set(qn('w:eastAsia'), font_name)


def create_table_doc(output_file, title, rows=3, cols=3, header_data=None):
    """
    표가 있는 Word 문서 생성

    Args:
        output_file: 저장할 파일 경로
        title: 문서 제목
        rows: 표 행 수 (헤더 포함)
        cols: 표 열 수
        header_data: 헤더 데이터 (리스트)
    """
    doc = Document()

    # 제목
    title_para = doc.add_paragraph(title)
    title_para.style = 'Heading 1'
    title_run = title_para.runs[0]
    set_korean_font(title_run, size=16, bold=True)

    # 표 생성
    table = doc.add_table(rows=rows, cols=cols)
    table.style = 'Light Grid Accent 1'

    # 헤더 행 설정
    header_cells = table.rows[0].cells

    if header_data:
        for i, header_text in enumerate(header_data[:cols]):
            header_cells[i].text = header_text
    else:
        for i in range(cols):
            header_cells[i].text = f"열{i+1}"

    # 헤더 셀 서식
    for cell in header_cells:
        # 배경색
        cell_xml = cell._element
        cell_pr = cell_xml.get_or_add_tcPr()
        shade = qn('w:shd')
        shade_element = cell_pr.find(shade)
        if shade_element is None:
            from docx.oxml import parse_xml
            shade_element = parse_xml(r'<w:shd {} w:fill="4472C4"/>'.format('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'))
            cell_pr.append(shade_element)

    # 헤더 텍스트 서식
    for cell in header_cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                set_korean_font(run, size=11, bold=True)

    # 데이터 행 추가 (더미 데이터)
    for row_idx in range(1, rows):
        for col_idx in range(cols):
            table.rows[row_idx].cells[col_idx].text = f"데이터{row_idx}-{col_idx}"

    # 열 너비 조정
    for col_idx in range(cols):
        width = Inches(1.5)
        for row in table.rows:
            row.cells[col_idx].width = width

    # 저장
    doc.save(output_file)
    print(f"✓ 생성 완료: {output_file} ({rows}행 x {cols}열)")
    return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Word 표 생성 유틸리티")
    parser.add_argument("--output", "-o", required=True, help="출력 파일 (.docx)")
    parser.add_argument("--title", "-t", default="표", help="문서 제목")
    parser.add_argument("--rows", "-r", type=int, default=3, help="표 행 수")
    parser.add_argument("--cols", "-c", type=int, default=3, help="표 열 수")
    parser.add_argument("--headers", "-H", nargs="+", help="헤더 텍스트")

    args = parser.parse_args()

    try:
        create_table_doc(
            args.output,
            args.title,
            rows=args.rows,
            cols=args.cols,
            header_data=args.headers
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
