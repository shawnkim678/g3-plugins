# g3-plugins — G3 Code 필수 스킬 묶음 (`g3-essentials`)

G3 Code(온프렘 G3 모델 코딩 CLI)용 스킬 모음. Claude Code 와 같은 `skills/*/SKILL.md` 형식이다.

## 설치

```
g3 plugin marketplace add shawnkim678/g3-plugins
g3 plugin list
```
G3 게이트웨이가 이 저장소를 커밋 고정으로 받아 라이선스·위험도를 검사한 보고서를 보여 주고, 승인하면 `%USERPROFILE%\.g3\plugins\` 에 설치한다.

## 스킬

| 스킬 | 하는 일 | 출처·라이선스 |
|---|---|---|
| `docx` | Word 문서 생성·편집·읽기 (MakeDoc 우선, python-docx) | 새로 작성 · MIT |
| `pptx` | PowerPoint 생성·편집 (MakeDoc 우선, python-pptx) | 새로 작성 · MIT |
| `xlsx` | Excel 표·수식·서식 (MakeDoc 우선, openpyxl) | 새로 작성 · MIT |
| `pdf` | PDF 읽기·분할·병합·표 추출 (pypdf, pdfplumber) | 새로 작성 · MIT |
| `hwpx` | 한글 HWPX 생성·서식 채우기·읽기·검증 (MakeDoc 우선, python-hwpx) | 새로 작성 · MIT |
| `security-review` | 보안 점검(시크릿·인젝션·권한·SSRF 등) | 새로 작성 · MIT |
| `tdd` | 시험 먼저 개발·회귀 시험 | 새로 작성 · MIT |
| `debugging` | 재현→가설 검증→근본 원인 수정 | 새로 작성 · MIT |
| `web-research` | 웹 검색·수집·교차 확인·출처 인용 (WebSearch·WebFetch) | 새로 작성 · MIT |
| `api-integration` | 외부 REST API 연동·비밀 처리·재시도·시험 (HttpRequest·httpx) | 새로 작성 · MIT |
| `frontend-design` | 개성 있는 웹 UI 디자인 | anthropics/claude-plugins-official · Apache-2.0 (수정) |
| `code-review` | 코드·PR 리뷰 | 〃 code-review + pr-review-toolkit · Apache-2.0 (수정) |
| `git-commit` | 커밋·푸시·PR·정리 | 〃 commit-commands · Apache-2.0 (수정) |
| `feature-dev` | 탐색→설계→구현→검토 단계별 기능 개발 | 〃 feature-dev · Apache-2.0 (수정) |
| `code-simplifier` | 동작은 그대로 코드 단순화 | 〃 code-simplifier · Apache-2.0 (수정) |

- Apache-2.0 파생 파일은 각 SKILL.md 머리에 출처·수정 고지가 있고, 전문은 `LICENSES/Apache-2.0.txt`, 고지는 `NOTICE`.
- Anthropic 의 독점 라이선스 스킬(문서 스킬, claude-security 등)은 포함하지 않으며 참고하지도 않았다.
- 오피스 스킬의 보조 스크립트는 python-docx·python-pptx·openpyxl(MIT), pypdf(BSD-3-Clause), pdfplumber(MIT), python-hwpx(Apache-2.0) 를 쓴다. 없으면 G3 가 사용자 허락을 받아 `pip install` 한다.
