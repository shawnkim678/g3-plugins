#!/usr/bin/env python3
"""
XLSX 스킬 보조: 수식이 있는 스프레드시트 생성 유틸리티

사용 예:
python formula_builder.py --output 판매.xlsx --type sales
python formula_builder.py --output 재무.xlsx --type budget
"""

import argparse
import sys
from datetime import datetime

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("ERROR: openpyxl not found. Install with: pip install openpyxl")
    sys.exit(1)


def create_sales_sheet(wb, sheet_name="판매현황"):
    """판매 데이터 시트 생성 (수식 포함)"""
    ws = wb.active
    ws.title = sheet_name

    # 헤더
    headers = ["분기", "판매액", "성장률", "누적액", "평균액"]
    ws.append(headers)

    # 데이터
    data = [
        ["Q1", 1000000, 0.10],
        ["Q2", 1500000, 0.50],
        ["Q3", 2000000, 0.33],
        ["Q4", 2500000, 0.25],
    ]

    for row_data in data:
        ws.append(row_data)

    # 수식 추가
    # D2: Q1 누적액 = B2
    ws['D2'] = "=B2"
    # D3: Q2 누적액 = D2 + B3
    ws['D3'] = "=D2+B3"
    # D4: Q3 누적액 = D3 + B4
    ws['D4'] = "=D3+B4"
    # D5: Q4 누적액 = D4 + B5
    ws['D5'] = "=D4+B5"

    # E2: 평균액 = AVERAGE($B$2:B2)
    for row in range(2, 6):
        ws[f'E{row}'] = f"=AVERAGE($B$2:B{row})"

    # 서식 적용
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)

    for col_num in range(1, 6):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # 숫자 포맷
    for row in range(2, 6):
        for col in [2, 4, 5]:  # 판매액, 누적액, 평균액
            cell = ws.cell(row=row, column=col)
            cell.number_format = '#,##0'

    # 백분율 포맷
    for row in range(2, 6):
        ws.cell(row=row, column=3).number_format = '0.0%'

    # 열 너비
    ws.column_dimensions['A'].width = 10
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 12
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 12

    return ws


def create_budget_sheet(wb, sheet_name="예산"):
    """예산 관리 시트 생성"""
    ws = wb.create_sheet(sheet_name)

    # 헤더
    headers = ["항목", "예산", "실제", "편차", "편차율"]
    ws.append(headers)

    # 데이터
    budget_items = [
        ["인건비", 5000000, 4800000],
        ["운영비", 2000000, 2100000],
        ["마케팅", 1500000, 1450000],
        ["기술개발", 3000000, 3200000],
    ]

    for item_data in budget_items:
        ws.append(item_data)

    # 수식: 편차 = 실제 - 예산
    for row in range(2, 6):
        ws[f'D{row}'] = f"=C{row}-B{row}"

    # 수식: 편차율 = 편차 / 예산
    for row in range(2, 6):
        ws[f'E{row}'] = f"=D{row}/B{row}"

    # 합계 행
    ws.append(["합계", "=SUM(B2:B5)", "=SUM(C2:C5)", "=SUM(D2:D5)", "=E6/B6"])

    # 서식
    header_fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=11)

    for col_num in range(1, 6):
        cell = ws.cell(row=1, column=col_num)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    # 합계 행 서식
    for col_num in range(1, 6):
        cell = ws.cell(row=6, column=col_num)
        cell.font = Font(bold=True)
        cell.fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")

    # 숫자 포맷
    for row in range(2, 7):
        for col in [2, 3, 4]:  # 예산, 실제, 편차
            ws.cell(row=row, column=col).number_format = '#,##0'
        ws.cell(row=row, column=5).number_format = '0.0%'  # 편차율

    # 열 너비
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 15
    ws.column_dimensions['D'].width = 12
    ws.column_dimensions['E'].width = 12

    return ws


def create_workbook(output_file, sheet_type="sales"):
    """워크북 생성"""
    wb = Workbook()

    if sheet_type == "sales":
        create_sales_sheet(wb)
        sheet_name = "판매현황"
    elif sheet_type == "budget":
        create_budget_sheet(wb)
        sheet_name = "예산"
    else:
        print(f"Unknown sheet type: {sheet_type}", file=sys.stderr)
        return None

    # 저장
    wb.save(output_file)
    print(f"✓ 생성 완료: {output_file} ({sheet_name})")
    print(f"  주의: 파일을 엑셀에서 열어야 수식이 계산됩니다")
    return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Excel 수식 스프레드시트 생성 유틸리티")
    parser.add_argument("--output", "-o", required=True, help="출력 파일 (.xlsx)")
    parser.add_argument("--type", "-t", default="sales", choices=["sales", "budget"], help="시트 종류")

    args = parser.parse_args()

    try:
        create_workbook(args.output, args.type)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
