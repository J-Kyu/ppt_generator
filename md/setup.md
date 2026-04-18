# 개발 환경 세팅 (Development Setup)

이 문서는 `ppt-generator` 프로젝트의 로컬 개발 환경을 구성하고 실행하는 방법을 안내합니다.
이 프로젝트는 의존성 관리 및 빠르고 일관된 가상 환경 구성을 위해 [uv](https://docs.astral.sh/uv/)를 사용합니다.

## 🛠 필수 요구 사항 (Prerequisites)

- **Python**: `>= 3.13`
- **패키지 관리자**: `uv`

### `uv` 설치
`uv`가 로컬에 설치되어 있지 않다면 아래 명령어를 통해 먼저 설치해야 합니다.

**Mac / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```
*(설치 후 터미널을 다시 시작해야 할 수 있습니다.)*

---

## 🚀 환경 구성 및 패키지 설치

### 1. 의존성 패키지 동기화 및 설치
프로젝트 최상위 디렉토리(루트)에서 다음 명령어를 실행합니다.
이 명령어는 자동으로 `.venv` 폴더(가상 환경)를 생성하고 `pyproject.toml` 및 `uv.lock`에 정의된 패키지들을 설치합니다.

```bash
uv sync
```
*참고: 여기에는 `flet`, `pydantic`, `python-pptx`, `pyinstaller` 등 필수 라이브러리와 `ruff`와 같은 개발용(dev) 라이브러리가 함께 설치됩니다.*

### 2. 가상 환경 활성화 (선택 사항)
`uv run` 명령어를 사용하면 가상 환경을 활성화하지 않아도 스크립트를 올바르게 실행할 수 있습니다. 하지만 IDE나 터미널에서 명시적으로 가상 환경을 활성화하려면 아래를 실행하세요.

**Mac / Linux:**
```bash
source .venv/bin/activate
```

**Windows:**
```powershell
.venv\Scripts\activate
```

---

## ▶️ 애플리케이션 실행

프로젝트 폴더 내 최상단에 있는 `main.py`를 실행하여 초기 애플리케이션이 정상적으로 동작하는지 테스트합니다.

```bash
uv run main.py
```
> 터미널에 `Hello from ppt-generator!` 메시지가 뜨면 정상적으로 설정된 것입니다.

---

## 🧹 포맷팅 및 린팅 (Linting & Formatting)

이 프로젝트는 빠르고 강력한 파이썬 린터이자 포맷터인 **Ruff**를 사용합니다.
코드를 커밋하거나 push하기 전에 포맷팅 및 린트를 실행하는 것을 권장합니다.

**✅ 코드 포맷팅 실행:**
```bash
uv run ruff format .
```

**✅ 린트 검사(에러 확인) 및 자동 수정:**
```bash
uv run ruff check .
uv run ruff check --fix .
```
