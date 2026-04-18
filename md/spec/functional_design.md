# 기능적 설계 명세 (Functional Design Specification)

이 문서는 `overview.md`, `tech_spec.md`, `ui_ux.md`를 바탕으로 실제 코드로 구현하기 위한 대략적인 기능 단위의 설계와 컴포넌트 구조를 정의합니다.

## 1. 시스템 컴포넌트 아키텍처 및 디렉토리 구조

프로젝트는 명확한 관심사 분리(Separation of Concerns)를 위해 역할에 따라 폴더와 모듈을 분리합니다.

```text
src/
├── main.py                # 진입점 (Flet 앱 실행 및 초기화)
├── core/                  # 비즈니스 로직 및 데이터 제어 계층
│   ├── engine.py          # python-pptx 기반 PPT 분석 및 생성 로직
│   └── schema.py          # Pydantic 모델 (JSON 직렬화 및 데이터 무결성 검증)
├── state/                 # 전역 상태 관리
│   └── app_state.py       # 업로드된 파일 경로, 파싱된 스키마, 사용자 입력 상태 저장
└── ui/                    # Flet GUI 계층
    ├── app.py             # 화면 라우팅 및 뷰(View) 전환 관리자
    ├── components/        # 재사용 가능한 UI 조각 (버튼, 다이얼로그, 로딩 스피너 등)
    └── views/             # UI/UX 4단계에 매칭되는 각 화면 단위
        ├── onboarding.py  # 1단계: 드래그 앤 드롭 및 파일 업로드 화면
        ├── analysis.py    # 2단계: 분석 결과 리스트 기반 확인 화면
        ├── entry_form.py  # 3단계: JSON 스키마 기반 동적 폼 입력 화면
        └── export.py      # 4단계: 최종 생성 버튼 및 결과(성공/실패) 화면
```

---

## 2. 핵심 모듈 및 인터페이스 (Core Modules)

### 2.1. 데이터 스키마 모델 (`core/schema.py`)
데이터의 흐름을 통제하고 런타임 오류를 방지하기 위해 `Pydantic`을 사용합니다.
- `ShapeSchema`: 개별 텍스트 박스/이미지 영역의 정보 (id, name, type, 내용)
- `SlideSchema`: 슬라이드 번호 및 포함된 `ShapeSchema` 리스트
- `PptSchema`: 전체 프레젠테이션 정보 및 `SlideSchema` 리스트, 템플릿 원본 경로

### 2.2. 로직 엔진 (`core/engine.py`)
UI와 독립적으로 작동하는 순수 파이썬 클래스로 기능합니다.
- `analyze_ppt(file_path: str) -> PptSchema`
  - 원본 PPTX 파일을 로드하고, **마스터 슬라이드와 레이아웃 슬라이드**를 분석하여 사용할 수 있는 레이아웃의 고유 식별자와 텍스트 입력 요소를 추출하여 반환합니다.
- `generate_ppt(template_path: str, user_deck: List[SlideSchema], output_path: str) -> bool`
  - 원본 템플릿의 사본(빈 문서 형태)을 만든 뒤, 사용자가 조합(Construct)한 `user_deck`의 순서대로 지정된 레이아웃 슬라이드를 추가(Add Slide)합니다.
  - 추가된 슬라이드의 지정된 문자열 영역에 사용자가 작성한 텍스트를 매핑삽입하고, 결과물을 `output_path`로 저장합니다.

### 2.3. 전역 상태 중앙 제어 (`state/app_state.py`)
Flet의 페이지 전환 시 데이터 유실을 막기 위해 싱글톤(Singleton) 패턴 또는 Flet의 `page.session` 등을 활용하여 데이터를 저장합니다.
- 보관 항목: 업로드한 원본 파일 경로, 엔진이 반환한 `PptSchema` 원본, 사용자가 폼에 입력 중인 현재 상태 값.

---

## 3. UI 뷰(View) 별 세부 기능 정의 (`ui/views/`)

### View 1: 업로드 화면 (`onboarding.py`)
- **기능:** 파일 선택 창 호출(File_picker) 및 드래그 앤 드롭 이벤트 수신.
- **예외 처리:** 확장자가 `.pptx`가 아닌 경우 경고 모달(Snackbar) 노출.
- **액션:** 올바른 파일 인식 후 `engine.analyze_ppt` 호출. 로딩 상태 표시.

### View 2: 분석된 레이아웃 선택 화면 (`layout_picker.py` 또는 `analysis.py`)
- **기능:** 추출된 `PptSchema`에서 가용 레이아웃 목록(Slide Layouts)을 요약 정보 및 썸네일과 함께 명시적으로 보여줍니다.
- **액션:** 사용자가 본문, 제목, 갤러리 이미지 등 본인이 원하는 레이아웃을 선택합니다.

### View 3: 슬라이드 문구 추가 폼 (`slide_builder.py` 또는 `entry_form.py`)
- **기능:** 사용자가 2단계에서 고른 레이아웃 구조에 맞춰 Flet의 `TextField` 컴포넌트를 동적으로 생성합니다. 사용자는 문구를 다 입력한 후 '슬라이드 추가' 버튼을 눌러 자신이 만들 대기열(Deck) 리스트에 추가합니다.
- **예외 처리:** 필수 값 누락 검사(Pydantic Validation 연동).
- **액션:** 리스트(배열)에 순차적으로 슬라이드 데이터가 적재되며, 하단/측면에서 전체 슬라이드 구성 상황을 미리보기 리스트로 파악할 수 있게 합니다.

### View 4: 결과 화면 (`export.py`)
- **기능:** 전체 구성이 완료되면 생성 트리거를 발생시켜 `engine.generate_ppt`를 호출 (로딩 바 표시).
- **액션:** 생성이 완료되면 OS 네이티브 경로 열기(`os.startfile` 등) 버튼 제공. 성공 여부 피드백.
