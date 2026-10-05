---
name: docx
description: Word 문서(.docx) 생성·편집·읽기 — 보고서·서신·제안서·이력서·표가 있는 문서, 한글 글꼴. Create, read and edit Microsoft Word documents.
---

# DOCX 스킬 가이드

## 언제 사용하나?

- **문서 생성**: 마크다운 기반 보고서를 Word로
- **기존 문서 편집**: docx 파일의 특정 부분 수정
- **내용 읽기**: docx 파일을 텍스트로 추출
- **서식 보존**: 글꼴, 제목, 단락 스타일 유지 필요 시

## 빠른 길 (내장 도구)

### 1. 마크다운에서 Word 생성

```
사용자: "계획안.docx를 만들어줘. 마크다운:
# 프로젝트 계획
## 목표
...
"
```

→ **MakeDoc(file_path, markdown, format="docx")**
```
응답: "계획안.docx를 생성했습니다."
```

검증:
```
→ ReadDoc("계획안.docx") 로 내용 확인
→ PreviewDoc("계획안.docx") 로 레이아웃 확인
```

### 2. 기존 문서 읽기

```
→ ReadDoc("기존파일.docx")
출력: "내용을 텍스트로 반환"
```

### 3. 문서 일부 수정 (서식 유지)

```
→ EditDoc("파일.docx", "찾을_텍스트", "새_텍스트")
출력: "수정 완료"
```

검증: ReadDoc 으로 변경된 부분 확인

## 세밀한 작업 (python-docx 라이브러리)

내장 도구로 안 되는 작업:
- **표 생성/편집** (표 서식, 병합 셀)
- **이미지/차트 삽입**
- **글꼴, 색상, 정렬 스타일 세부 조정**
- **머리글/바닥글 추가**
- **다단계 목록 또는 양식**
- **문서 내 하이퍼링크 추가**

### 예제 1: 표가 있는 문서 만들기

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

doc = Document()

# 제목
title = doc.add_paragraph("판매 현황 보고서")
title.style = 'Heading 1'

# 표 추가: 3행 3열
table = doc.add_table(rows=3, cols=3)
table.style = 'Light Grid Accent 1'

# 헤더 행
hdr_cells = table.rows[0].cells
hdr_cells[0].text = '월'
hdr_cells[1].text = '판매액'
hdr_cells[2].text = '성장률'

# 데이터 행
table.rows[1].cells[0].text = '1월'
table.rows[1].cells[1].text = '100만원'
table.rows[1].cells[2].text = '10%'

table.rows[2].cells[0].text = '2월'
table.rows[2].cells[1].text = '150만원'
table.rows[2].cells[2].text = '50%'

doc.save("보고서.docx")
```

검증:
```
1. ReadDoc("보고서.docx") → 표 내용 확인
2. PreviewDoc("보고서.docx") → 표 레이아웃 확인
```

### 예제 2: 글꼴 및 색상 지정 (한글 포함)

```python
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def set_korean_font(run, font_name="맑은 고딕", size=11, bold=False, color=None):
    """
    한글 글꼴 설정 (eastAsia 속성 필요)
    """
    run.font.name = font_name  # 영문 폴백
    run.font.size = Pt(size)
    run.font.bold = bold
    
    # eastAsia 속성: 한글 글꼴 지정
    rFonts = run.font._element.get_or_add_rFonts()
    rFonts.set(qn('w:eastAsia'), font_name)
    
    if color:
        run.font.color.rgb = color

doc = Document()

# 제목 (한글 + 파란색)
para = doc.add_paragraph()
run = para.add_run("중요한 공지")
set_korean_font(run, "맑은 고딕", 14, bold=True, color=RGBColor(0, 0, 255))

# 본문 (한글)
para = doc.add_paragraph()
run = para.add_run("이것은 한글 문서입니다. 맑은 고딕으로 표시됩니다.")
set_korean_font(run, "맑은 고딕", 11)

doc.save("한글문서.docx")
```

검증:
```
1. ReadDoc("한글문서.docx") → 텍스트 내용 확인
2. PreviewDoc("한글문서.docx") → 글꼴 및 색상 확인
```

### 예제 3: 이미지 삽입

```python
from docx import Document
from docx.shared import Inches

doc = Document()
doc.add_paragraph("이미지 예제")
doc.add_picture("이미지경로.png", width=Inches(4))
doc.save("이미지포함.docx")
```

## 검증 단계

1. **MakeDoc 사용** → 문서 생성
   ```
   MakeDoc("output.docx", "# 제목\n본문", format="docx")
   ```

2. **ReadDoc 확인** → 내용 검증
   ```
   ReadDoc("output.docx")
   → 텍스트 내용이 올바른지 확인
   ```

3. **PreviewDoc 확인** → 시각적 확인
   ```
   PreviewDoc("output.docx")
   → PNG로 렌더링되어 모양 확인
   ```

4. **수정 필요 시 EditDoc**
   ```
   EditDoc("output.docx", "찾을_텍스트", "새_텍스트")
   ```

## 흔한 함정

| 함정 | 해결책 |
|------|--------|
| 한글이 깨짐 | `rFonts.set(qn('w:eastAsia'), "맑은 고딕")` 필수 |
| 서식이 사라짐 | EditDoc만 사용 (MakeDoc은 마크다운 기반이므로 제한적) |
| 표 병합 불가 | EditDoc으로는 안 됨 → python-docx로 직접 처리 |
| 이미지 경로 오류 | 절대경로 또는 현재 디렉토리 기준 확인 |
| 파일이 열려 있음 | 저장 전에 파일이 Word에서 닫혀 있는지 확인 |

## 추천 워크플로우

```
1. 간단한 보고서 → MakeDoc(마크다운) + ReadDoc 검증
2. 기존 문서 수정 → ReadDoc(내용 확인) → EditDoc(수정) → ReadDoc(검증)
3. 복잡한 서식 필요 → python-docx 스크립트 + MakeDoc 저장
4. 한글 포함 → 반드시 eastAsia 글꼴 속성 지정
```


## 보조 스크립트 (이 SKILL.md 와 같은 폴더의 `scripts/`)

SKILL.md 경로의 폴더를 `<스킬폴더>` 라 할 때(설치 위치는 스킬 목록에 나온 경로):

```
python "<스킬폴더>/scripts/table_builder.py" --output 보고서.docx --title "제목" --rows 3 --cols 2 --headers 이름 값
```
- `--headers` 는 **띄어쓰기로** 구분한다(쉼표로 쓰면 한 칸에 들어간다). 만든 뒤 ReadDoc 으로 확인.
