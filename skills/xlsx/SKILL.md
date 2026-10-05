---
name: xlsx
description: |
  엑셀 스프레드시트(.xlsx) 생성·편집·읽기. 표, 수식, 차트, 데이터 분석.
  Create, read, and edit Excel spreadsheets with formulas and formatting.
---

# XLSX 스킬 가이드

## 언제 사용하나?

- **데이터 테이블 생성**: 마크다운 표를 엑셀로
- **기존 스프레드시트 편집**: 셀 값 수정
- **내용 읽기**: xlsx 파일을 텍스트로 추출
- **수식 추가**: SUM, AVERAGE, IF 등 자동 계산
- **차트, 포맷팅**: 조건부 서식, 병합 셀

## 빠른 길 (내장 도구)

### 1. 마크다운 표에서 엑셀 생성

마크다운 표가 자동으로 각 행을 시트 행으로 변환:

```
사용자: "판매.xlsx를 만들어줘. 마크다운:
| 분기 | 판매액 | 성장률 |
|------|--------|--------|
| Q1   | 100만  | 10%    |
| Q2   | 150만  | 50%    |
"
```

→ **MakeDoc("판매.xlsx", markdown, format="xlsx")**

결과: A1:C3 범위의 표 (헤더 + 2행 데이터)

검증:
```
→ ReadDoc("판매.xlsx") 로 내용 확인
```

### 2. 스프레드시트 읽기

```
→ ReadDoc("판매.xlsx")
출력: "시트별, 셀별 내용"
```

### 3. 셀 데이터 수정 (기본)

```
→ EditDoc("판매.xlsx", "100만", "120만")
출력: "수정 완료"
```

주의: EditDoc은 값만 수정, 수식/서식은 별도 처리

## 세밀한 작업 (openpyxl 라이브러리)

내장 도구로 안 되는 작업:
- **수식 입력** (SUM, AVERAGE, IF, VLOOKUP)
- **여러 시트** (Sheet1, Sheet2, ...)
- **병합 셀, 조건부 서식**
- **차트, 그래프**
- **셀 색상, 글꼴 스타일, 테두리**
- **데이터 유효성 (Dropdown)**
- **피벗 테이블**

### 예제 1: 기본 스프레드시트 (데이터 + 수식)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "판매현황"

# 헤더 행
headers = ["분기", "판매액", "성장률", "누적액"]
ws.append(headers)

# 데이터 행
ws.append(["Q1", 1000000, 0.10, None])
ws.append(["Q2", 1500000, 0.50, None])
ws.append(["Q3", 2000000, 0.33, None])

# 수식: 누적액 = 현재액 + 이전액
# D2 = C2 (Q1은 누적액 = 판매액)
ws['D2'] = "=B2"
# D3 = D2 + B3
ws['D3'] = "=D2+B3"
# D4 = D3 + B4
ws['D4'] = "=D3+B4"

# 헤더 서식
header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
header_font = Font(bold=True, color="FFFFFF")

for cell in ws[1]:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")

# 숫자 포맷: 천단위 구분
for row in ws.iter_rows(min_row=2, max_row=4, min_col=2, max_col=2):
    for cell in row:
        cell.number_format = '#,##0'

# 백분율 포맷
for row in ws.iter_rows(min_row=2, max_row=4, min_col=3, max_col=3):
    for cell in row:
        cell.number_format = '0%'

# 열 너비 조정
ws.column_dimensions['A'].width = 10
ws.column_dimensions['B'].width = 15
ws.column_dimensions['C'].width = 12
ws.column_dimensions['D'].width = 12

wb.save("판매현황.xlsx")
```

검증:
```
1. ReadDoc("판매현황.xlsx") → 헤더, 데이터, 수식 확인
   (수식 계산값이 올바른지 확인)
2. 엑셀에서 직접 열어서 D2, D3, D4 셀 값이 계산되었는지 확인
```

### 예제 2: 여러 시트 (Sheet 분리)

```python
from openpyxl import Workbook

wb = Workbook()

# 첫 번째 시트 (기본값)
ws1 = wb.active
ws1.title = "2026년 Q1"
ws1.append(["1월", "100만"])
ws1.append(["2월", "120만"])
ws1.append(["3월", "130만"])

# 새로운 시트 추가
ws2 = wb.create_sheet("2026년 Q2")
ws2.append(["4월", "140만"])
ws2.append(["5월", "150만"])
ws2.append(["6월", "160만"])

# 또 다른 시트
ws3 = wb.create_sheet("요약")
ws3.append(["분기", "총액"])
ws3.append(["Q1", "=SUM('2026년 Q1'!B:B)"])  # Q1 총합
ws3.append(["Q2", "=SUM('2026년 Q2'!B:B)"])  # Q2 총합

wb.save("분기별.xlsx")
```

검증:
```
ReadDoc("분기별.xlsx")
→ 각 시트(Q1, Q2, 요약) 내용 확인
→ 요약 시트의 SUM 수식이 계산되었는지 확인
```

### 예제 3: 조건부 서식 및 데이터 유효성

```python
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import ColorScaleRule
from openpyxl.worksheet.datavalidation import DataValidation

wb = Workbook()
ws = wb.active

# 헤더
ws.append(["제품", "판매량", "평가"])

# 데이터
ws.append(["제품A", 100, None])
ws.append(["제품B", 50, None])
ws.append(["제품C", 200, None])
ws.append(["제품D", 150, None])

# 1. 색상 그라데이션 (판매량에 따라 초록색~빨간색)
# B2:B5 범위에 Color Scale 적용
color_scale_rule = ColorScaleRule(
    start_type="min", start_color="63BE7B",  # 초록색
    mid_type="percentile", mid_value=50, mid_color="FFEB84",  # 노란색
    end_type="max", end_color="F8696B"  # 빨간색
)
ws.conditional_formatting.add(f'B2:B5', color_scale_rule)

# 2. 데이터 유효성: C열에 드롭다운 메뉴
dv = DataValidation(type="list", formula1='"좋음,보통,나쁨"', allow_blank=False)
dv.error = '좋음, 보통, 나쁨 중 하나를 선택하세요'
dv.errorTitle = '유효성 오류'
ws.add_data_validation(dv)
dv.add(f'C2:C5')  # C2부터 C5까지 적용

ws.column_dimensions['A'].width = 12
ws.column_dimensions['B'].width = 10
ws.column_dimensions['C'].width = 10

wb.save("조건부서식.xlsx")
```

검증:
```
1. ReadDoc("조건부서식.xlsx") → 데이터 확인
2. 엑셀에서 직접 열어서:
   - B2:B5가 초록~빨강 그라데이션으로 표시되는지 확인
   - C2:C5 셀을 클릭해서 드롭다운이 작동하는지 확인
```

## 검증 단계

1. **MakeDoc 사용** → 스프레드시트 생성
   ```
   MakeDoc("데이터.xlsx", "마크다운 표", format="xlsx")
   ```

2. **ReadDoc 확인** → 내용 검증
   ```
   ReadDoc("데이터.xlsx")
   → 모든 셀 값과 수식 확인
   ```

3. **수식 계산 확인** → 엑셀에서 직접 열기
   ```
   엑셀에서 파일 열기
   → SUM, AVERAGE 등 수식의 계산값 확인
   ```

4. **수정 필요 시 EditDoc**
   ```
   EditDoc("데이터.xlsx", "100", "120")
   ```

## 흔한 함정

| 함정 | 해결책 |
|------|--------|
| 수식이 계산되지 않음 | 엑셀에서 파일을 열어야 수식 계산됨 (ReadDoc는 수식 원문만 표시) |
| 다른 시트 참조 오류 | `'시트명'!셀` 형식 사용, 시트명에 공백 있으면 `'시트 명'!셀` |
| 숫자 서식 미적용 | `cell.number_format = '#,##0'` (천단위) 또는 `'0%'` (백분율) |
| 한글 폰트 미지정 | openpyxl은 기본 폰트 사용, 별도 설정 불필요 |
| 병합 셀 충돌 | `merge_cells("A1:C1")` 사용 전에 범위 확인 |
| 파일이 열려 있음 | 저장 전에 엑셀에서 닫혀 있는지 확인 |

## 추천 워크플로우

```
1. 간단한 표 → MakeDoc(마크다운 표) + ReadDoc 검증
2. 기존 스프레드시트 수정 → ReadDoc(내용 확인) → EditDoc(값 수정)
3. 수식 필요 → openpyxl 스크립트로 직접 작성
4. 복잡한 서식/차트 → openpyxl 또는 수동으로 엑셀에서 작성
5. 수식 검증 → 반드시 엑셀에서 열어서 계산값 확인
```

## 추가 팁

### 대량 데이터 처리
```python
# 리스트에서 한 번에 추가
data = [
    ["이름", "나이", "부서"],
    ["홍길동", 30, "영업"],
    ["김철수", 28, "개발"],
]
for row in data:
    ws.append(row)
```

### 범위 순회
```python
# 특정 범위의 모든 셀 순회
for row in ws.iter_rows(min_row=2, max_row=10, min_col=1, max_col=3):
    for cell in row:
        print(cell.value)
```


## 보조 스크립트 (이 SKILL.md 와 같은 폴더의 `scripts/`)

SKILL.md 경로의 폴더를 `<스킬폴더>` 라 할 때(설치 위치는 스킬 목록에 나온 경로):

```
python "<스킬폴더>/scripts/formula_builder.py" --output 현황.xlsx --type sales     # 또는 --type budget
```
- openpyxl 은 수식을 **저장만** 한다. 계산값은 엑셀/LibreOffice 에서 열어야 생긴다.
