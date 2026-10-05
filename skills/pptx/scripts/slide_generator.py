#!/usr/bin/env python3
"""
PPTX 스킬 보조: 간단한 슬라이드 생성 유틸리티

사용 예:
python slide_generator.py --output 발표.pptx --title "프로젝트" --bullets "목표" "성과" "계획"
"""

import argparse
import sys

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.enum.text import PP_ALIGN
    from pptx.dml.color import RGBColor
except ImportError:
    print("ERROR: python-pptx not found. Install with: pip install python-pptx")
    sys.exit(1)


def create_title_slide(prs, title_text, subtitle_text):
    """제목 슬라이드 추가"""
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)

    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = title_text
    subtitle.text = subtitle_text

    return slide


def create_bullet_slide(prs, title_text, bullets):
    """불릿 포인트 슬라이드 추가"""
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)

    title = slide.shapes.title
    title.text = title_text

    body = slide.placeholders[1]
    tf = body.text_frame
    tf.clear()

    for i, bullet_text in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        p.text = bullet_text
        p.level = 0
        p.font.size = Pt(18)

    return slide


def create_blank_slide(prs, title_text):
    """빈 슬라이드 (제목만)"""
    blank_slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_slide_layout)

    # 제목 텍스트 박스 추가
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.5), Inches(9), Inches(0.8)
    )
    text_frame = title_box.text_frame
    p = text_frame.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(32)
    p.font.bold = True

    return slide


def create_presentation(output_file, title, subtitle, bullet_slides):
    """
    프레젠테이션 생성

    Args:
        output_file: 저장할 파일 (.pptx)
        title: 제목
        subtitle: 부제목
        bullet_slides: [(제목, [불릿 리스트]), ...] 형식
    """
    prs = Presentation()

    # 제목 슬라이드
    create_title_slide(prs, title, subtitle)

    # 불릿 슬라이드들
    for slide_title, bullets in bullet_slides:
        create_bullet_slide(prs, slide_title, bullets)

    # 저장
    prs.save(output_file)
    print(f"✓ 생성 완료: {output_file} ({len(prs.slides)}개 슬라이드)")
    return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PowerPoint 슬라이드 생성 유틸리티")
    parser.add_argument("--output", "-o", required=True, help="출력 파일 (.pptx)")
    parser.add_argument("--title", "-t", required=True, help="프레젠테이션 제목")
    parser.add_argument("--subtitle", "-s", default="", help="부제목")
    parser.add_argument("--slide1-title", default="개요", help="첫 번째 슬라이드 제목")
    parser.add_argument("--slide1-bullets", nargs="+", default=["내용1", "내용2", "내용3"], help="첫 번째 슬라이드 불릿")
    parser.add_argument("--slide2-title", default="세부사항", help="두 번째 슬라이드 제목")
    parser.add_argument("--slide2-bullets", nargs="+", default=["항목1", "항목2", "항목3"], help="두 번째 슬라이드 불릿")

    args = parser.parse_args()

    try:
        bullet_slides = [
            (args.slide1_title, args.slide1_bullets),
            (args.slide2_title, args.slide2_bullets),
        ]

        create_presentation(
            args.output,
            args.title,
            args.subtitle,
            bullet_slides
        )
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
