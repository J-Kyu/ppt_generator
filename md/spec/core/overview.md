# Core Layer 세부 기능 정의 설계

`core` 계층은 프로젝트의 가장 핵심적인 비즈니스 로직을 담당하는 부분으로, 외부 요인(UI 등)에 의존하지 않고 독립적으로 동작해야 합니다. 핵심 요소인 **데이터 구조 명세(Schema)**와 **PPT 변환기(Engine)**로 나뉩니다.

---

## 1. Schema 계층 세부 설계 (`core/schema.py`)

Pydantic을 활용하여 데이터의 직렬화/역직렬화 및 런타임 유효성을 검증(Validation)하기 위한 모델을 정의합니다. 데이터의 구조는 계층적(Tree) 형식으로 구성됩니다.

### 1-1. `ShapeSchema`
개별 슬라이드 내에 존재하는 편집 가능한 요소(텍스트 박스, 이미지 등)를 정의합니다.
* **필드(Fields)**
  * `id` (int): 원본 PPT에서 해당 Shape가 갖는 고유 식별자
  * `name` (str): PPT에서 지정된 Shape의 이름 (동적 폼 생성 시 라벨로 활용)
  * `shape_type` (str): 요소의 타입 (현재는 `TEXT`를 기본으로 지원하며, 향후 `IMAGE` 확장을 대비)
  * `default_text` (str): 분석 당시 들어있던 원본 텍스트 내용
  * `user_input` (Optional[str]): 사용자가 동적 폼에서 실제로 입력한 값
  * `is_required` (bool): 폼 입력 시 필수 입력값인지 여부 (초기엔 무조건 `True`로 설정 가능)

### 1-2. `SlideSchema`
하나의 슬라이드를 관장하는 모델입니다.
* **필드(Fields)**
  * `slide_index` (int): 슬라이드의 순서(번호)
  * `shapes` (List[ShapeSchema]): 슬라이드 내부의 편집 가능한 Shape 리스트 (입력 가능한 텍스트 박스가 없으면 빈 리스트)

### 1-3. `PptSchema`
전체 프레젠테이션의 최상단 루트 모델입니다.
* **필드(Fields)**
  * `original_file_path` (str): 분석된 원본 파일(템플릿)의 절대 경로
  * `slides` (List[SlideSchema]): PPT의 전체 슬라이드 리스트
* **사용성**
  * `validate_inputs()`: 최종 PPT 생성 전, 사용자 입력이 다 채워졌는지 검증하는 Pydantic 내부 검증 로직 구현.

---

## 2. Engine 계층 세부 설계 (`core/engine.py`)

`python-pptx` 라이브러리를 래핑(Wrapping)하여 PPT 파일의 I/O와 수정 로직을 담당합니다.

### 2-1. `analyze_ppt` 함수
* **시그니처:** `def analyze_ppt(file_path: str) -> PptSchema:`
* **주요 흐름:**
  1. `file_path`로부터 `Presentation` 객체를 생성합니다.
  2. 모든 슬라이드를 개별적으로 순회하는 대신, **마스터 슬라이드(Slide Master)**와 **슬라이드 레이아웃(Slide Layout)**을 타겟으로 분석합니다.
  3. 반복되는 레이아웃을 식별할 수 있는 **고유 값 혹은 인덱스**를 부여하고, 해당 레이아웃 내의 `shape`들을 순회하여 `shape.has_text_frame`이 `True`인 텍스트 상자 등의 요소 특성(attribute)을 추출합니다.
  4. 추출한 정보 요소들로 `ShapeSchema` 객체를 생성하고, 상위의 `SlideSchema`(레이아웃 기준 배열), `PptSchema`로 묶어 반환합니다.
* **핵심 예외 처리:** 
  * 파일이 없거나 망가진 파일인 경우 `PPTAnalyzeError`를 발생시켜 UI 계층에서 알 수 있도록 함.

### 2-2. `generate_ppt` 함수
* **시그니처:** `def generate_ppt(template_path: str, user_deck: List[SlideSchema], output_path: str) -> bool:`
* **주요 흐름:**
  1. `template_path`의 원본 파일을 엽니다. (템플릿 내 기존 더미 슬라이드가 있다면 보존 혹은 옵션에 따라 삭제합니다)
  2. 사용자가 구성한 배열인 `user_deck`을 순차적으로 순회합니다.
  3. 반복될 때마다 `user_deck`의 각 요소가 지정한 **마스터 레이아웃 템플릿(Slide Layout)**을 원본에서 복사하여 새 슬라이드로 추가(`add_slide()`)합니다.
  4. 새로 추가된 슬라이드 레이아웃의 지정된 Shape 영역에 사용자가 폼에서 작성한 문자열(`user_input`)을 대입합니다. 서식 훼손을 막기 위해 `text_frame` 문단 제어 방식을 적용합니다.
  5. 처리가 완료된 형태의 프레젠테이션을 최종 `output_path`로 저장(Save)합니다.
  6. 성공 시 `True` 반환, 실패 시 로깅과 함께 Exception 반환.

---

## 3. 타 계층(State / UI)과의 인터페이스 고려
* **UI/State의 의존성:** UI 계층이나 State 계층은 `python-pptx` 라이브러리를 직접 호출하거나 import하지 않습니다. 반드시 `schema.py` 모델 객체와 `engine.py`의 함수만을 호출하여 데이터를 교환해야 합니다. 이를 통해 추후 로직이 바뀌더라도(예: 분석 툴 교체) UI 코드 수정이 발생하지 않도록 은닉합니다.
