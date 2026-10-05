---
name: security-review
description: 코드 보안 점검(보안 리뷰·취약점·시크릿 노출·인젝션·인증/권한·의존성). Security review of code changes — secrets, injection, authz, unsafe deserialization, path traversal, SSRF, dependency risk. 사용자가 "보안 점검", "취약점 확인", "security review"를 요청하거나, 인증·결제·파일 업로드·외부 입력을 다루는 코드를 바꾼 뒤에 쓴다.
---

# 보안 점검 (security-review)

변경된 코드(또는 지정한 범위)를 **공격자 관점**에서 읽고, 실제로 악용 가능한 문제만 근거와 함께 보고한다.
추측성 경고를 늘어놓지 않는다. 각 지적에는 **파일:줄 · 공격 시나리오 · 고치는 방법**이 있어야 한다.

## 1. 범위 정하기
1. 사용자가 범위를 주지 않았으면 `git status` · `git diff`(스테이징 포함 `git diff HEAD`)로 바뀐 파일을 본다. git 저장소가 아니면 사용자가 말한 폴더를 Glob 으로 훑는다.
2. 바뀐 코드가 닿는 **신뢰 경계**를 적는다: 외부 입력(HTTP 요청·CLI 인자·파일·환경 변수·외부 API 응답) → 처리 → 위험한 출구(DB·셸·파일 시스템·HTML 출력·네트워크).
3. TodoWrite 로 아래 점검 항목 중 해당하는 것만 목록화한다.

## 2. 점검 항목 (해당하는 것만)
| 분류 | 찾는 것 | 빠른 탐색 (Grep 패턴 예) |
|---|---|---|
| 시크릿 | 코드·설정·테스트·로그에 키·토큰·비밀번호·개인키 | `(api[_-]?key|secret|token|passw(or)?d)\s*[:=]`, `-----BEGIN .*PRIVATE KEY-----`, `AKIA[0-9A-Z]{16}` |
| 인젝션 | SQL 문자열 결합, 셸 명령 조립, eval/exec, 템플릿 직접 조립 | `execute\(.*(\+|%|f")`, `shell=True`, `os\.system`, `eval\(`, `exec\(`, `Invoke-Expression` |
| XSS | 이스케이프 없는 HTML 출력, **인라인 이벤트 속성 안 데이터**(HTML 이스케이프로는 `'` 를 못 막는다) | `innerHTML`, `dangerouslySetInnerHTML`, `\|safe`, `mark_safe`, `onclick="[^"]*\$\{` |
| 경로 이탈 | 사용자 입력으로 파일 경로 조립 | `open\(.*(request|input|args)`, `\.\./`, `Path\(.*\) / ` 뒤 resolve 검사 없음 |
| 인증·권한 | 권한 확인 없는 엔드포인트, IDOR(남의 id 로 접근), 관리자 기능 노출 | 라우트 정의 근처의 권한 데코레이터·미들웨어 유무 |
| 역직렬화 | 신뢰할 수 없는 데이터의 pickle/yaml.load/BinaryFormatter | `pickle\.loads?`, `yaml\.load\(` (SafeLoader 없이), `marshal` |
| SSRF | 사용자 URL 로 서버가 요청 | `requests\.(get|post)\(.*(url|request)`, `urlopen\(` |
| 암호 | 약한 해시로 비밀번호 저장, 고정 IV/키, 직접 만든 암호 | `md5`, `sha1` (비밀번호 용도), `random\.` (보안 용도) |
| 의존성 | 알려진 취약 버전, 출처 불명 패키지 | `requirements*.txt`, `package.json`, `pyproject.toml` 의 고정 버전 |
| 정보 노출 | 오류 메시지·로그에 내부 주소·스택·개인정보 | `traceback`, `print\(e\)`, `str\(e\)` 를 사용자에게 반환 |

## 3. 각 후보를 검증하기
- 후보마다 **입력이 정말 공격자 손에 있는지** 호출 경로를 Read 로 따라가 확인한다(이미 검증·이스케이프되면 제외).
- 가능하면 작은 재현으로 확인한다: 단위 시험을 하나 만들어 악성 입력(`'; DROP TABLE x;--`, `../../etc/passwd`, `<script>`, `$(whoami)`)이 막히는지 Bash 로 돌린다. 재현은 작업 폴더 안 임시 파일로 하고 끝나면 지운다.
- 확인하지 못한 것은 "가능성"으로 따로 분류하고 이유를 적는다.
- 판단이 애매하면 AskAI 로 다른 AI(claude·codex 등)에게 그 코드 조각과 시나리오만 보내 두 번째 의견을 받는다(시크릿·개인정보가 섞인 코드는 보내지 않는다).

## 4. 보고 형식
심각도 순으로:

```
[높음] src/api/user.py:42 — SQL 인젝션
  공격: GET /user?id=1 OR 1=1 → 전체 사용자 조회
  근거: cursor.execute(f"SELECT * FROM users WHERE id={uid}")  (uid 는 request.args 에서 그대로)
  고침: cursor.execute("SELECT * FROM users WHERE id = %s", (uid,))
```
- 심각도: 높음(원격·무인증 악용, 데이터 유출/변조) · 중간(인증 필요, 제한적 영향) · 낮음(심층 방어).
- 문제가 없으면 "점검한 범위와 항목, 발견 없음"을 분명히 쓴다.
- **사용자가 고치라고 하기 전에는 코드를 바꾸지 않는다.** 고칠 때는 각 수정 뒤 재현 시험이 막히는지 다시 돌린다.

## 하지 말 것
- 시크릿을 화면·보고서에 그대로 옮기지 않는다(앞 4자만 + `…`).
- 근거 없는 "잠재적 위험" 나열, 스타일 지적 섞기.
- 운영 시스템·외부 서버를 대상으로 공격 시험을 실행하지 않는다(로컬 재현만).
