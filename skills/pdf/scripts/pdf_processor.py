#!/usr/bin/env python3
"""
PDF 스킬 보조: PDF 분할, 병합, 추출 유틸리티

사용 예:
python pdf_processor.py --mode extract --input 문서.pdf --output 추출.txt
python pdf_processor.py --mode split --input 문서.pdf --pages 1 3 5 --output 분할.pdf
python pdf_processor.py --mode merge --input 문서1.pdf 문서2.pdf --output 병합.pdf
"""

import argparse
import sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    print("ERROR: pypdf not found. Install with: pip install pypdf")
    sys.exit(1)

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def extract_text(input_file, output_file=None):
    """PDF에서 텍스트 추출"""
    try:
        if pdfplumber:
            # pdfplumber 사용 (더 안정적)
            with pdfplumber.open(input_file) as pdf:
                all_text = []
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    all_text.append(f"=== 페이지 {page_num + 1} ===\n{text}\n")

                full_text = "\n".join(all_text)
        else:
            # pypdf 사용
            reader = PdfReader(input_file)
            all_text = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                all_text.append(f"=== 페이지 {page_num + 1} ===\n{text}\n")

            full_text = "\n".join(all_text)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"✓ 추출 완료: {output_file}")
        else:
            print(full_text)

        return full_text

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None


def split_pdf(input_file, page_numbers, output_file):
    """특정 페이지만 추출"""
    try:
        reader = PdfReader(input_file)
        writer = PdfWriter()

        # 페이지 번호를 0-indexed로 변환
        for page_num in page_numbers:
            if 1 <= page_num <= len(reader.pages):
                writer.add_page(reader.pages[page_num - 1])
            else:
                print(f"Warning: 페이지 {page_num}은 존재하지 않습니다 (총 {len(reader.pages)}페이지)")

        with open(output_file, 'wb') as f:
            writer.write(f)

        print(f"✓ 분할 완료: {output_file} ({len(writer.pages)}페이지)")
        return True

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return False


def merge_pdfs(input_files, output_file):
    """여러 PDF 병합"""
    try:
        writer = PdfWriter()

        for pdf_file in input_files:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                writer.add_page(page)

        with open(output_file, 'wb') as f:
            writer.write(f)

        print(f"✓ 병합 완료: {output_file} ({len(writer.pages)}페이지)")
        return True

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return False


def get_info(input_file):
    """PDF 메타데이터 조회"""
    try:
        reader = PdfReader(input_file)

        print(f"파일: {input_file}")
        print(f"페이지 수: {len(reader.pages)}")

        if reader.metadata:
            print("메타데이터:")
            for key, value in reader.metadata.items():
                print(f"  {key}: {value}")

        return True

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF 처리 유틸리티")
    parser.add_argument("--mode", "-m", required=True,
                       choices=["extract", "split", "merge", "info"],
                       help="처리 모드")
    parser.add_argument("--input", "-i", nargs="+", help="입력 PDF 파일")
    parser.add_argument("--output", "-o", help="출력 파일")
    parser.add_argument("--pages", "-p", type=int, nargs="+",
                       help="추출할 페이지 번호 (1-indexed, split 모드에서만)")

    args = parser.parse_args()

    if args.mode == "extract":
        if not args.input:
            print("ERROR: --input 필수 (extract 모드)", file=sys.stderr)
            sys.exit(1)
        extract_text(args.input[0], args.output)

    elif args.mode == "split":
        if not args.input or not args.pages:
            print("ERROR: --input과 --pages 필수 (split 모드)", file=sys.stderr)
            sys.exit(1)
        if not args.output:
            print("ERROR: --output 필수 (split 모드)", file=sys.stderr)
            sys.exit(1)
        split_pdf(args.input[0], args.pages, args.output)

    elif args.mode == "merge":
        if not args.input or len(args.input) < 2:
            print("ERROR: 최소 2개 이상의 --input 필수 (merge 모드)", file=sys.stderr)
            sys.exit(1)
        if not args.output:
            print("ERROR: --output 필수 (merge 모드)", file=sys.stderr)
            sys.exit(1)
        merge_pdfs(args.input, args.output)

    elif args.mode == "info":
        if not args.input:
            print("ERROR: --input 필수 (info 모드)", file=sys.stderr)
            sys.exit(1)
        get_info(args.input[0])
