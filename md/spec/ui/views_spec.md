# UI Layer: Views Specification

이 문서는 Flet 프레임워크를 기반으로 서비스의 각 화면(View) 단위가 어떤 컴포넌트로 렌더링되고, 데이터 흐름과 라우팅을 어떻게 제어할지 상세히 기술합니다.

## 1. Onboarding View (`ui/views/onboarding.py`)
- **역할:** 앱 실행 시 가장 먼저 마주하는 화면. 기준 템플릿(샘플 PPT) 파일을 업로드하는 진입점입니다.
- **주요 Flet 컴포넌트:** 
  - `ft.FilePicker`: 네이티브 파일 탐색기 호출을 위한 객체
  - `ft.Container` (Drop Zone): 커다란 사각형 영역의 Drag & Drop Zone 생성 (UI/UX 디자인 요소 강화)
  - `ft.Container` + `ft.Text` (경로 표시 박스): 파일 선택 직후 선택된 파일의 절대 경로를 시각적으로 표시 (파일 선택 전 숨김)
  - `ft.ProgressRing` / `ft.ProgressBar`: 파일이 업로드되고 파싱될 때 돌아가는 로딩 애니메이션
- **동작 흐름(Action):**
  1. 파일(템플릿)이 드래그 앤 드롭되거나 선택되면 **선택된 파일 경로를 즉시 화면에 표시**합니다.
  2. 화면에 스피너를 돌리고, 파일의 절대 경로를 `core.engine.analyze_ppt()`에 넘겨 분석을 요청합니다.
  3. 정상적으로 반환된 전체 레이아웃 스키마 목록을 전역 상태인 `app_state`에 저장합니다.
  4. 로딩 스피너 작동을 종료하고 `Layout Picker View` (단계 2)로 화면 라우팅을 이동합니다.

---

## 2. Layout Picker View (`ui/views/layout_picker.py`)
- **역할:** 엔진이 추출해 낸 가용 슬라이드 레이아웃(Slide Layout)들의 목록을 보여주어 선택하게 합니다.
- **주요 Flet 컴포넌트:**
  - `ft.GridView` 또는 `ft.ListView`: 여러 개의 레이아웃을 갤러리 형태로 나열
  - `ft.Card`: 개별 레이아웃을 시각적으로 분리하기 위한 카드 뷰 
  - `ft.Text`: 카드 내부에 레이아웃의 이름(Title) 및 텍스트 상자 개수 등의 속성을 간략히 표기
- **동작 흐름(Action):**
  1. `app_state`에 보관된 분석 레이아웃 목록 배열을 순회하며 카드를 렌더링합니다.
  2. 사용자가 특정 카드를 클릭하면, 선택된 레이아웃의 고유 식별자(Index 또는 Name)를 지참하여 `Slide Builder View` (단계 3)로 이동합니다.

---

## 3. Slide Builder View (`ui/views/slide_builder.py` - 핵심)
- **역할:** 선택한 레이아웃 형태에 맞춰 동적으로 입력 폼을 출력하고, 텍스트를 기입한 슬라이드 1장을 완성하여 전체 대기열(Deck) 리스트에 누적시키는 메인 작업 화면입니다.
- **주요 Flet 컴포넌트:**
  - **Left Panel (Form Area):** `ft.Column` 
    - `core.schema`에 정의된 개별 속성들을 `ft.TextField`로 동적 생성하여 렌더링.
    - `ft.ElevatedButton` ("슬라이드 누적/추가하기" 버튼)
  - **Right Panel (Deck Area):** `ft.ListView` 
    - 사용자가 지금까지 누적 생성한 슬라이드 대기열 타임라인을 순서대로 표시(과거 생성 이력 확인용).
  - **Bottom Navigation:** `ft.ElevatedButton` ("완료 및 빌드하기" 버튼과 "다른 레이아웃 추가하기" 버튼)
- **동작 흐름(Action):**
  1. 화면 진입 시 전달받은 레이아웃 식별자를 바탕으로 필요한 입력 폼을 화면 왼쪽 패널에 그립니다.
  2. 데이터 입력 후 '추가' 버튼 트리거 시, 빈칸 등의 유효성 검사(Validation)를 수행합니다.
  3. 검사가 통과되면 해당 슬라이드 1장 분량의 데이터를 `app_state` 내부의 배열(Slide Deck List)에 `.append()` 합니다.
  4. 화면 오른쪽 장바구니 리스트(Deck Area)를 최신 업데이트하여 시각 피드백을 줍니다.
  5. 추가가 모두 끝나 파일로 내보내고 싶다면 '완료 및 빌드하기' 버튼을 눌러 라우팅합니다.

---

## 4. Export & Result View (`ui/views/export.py`)
- **역할:** 사용자가 누적 구성해낸 슬라이드 대기열(Deck)을 실물 PPT로 구워내고 완료를 축하하는 화면입니다.
- **주요 Flet 컴포넌트:**
  - `ft.ProgressBar` / `ft.Text` : 파일 렌더링 진행률 및 처리 메시지 노출
  - `ft.Lottie` 또는 `ft.Icon` : 완료를 알리는 시각적 축하 애니메이션/아이콘
  - `ft.TextButton` : 만들어진 새 폴더 열기 / "새 문서 시작하기" 기능 지원
- **동작 흐름(Action):**
  1. 화면에 들어오자마자 `app_state`에 저장된 원본 템플릿 경로와 `user_deck` 배열 전체를 `core.engine.generate_ppt()`로 넘깁니다. (오래 걸릴 수 있으므로 가급적 비동기/스레드 안에서 호출합니다)
  2. 엔진이 처리를 마치고 성공 결과를 반환하면 로딩 바를 완성 화면 컴포넌트로 교환(Update)합니다.
  3. '시작 폴더 열기' 클릭 시 `os.startfile(output_path)` (Mac의 경우 `open`) 등을 호출해 사용자가 문서를 즉시 볼 수 있게 에스코트합니다.
  4. '새 문서 시작하기' 클릭 시 `app_state` 데이터를 모두 지우고 Onboarding View로 회귀합니다.
