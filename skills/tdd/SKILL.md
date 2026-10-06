---
name: tdd
description: 시험 먼저 개발(TDD)·테스트 작성·테스트 실행. Test-driven development — write a failing test first, make it pass, refactor; add regression tests for bugs. "테스트 먼저", "TDD", "테스트 짜줘", "버그 재현 테스트" 요청이나, 새 함수·버그 수정 작업에 쓴다.
---

# 시험 먼저 개발 (tdd)

**빨강 → 초록 → 정리** 순서를 지킨다. 시험이 먼저 실패하는 것을 눈으로 확인하지 않으면 그 시험은 아무것도 증명하지 못한다.

## 0. 시험 도구 찾기
- 이미 있는 것을 쓴다: `pyproject.toml`/`pytest.ini`/`tests/`(pytest), `package.json` 의 `test` 스크립트(jest·vitest), `go test`, `cargo test`, `*.csproj`(dotnet test).
- 없으면 언어 기본값을 제안하고 사용자 허락 후 설치(파이썬: `python -m pip install pytest`).
- 기존 시험을 먼저 한 번 돌려 **출발점(통과/실패 수)** 을 기록한다. 원래 실패하던 시험은 내 탓이 아니므로 따로 적어 둔다.

## 1. 빨강 — 실패하는 시험 하나
1. 요구를 **관찰 가능한 동작** 한 가지로 쪼갠다(입력 → 기대 출력/예외/부작용).
2. 그 동작 하나만 확인하는 시험을 쓴다. 이름은 동작을 말한다: `test_divide_by_zero_raises_value_error`.
3. 실행해 **기대한 이유로** 실패하는지 확인한다(ImportError·오타 때문에 실패하면 빨강이 아니다).

## 2. 초록 — 통과시키는 최소 구현
- 시험을 통과시키는 가장 단순한 코드만 쓴다. 다음 요구를 미리 구현하지 않는다.
- 시험을 돌려 통과를 확인한다. **시험을 고쳐서 통과시키지 않는다**(시험이 틀렸다고 판단되면 이유를 사용자에게 말하고 고친다).

## 3. 정리 — 동작은 그대로, 코드만 깔끔하게
- 중복 제거·이름 정리·작은 함수로 나누기. 매 단계 뒤 전체 시험을 다시 돌린다.

## 4. 다음 동작으로 반복
경계값을 꼭 넣는다: 빈 입력, 0, 음수, 최댓값, None/null, 유니코드(한글), 아주 긴 입력, 중복, 순서 바뀜.

## 버그를 고칠 때
1. 먼저 **버그를 재현하는 시험**을 쓰고 실패를 확인한다(이게 회귀 시험이 된다).
2. 고친 뒤 그 시험과 전체 시험이 통과하는지 확인한다.

## 대화형·외부 의존 코드
- `input()` 루프: 로직을 함수로 빼서 직접 시험하고, 실행 확인은 표준 입력을 파이프로 넣는다.
  윈도우 PowerShell: `"10 + 20`n3 * 4`nq" | python calc.py` (`<` 리다이렉트는 PowerShell 에서 안 된다).
- 네트워크·시간·난수: 주입 가능한 매개변수로 바꾸거나 시험에서 대체(mock/monkeypatch)한다. 실제 외부 서버에 의존하는 시험은 쓰지 않는다.

## DB 를 쓰는 웹앱 시험 (FastAPI·SQLAlchemy 예)
- 시험 DB 는 실제 `salon.db` 같은 파일이 아니라 `tmp_path` 의 새 파일(또는 메모리)로. 순서는 **엔진 만들기 → `create_all` → 시드(관리자 계정 등) → 앱 의존성 바꾸기**.
  `no such table` 이 나오면 거의 항상 이 순서가 틀렸거나 앱이 다른 엔진을 보고 있다 — 픽스처를 고치기 전에 앱이 어느 엔진을 쓰는지 Read 로 확인한다.
  ```python
  # tests/conftest.py
  import pytest
  from fastapi.testclient import TestClient
  from sqlalchemy import create_engine
  from sqlalchemy.orm import sessionmaker
  from database import Base, get_db
  from main import app

  @pytest.fixture
  def client(tmp_path):
      engine = create_engine(f"sqlite:///{tmp_path/'test.db'}", connect_args={"check_same_thread": False})
      Base.metadata.create_all(engine)                      # 1) 표 먼저
      TestSession = sessionmaker(bind=engine)
      with TestSession() as s:                              # 2) 시드
          seed_admin(s)                                     #    (프로젝트의 시드 함수)
      def _db():
          with TestSession() as s:
              yield s
      app.dependency_overrides[get_db] = _db                # 3) 앱이 시험 DB 를 보게
      with TestClient(app) as c:
          yield c
      app.dependency_overrides.clear()
  ```
- 통과하던 시험 수가 줄면(예: 28 → 0) 그 직전 편집이 원인이다. 더 고치기 전에 그 편집을 되돌리고 다른 방법을 찾는다.
- 화면 경로(`/`, `/login` …)도 시험에 넣는다: `assert client.get("/login").status_code == 200`.

## 보고
- 추가한 시험 목록, 실행 명령, **실행 결과 원문 마지막 줄**(예: `12 passed in 0.31s`), 출발점 대비 변화.
- 통과하지 못한 시험이 있으면 숨기지 않고 실패 메시지와 함께 보고한다.
