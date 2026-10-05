---
name: pdf
description: |
  PDF 파일 읽기·추출·병합·분할. 문서 처리, 데이터 추출, 보고서 생성.
  Read, extract text, merge, split, and process PDF documents.
---

# PDF 스킬 가이드

## 언제 사용하나?

- **PDF 읽기**: 텍스트 추출, 페이지 정보 확인
- **페이지 분할**: 특정 페이지만 추출
- **여러 PDF 병합**: 보고서 통합
- **데이터 추출**: 표, 텍스트 크롤링
- **메타데이터 조회**: 페이지 수, 작성자 등
- **PDF 생성**: 마크다운 또는 HTML 기반

## 빠른 길 (내장 도구)

### 1. PDF 읽기 (텍스트 추출)

```
→ ReadDoc("문서.pdf")
출력: "PDF의 모든 텍스트 내용 (페이지별)"
```

### 2. PDF 미리보기 (페이지 확인)

```
→ PreviewDoc("문서.pdf")
출력: PNG 이미지 (첫 페이지 렌더링)
```

### 3. 마크다운에서 PDF 생성

```
사용자: "보고서.pdf를 만들어줘. 마크다운:
# 월간 보고서
## 목표 달성도
- 목표 A: 100% 달성
- 목표 B: 85% 달성
"
```

→ **MakeDoc("보고서.pdf", markdown, format="pdf")**

검증:
```
→ ReadDoc("보고서.pdf") 로 내용 확인
→ PreviewDoc("보고서.pdf") 로 레이아웃 확인
```

## 세밀한 작업 (pypdf, pdfplumber 라이브러리)

내장 도구로 안 되는 작업:
- **선택적 페이지 추출** (1,3,5번 페이지만)
- **여러 PDF 병합** (순서 유지)
- **PDF 분할** (N개 페이지씩)
- **테이블 추출** (표 구조 파악)
- **좌표 기반 텍스트 추출** (특정 영역만)
- **PDF 회전, 자르기**
- **이미지 추출**

### 예제 1: PDF 페이지 분할 (pypdf 사용)

```python
from pypdf import PdfReader, PdfWriter

# PDF 열기
reader = PdfReader("원본.pdf")
print(f"총 페이지 수: {len(reader.pages)}")

# 새로운 writer 생성
writer = PdfWriter()

# 특정 페이지만 추출: 1, 3, 5번 페이지 (0-indexed: 0, 2, 4)
for page_num in [0, 2, 4]:
    if page_num < len(reader.pages):
        writer.add_page(reader.pages[page_num])

# 분할된 PDF 저장
with open("분할.pdf", "wb") as f:
    writer.write(f)

print("✓ 분할 완료: 분할.pdf")
```

검증:
```
1. ReadDoc("분할.pdf") → 선택된 페이지 내용 확인
2. PreviewDoc("분할.pdf") → 페이지 수 확인 (3페이지여야 함)
```

### 예제 2: 여러 PDF 병합

```python
from pypdf import PdfReader, PdfWriter

# 여러 PDF 파일
pdf_files = ["문서1.pdf", "문서2.pdf", "문서3.pdf"]

writer = PdfWriter()

# 각 PDF 읽기 및 병합
for pdf_file in pdf_files:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

# 병합된 PDF 저장
with open("병합.pdf", "wb") as f:
    writer.write(f)

print("✓ 병합 완료: 병합.pdf")
```

검증:
```
ReadDoc("병합.pdf") → 모든 문서 내용 확인
→ 페이지 순서가 올바른지 확인
```

### 예제 3: 페이지 회전 및 자르기

```python
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

reader = PdfReader("원본.pdf")
writer = PdfWriter()

for page_num, page in enumerate(reader.pages):
    # 페이지 90도 회전
    page.rotate_clockwise(90)
    
    # 자르기: 좌상단(x0, y0)에서 우하단(x1, y1)
    # A4 페이지: 일반적으로 0,0 - 612,792
    crop_box = RectangleObject([0, 100, 600, 700])  # 상단 100, 하단 92 제거
    page.cropbox = crop_box
    
    writer.add_page(page)

with open("회전및자르기.pdf", "wb") as f:
    writer.write(f)

print("✓ 변환 완료: 회전및자르기.pdf")
```

검증:
```
PreviewDoc("회전및자르기.pdf") → 회전 및 자르기 확인
```

### 예제 4: 텍스트 및 테이블 추출 (pdfplumber 사용)

```python
import pdfplumber
import json

# PDF 열기
with pdfplumber.open("문서.pdf") as pdf:
    print(f"총 페이지 수: {len(pdf.pages)}")
    
    # 첫 번째 페이지에서 텍스트 추출
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    print("추출된 텍스트:")
    print(text[:500])  # 첫 500자
    
    # 첫 번째 페이지에서 테이블 추출
    tables = first_page.extract_tables()
    if tables:
        print("\n추출된 테이블:")
        for i, table in enumerate(tables):
            print(f"테이블 {i+1}:")
            for row in table:
                print(row)
    
    # 페이지별 텍스트 추출
    for page_num, page in enumerate(pdf.pages):
        print(f"\n페이지 {page_num + 1}: {len(page.extract_text())}자")
```

검증:
```
1. 스크립트 실행하여 텍스트/테이블 추출 확인
2. 추출된 데이터가 원본 PDF와 일치하는지 확인
```

### 예제 5: 특정 영역 추출 (좌표 기반)

```python
import pdfplumber

with pdfplumber.open("문서.pdf") as pdf:
    page = pdf.pages[0]
    
    # 특정 영역 정의: (x0, y0, x1, y1)
    # x0=0, y0=0, x1=612, y1=100: 상단 100 픽셀 영역
    crop_box = {
        "top": 0,
        "left": 0,
        "bottom": 100,
        "right": 612
    }
    
    # 해당 영역의 텍스트 추출
    cropped_page = page.crop((crop_box["left"], crop_box["top"], 
                              crop_box["right"], crop_box["bottom"]))
    text = cropped_page.extract_text()
    print("추출된 텍스트:")
    print(text)
    
    # 해당 영역의 테이블 추출
    tables = cropped_page.extract_tables()
    if tables:
        print("\n추출된 테이블:")
        for table in tables:
            print(table)
```

## 검증 단계

1. **ReadDoc 확인** → 텍스트 추출 검증
   ```
   ReadDoc("문서.pdf")
   → 모든 페이지의 텍스트 내용 확인
   ```

2. **PreviewDoc 확인** → 시각적 확인
   ```
   PreviewDoc("문서.pdf")
   → PNG 이미지로 첫 페이지 확인
   ```

3. **페이지 수 확인** → 분할/병합 후
   ```
   ReadDoc("분할.pdf") → 페이지 수 확인
   ```

4. **메타데이터 확인** (python-docx 스크립트 사용)
   ```python
   from pypdf import PdfReader
   reader = PdfReader("문서.pdf")
   print(f"페이지 수: {len(reader.pages)}")
   print(f"메타데이터: {reader.metadata}")
   ```

## 흔한 함정

| 함정 | 해결책 |
|------|--------|
| 텍스트 추출 시 인코딩 오류 | pdfplumber 사용 (더 안정적) |
| 테이블이 추출 안 됨 | pdfplumber로 `extract_tables()` 시도 |
| 페이지 좌표 혼동 | PDF 좌표: 좌하단(0,0), PDF 미리보기로 확인 |
| 병합 후 페이지 순서 오류 | 파일 리스트 순서 재확인 |
| 파일이 열려 있음 | 저장 전에 PDF 뷰어에서 닫혀 있는지 확인 |
| 이미지 기반 PDF (스캔) | 텍스트 추출 안 됨 → OCR 도구 필요 |

## 추천 워크플로우

```
1. 간단한 PDF 읽기 → ReadDoc + PreviewDoc
2. 페이지 분할/병합 → pypdf 스크립트
3. 텍스트/테이블 추출 → pdfplumber 스크립트
4. PDF 생성 → MakeDoc(마크다운, format="pdf")
5. 복합 작업 → 위 스크립트 조합
```

## 추가 팁

### PDF 생성 시 이미지 포함 (마크다운)

```markdown
# 보고서

![차트](chart.png)

## 설명
위의 차트는...
```

MakeDoc에서 format="pdf"로 지정하면 이미지도 포함됨.

### PDF 메타데이터 설정 (pypdf)

```python
from pypdf import PdfWriter

writer = PdfWriter()
# ... 페이지 추가 ...

writer.add_metadata({
    "/Title": "내 보고서",
    "/Author": "작성자",
    "/Subject": "주제",
})

with open("메타데이터.pdf", "wb") as f:
    writer.write(f)
```

### 암호 보호 PDF

```python
from pypdf import PdfWriter

writer = PdfWriter()
# ... 페이지 추가 ...

# 사용자 암호: "user123", 소유자 암호: "owner456"
writer.encrypt("user123", "owner456")

with open("암호보호.pdf", "wb") as f:
    writer.write(f)
```


## 보조 스크립트 (이 SKILL.md 와 같은 폴더의 `scripts/`)

SKILL.md 경로의 폴더를 `<스킬폴더>` 라 할 때(설치 위치는 스킬 목록에 나온 경로):

```
python "<스킬폴더>/scripts/pdf_processor.py" --mode info    --input a.pdf
python "<스킬폴더>/scripts/pdf_processor.py" --mode extract --input a.pdf
python "<스킬폴더>/scripts/pdf_processor.py" --mode split   --input a.pdf --output 일부.pdf --pages 1 2
python "<스킬폴더>/scripts/pdf_processor.py" --mode merge   --input a.pdf b.pdf --output 합본.pdf
```
- `--pages` 는 1부터 세는 쪽 번호를 **띄어쓰기로** 나열한다(`1-2` 같은 범위 표기는 안 된다).
