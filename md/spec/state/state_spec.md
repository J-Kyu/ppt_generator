# State Management Specification

Flet은 화면(View)을 넘나들 때 로컬 변수가 소실되기 쉬운 특징이 있습니다. 따라서 여러 화면들(Onboarding ➔ Layout Picker ➔ Slide Builder ➔ Export) 간의 연속적인 데이터 흐름을 안전하게 보장하기 위해, 전역 상태(Global State) 관리 계층을 설계합니다.

---

## 1. 전역 상태 모델 (`state/app_state.py`)

서비스의 현재 위치와 사용자가 누적한 데이터를 기억하는 중앙 저장소입니다. 로컬 오프라인 전용 앱이므로, 단순한 **싱글톤(Singleton) 클래스 인스턴스** 구조나 **Flet의 `page.session`**을 활용하여 구현합니다.

### 1-1. 보관하는 상태 데이터 (Properties)
* `original_template_path` (str):
  * **설명:** 1단계에서 업로드되어 분석된 원본 파일(템플릿)의 절대 경로.
  * **용도:** 마지막 생성(Export) 단계에서 이 경로를 다시 참조해 템플릿의 사본을 열어야 하므로 반드시 저장해야 함.
* `available_layouts` (List[`LayoutSchema`]):
  * **설명:** 원본 PPT에서 엔진이 추출해 낸 "가용 레이아웃 목록" (Pydantic 모델 배열 형태).
  * **용도:** Layout Picker 화면에 렌더링하기 위해 사용.
* `user_deck` (List[`SlideSchema`]):
  * **설명:** 사용자가 작성 및 추가한 **슬라이드 대기열 장바구니**.
  * **용도:** 최종적으로 PPT를 합성할 때, 여기에 담긴 순서와 텍스트 데이터대로 슬라이드가 추가되며 생성됨.
* `current_selected_layout_id` (str 혹은 int):
  * **설명:** 사용자가 방금 레이아웃 뷰어에서 콕 집어서 선택한 대상.
  * **용도:** Slide Builder 화면에 진입할 때, 어떤 폼(`TextField`) 배열을 그려야 할지 식별하기 위함.

---

## 2. 상태 변경 메서드 (Actions/Mutators)

상태값의 무결성을 지키기 위해, UI 컴포넌트가 직접 배열에 `.append()` 하지 않고 `AppState` 내부의 전용 함수들을 통해서만 상태를 조작해야 합니다.

* `initialize_session(file_path: str, layouts: List[LayoutSchema])`
  * 파일이 성공적으로 읽힌 직후 호출되어 경로와 가용 레이아웃 목록을 세팅합니다.
* `add_slide_to_deck(slide_data: SlideSchema)`
  * 사용자가 폼 작성을 완료하고 '추가' 버튼을 누를 때 호출됩니다. `user_deck` 배열 맨 뒤에 추가합니다.
* `remove_slide_from_deck(index: int)`
  * 사용자가 UI의 장바구니 뷰어(Deck Area)에서 특정 슬라이드의 "삭제(x)" 아이콘을 누를 때 호출되어, 해당 슬라이드를 배열에서 제거합니다.
* `reorder_deck(old_index: int, new_index: int)` (선택/향후 확장)
  * 사용자가 만든 슬라이드들의 순서를 뒤바꿀 때 사용합니다.
* `reset_session()`
  * 작업이 모두 끝나고 '새 문서 만들기'를 눌렀을 때, 담겨있던 위 상태 데이터들을 완전 초기화합니다.

---

## 3. 타 계층과의 상호작용
* **UI 계층과의 관계:** UI(화면 컴포넌트)들은 `app_state`의 데이터를 읽어와서 화면을 그리며(Read), 사용자 액션에 의해 `app_state.add_slide_to_deck()` 등을 호출하여 데이터를 변경(Write)합니다.
* **Core 계층과의 관계:** 최종 렌더링(Export) 시, UI 계층은 `engine.generate_ppt()`에 인자값으로 `app_state.original_template_path`와 `app_state.user_deck`을 한꺼번에 전달합니다.
