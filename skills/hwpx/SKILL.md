---
name: hwpx
description: 한글(한컴오피스) 문서 HWPX 생성·편집·읽기 — 공문·보고서·서식·양식 채우기·법원/관공서 제출 문서·표·머리말. Create, edit, fill templates and read Hancom HWPX (.hwpx) documents.
---

# 한글 HWPX 문서 (hwpx)

## 언제 쓰나
- "한글 파일로", ".hwpx", "공문", "관공서·법원 제출", "한글 서식에 채워줘" 요청.
- `.hwp`(옛 바이너리 형식)는 직접 고치지 않는다 — 한컴오피스에서 HWPX 로 다시 저장해 달라고 안내한다(읽기만 필요하면 ReadDoc 시도).

## 빠른 길 — G3 내장 도구 먼저
| 할 일 | 도구 |
|---|---|
| 새 문서 | `MakeDoc {file_path: "보고.hwpx", format: "hwpx", markdown: "..."}` — `#` 제목, 문단, 마크다운 표가 HWPX 로 |
| 읽기 | `ReadDoc {file_path}` — 본문을 텍스트로 |
| 글자 바꾸기(서식 유지) | `EditDoc {file_path, old_text, new_text}` |
| 모양 확인 | `PreviewDoc {file_path}` — 첫 쪽 PNG (변환기가 없으면 건너뛰고 ReadDoc 로 확인) |

간단한 보고서·메모는 MakeDoc 하나로 끝낸다. 만든 뒤 **반드시 ReadDoc 으로 내용 확인**.

## 세밀한 작업 — python-hwpx (Apache-2.0)
머리말·쪽 여백·표 칸 하나하나·양식(누름틀) 채우기·여러 자리 치환이 필요할 때.
프로젝트 가상환경에 설치: `.venv\Scripts\python -m pip install python-hwpx` (전역 설치 금지).
아래 코드는 python-hwpx 6.7 에서 실행해 확인했다(폐기 예정 API 없음).

```python
from hwpx.document import HwpxDocument

doc = HwpxDocument.new()
doc.add_heading("2026년 3분기 매출 보고", level=1)
doc.add_paragraph("작성: {{작성자}} · 2026-10-05")
doc.add_paragraph("3분기 매출은 전 분기 대비 12% 증가했다.")

rows = [("분기", "매출(원)", "증감률"), ("2분기", "120,000,000", "-"), ("3분기", "134,400,000", "+12%")]
t = doc.add_table(len(rows), 3)
for r, row in enumerate(rows):
    for c, v in enumerate(row):
        t.set_cell_text(r, c, v)          # 칸 서식 유지

doc.page.set_header(text="영업팀 내부 보고")
doc.save_to_path("report.hwpx")
```

### 서식(템플릿)에 채우기
사용자가 준 `.hwpx` 서식의 자리표시(`{{이름}}` 같은 글자)를 바꾼다 — 원본은 복사해 두고 사본을 고친다.
```python
from hwpx.document import HwpxDocument
d = HwpxDocument.open("서식.hwpx")
for k, v in {"{{작성자}}": "김영업", "{{날짜}}": "2026-10-05"}.items():
    n = d.text.replace(k, v)              # 바꾼 개수를 돌려준다 — 0 이면 자리표시가 없다는 뜻
    print(k, n)
d.save_to_path("채운_문서.hwpx")
```
- 표 안 칸을 이름표로 찾을 땐 `d.find_cell_by_label(...)`, 누름틀은 `d.list_form_fields()` / `d.fill_form_field(...)` 를 먼저 목록으로 확인하고 쓴다(서식마다 다르므로 목록 출력부터).

### 확인
```python
from hwpx.document import HwpxDocument
d = HwpxDocument.open("report.hwpx")
print(d.text.plain()[:500])               # 본문 확인
print(d.validate())                       # issues=() 이면 구조 정상
```

## 보조 스크립트 (이 SKILL.md 와 같은 폴더의 `scripts/`)
```
python "<스킬폴더>/scripts/hwpx_report.py" --output 보고.hwpx --title "제목" --para "첫 문단" --para "둘째 문단" --table "분기,매출" --table "3분기,134400000" --header "머리말"
python "<스킬폴더>/scripts/hwpx_report.py" --fill 서식.hwpx --output 채운.hwpx --set "{{작성자}}=김영업" --set "{{날짜}}=2026-10-05"
```
- `--table` 은 한 번에 한 행(쉼표 구분), 첫 행이 머리행. 끝나면 본문 앞부분과 검증 결과를 출력한다.

## 흔한 함정
- **바꾼 개수 0**: 자리표시가 서로 다른 글자 조각(run)으로 쪼개져 있으면 못 찾는다 — 한컴오피스에서 자리표시를 한 번에 다시 입력해 저장하거나, ReadDoc 출력으로 실제 글자를 확인.
- 한글 글꼴·문단 모양은 새 문서의 기본 스타일을 따른다. 기관 서식이 있으면 **서식 파일을 받아 채우는 쪽**이 모양이 정확하다.
- 저장 뒤 `validate()` 에 issues 가 있으면 사용자에게 알리고 한컴오피스로 열어 확인하라고 안내.
- 윈도우 PowerShell 에서 여러 줄 파이썬은 `python -c` 대신 .py 파일로 만들어 실행.
