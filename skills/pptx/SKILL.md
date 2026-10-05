---
name: pptx
description: |
  PowerPoint 프레젠테이션(.pptx) 생성·편집. 슬라이드쇼, 발표자료, 
  회의 자료. Create and edit PowerPoint presentations and slide decks.
---

# PPTX 스킬 가이드

## 언제 사용하나?

- **슬라이드 생성**: 마크다운 기반 발표 자료
- **프레젠테이션 만들기**: 슬라이드 구조, 텍스트, 이미지, 표
- **기존 슬라이드 편집**: 특정 슬라이드 수정
- **슬라이드쇼 자동화**: 배치 생성 또는 반복 작업

## 빠른 길 (내장 도구)

### 1. 마크다운에서 프레젠테이션 생성

마크다운의 `##` 제목마다 새 슬라이드 생성:

```
사용자: "발표자료.pptx를 만들어줘. 마크다운:
# 회사 소개
## 개요
우리는 ...

## 제품
- 제품 A
- 제품 B
"
```

→ **MakeDoc(file_path, markdown, format="pptx")**

결과: 슬라이드 2개 (각 `##`마다 1개)

검증:
```
→ ReadDoc("발표자료.pptx") 로 내용 확인
→ PreviewDoc("발표자료.pptx") 로 슬라이드 확인
```

### 2. 프레젠테이션 읽기

```
→ ReadDoc("발표자료.pptx")
출력: "슬라이드별 텍스트 내용"
```

### 3. 슬라이드 텍스트 수정 (기본 예제)

```
→ EditDoc("발표자료.pptx", "기존 텍스트", "새 텍스트")
출력: "수정 완료"
```

주의: EditDoc은 텍스트만 수정, 레이아웃/이미지는 별도 처리

## 세밀한 작업 (python-pptx 라이브러리)

내장 도구로 안 되는 작업:
- **다양한 레이아웃** (텍스트 + 이미지, 2열 레이아웃)
- **이미지/차트 삽입**
- **도형, 텍스트 박스, 테이블 추가**
- **색상, 배경, 테마 커스터마이징**
- **애니메이션 및 전환 효과**
- **슬라이드 순서 변경**

### 예제 1: 기본 슬라이드 만들기

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# 프레젠테이션 생성
prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# 슬라이드 1: 제목 슬라이드
title_slide_layout = prs.slide_layouts[0]  # Title Slide
slide1 = prs.slides.add_slide(title_slide_layout)
title = slide1.shapes.title
subtitle = slide1.placeholders[1]
title.text = "프로젝트 발표"
subtitle.text = "2026년 Q1 결과"

# 슬라이드 2: 텍스트 슬라이드
bullet_slide_layout = prs.slide_layouts[1]  # Bullet Points
slide2 = prs.slides.add_slide(bullet_slide_layout)
title = slide2.shapes.title
title.text = "주요 성과"

body = slide2.placeholders[1]
tf = body.text_frame
tf.text = "첫 번째 목표 달성"

p = tf.add_paragraph()
p.text = "두 번째 목표 달성"
p.level = 0

p = tf.add_paragraph()
p.text = "세부 항목"
p.level = 1

prs.save("발표.pptx")
```

검증:
```
1. ReadDoc("발표.pptx") → 슬라이드 텍스트 확인
2. PreviewDoc("발표.pptx") → 슬라이드 레이아웃 확인
```

### 예제 2: 테이블이 있는 슬라이드

```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
blank_slide_layout = prs.slide_layouts[6]  # Blank layout
slide = prs.slides.add_slide(blank_slide_layout)

# 제목 추가
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.5))
title_frame = title_box.text_frame
title_frame.text = "판매 현황"

# 테이블 추가: 2행 3열
rows, cols = 3, 3
left = Inches(1)
top = Inches(1.5)
width = Inches(8)
height = Inches(3)

table_shape = slide.shapes.add_table(rows, cols, left, top, width, height).table

# 헤더 행
table_shape.cell(0, 0).text = "분기"
table_shape.cell(0, 1).text = "판매액"
table_shape.cell(0, 2).text = "성장률"

# 데이터 행
table_shape.cell(1, 0).text = "Q1"
table_shape.cell(1, 1).text = "100만원"
table_shape.cell(1, 2).text = "10%"

table_shape.cell(2, 0).text = "Q2"
table_shape.cell(2, 1).text = "150만원"
table_shape.cell(2, 2).text = "50%"

prs.save("테이블발표.pptx")
```

검증:
```
1. ReadDoc("테이블발표.pptx") → 테이블 내용 확인
2. PreviewDoc("테이블발표.pptx") → 테이블 레이아웃 확인
```

### 예제 3: 도형 및 텍스트 박스

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

prs = Presentation()
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

# 배경색 설정
background = slide.background
fill = background.fill
fill.solid()
fill.fore_color.rgb = RGBColor(240, 248, 255)  # Alice blue

# 제목
title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.5), Inches(9), Inches(0.8))
tf = title_box.text_frame
tf.text = "핵심 포인트"
tf.paragraphs[0].font.size = Pt(36)
tf.paragraphs[0].font.bold = True

# 원형 도형 추가
circle = slide.shapes.add_shape(
    MSO_SHAPE.OVAL, Inches(2), Inches(2), Inches(2), Inches(2)
)
circle.fill.solid()
circle.fill.fore_color.rgb = RGBColor(255, 0, 0)  # Red
circle.line.color.rgb = RGBColor(0, 0, 0)

# 도형 내 텍스트
text_frame = circle.text_frame
text_frame.text = "중요!"
text_frame.paragraphs[0].font.size = Pt(24)
text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

# 직사각형 추가
rect = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(5), Inches(2), Inches(3), Inches(2)
)
rect.fill.solid()
rect.fill.fore_color.rgb = RGBColor(0, 0, 255)  # Blue

text_frame = rect.text_frame
text_frame.text = "추가 정보"
text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)

prs.save("도형발표.pptx")
```

검증:
```
1. PreviewDoc("도형발표.pptx") → 도형 및 색상 확인
```

## 검증 단계

1. **MakeDoc 사용** → 프레젠테이션 생성
   ```
   MakeDoc("발표.pptx", "마크다운 내용", format="pptx")
   ```

2. **ReadDoc 확인** → 슬라이드 텍스트 검증
   ```
   ReadDoc("발표.pptx")
   → 모든 슬라이드 텍스트 내용 확인
   ```

3. **PreviewDoc 확인** → 시각적 확인
   ```
   PreviewDoc("발표.pptx")
   → PNG로 렌더링되어 슬라이드 확인
   ```

4. **수정 필요 시 EditDoc**
   ```
   EditDoc("발표.pptx", "기존 텍스트", "새 텍스트")
   ```

## 흔한 함정

| 함정 | 해결책 |
|------|--------|
| 마크다운 `##` 미인식 | 반드시 `##`(2개 #) 사용, `#`(1개)는 제목용 |
| 슬라이드 레이아웃 부작용 | `prs.slide_layouts[6]` (Blank)로 시작, 수동 배치 |
| 텍스트 오버플로우 | 글꼴 크기 조정 또는 텍스트 박스 크기 확대 |
| 이미지 경로 오류 | 절대경로 사용 |
| 한글 폰트 미지정 | python-pptx는 자동으로 기본 폰트 사용 (별도 설정 불필요) |
| 파일 열려 있음 | 저장 전에 PowerPoint에서 닫혀 있는지 확인 |

## 추천 워크플로우

```
1. 간단한 발표 → MakeDoc(마크다운) + ReadDoc 검증
2. 기존 프레젠테이션 수정 → ReadDoc(내용 확인) → EditDoc(텍스트 수정)
3. 복잡한 레이아웃 필요 → python-pptx 스크립트 + MakeDoc 저장
4. 이미지, 표, 도형 필요 → python-pptx 라이브러리 사용
```


## 보조 스크립트 (이 SKILL.md 와 같은 폴더의 `scripts/`)

SKILL.md 경로의 폴더를 `<스킬폴더>` 라 할 때(설치 위치는 스킬 목록에 나온 경로):

```
python "<스킬폴더>/scripts/slide_generator.py" --output 발표.pptx --title "제목" --subtitle "부제" --slide1-title "첫 장" --slide1-bullets 가 나 다 --slide2-title "둘째 장" --slide2-bullets 라 마
```
- 제목 슬라이드 + 불릿 슬라이드 최대 2장. 그 이상은 MakeDoc(pptx) 이나 python-pptx 코드로.
